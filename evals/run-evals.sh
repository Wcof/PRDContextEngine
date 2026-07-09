#!/usr/bin/env bash
# PMSkill 评估运行器 (model-free structural validation)
#
# 用法：
#   bash evals/run-evals.sh --dry-run
#   bash evals/run-evals.sh --dry-run --skill pm-prd
#   bash evals/run-evals.sh --live   # 当前 live 仍降级为结构校验

set -euo pipefail

MODE="dry-run"
SKILL_FILTER=""
EVALS_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$EVALS_DIR/.." && pwd)"
RESULTS_TSV="$EVALS_DIR/results.tsv"
RESULTS_JSON="$EVALS_DIR/results.json"

usage() {
  cat >&2 <<EOF
PMSkill 评估运行器
用法: bash evals/run-evals.sh [--dry-run|--live] [--skill <name>]
  --dry-run    只做结构校验（默认）
  --live       调用 Agent CLI 跑真实 query（当前降级为 dry-run）
  --skill <n>  只跑指定 skill（如 pm-prd）
  -h, --help   显示本帮助
EOF
  exit 2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) MODE="dry-run"; shift;;
    --live)    MODE="live"; shift;;
    --skill)   [[ $# -ge 2 ]] || usage; SKILL_FILTER="$2"; shift 2;;
    -h|--help) usage;;
    *) echo "未知参数: $1" >&2; usage;;
  esac
done

if ! command -v python3 >/dev/null 2>&1; then
  echo "✗ 需要 python3 解析 JSON" >&2
  exit 2
fi

if [[ "$MODE" == "live" ]]; then
  if ! command -v claude >/dev/null 2>&1 && ! command -v codex >/dev/null 2>&1; then
    echo "⚠ 未找到 claude/codex CLI，自动降级为 --dry-run" >&2
  else
    echo "⚠ --live 真实模型跑分尚未接入，当前执行结构校验" >&2
  fi
  MODE="dry-run"
fi

python3 - "$EVALS_DIR" "$RESULTS_TSV" "$RESULTS_JSON" "$MODE" "$SKILL_FILTER" <<'PY'
from __future__ import annotations

import glob
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

evals_dir = Path(sys.argv[1])
results_tsv = Path(sys.argv[2])
results_json = Path(sys.argv[3])
mode = sys.argv[4]
skill_filter = sys.argv[5]

if skill_filter:
    files = [evals_dir / f"{skill_filter}.json"]
    if not files[0].exists():
        print(f"✗ 未找到 evals/{skill_filter}.json", file=sys.stderr)
        sys.exit(2)
else:
    files = [Path(p) for p in sorted(glob.glob(str(evals_dir / "pm-*.json")))]

if not files:
    print("✗ 未找到任何 evals/pm-*.json", file=sys.stderr)
    sys.exit(2)

rows = []
for file in files:
    print(f"▶ {file.stem} ({file})")
    try:
        data = json.loads(file.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        row = {"skill":"","scenario_id":"","query":"","expected_count":0,"status":"FAIL","note":f"JSON解析失败: {exc}"}
        rows.append(row)
        print(f"   \t\t\t0\tFAIL\t{row['note']}")
        continue
    if not isinstance(data, list) or not data:
        row = {"skill":"","scenario_id":"","query":"","expected_count":0,"status":"FAIL","note":"顶层非数组或为空"}
        rows.append(row)
        print(f"   \t\t\t0\tFAIL\t{row['note']}")
        continue
    for sc in data:
        sid = str(sc.get("id", "?"))
        skills = sc.get("skills", [])
        skill = skills[0] if skills else "?"
        query = sc.get("query", "")
        query_short = query[:40].replace("\t", " ").replace("\n", " ")
        eb = sc.get("expected_behavior", [])
        fixtures = sc.get("files", [])
        issues = []
        if not skills:
            issues.append("缺 skills")
        if not query:
            issues.append("缺 query")
        if not isinstance(eb, list) or not eb:
            issues.append("expected_behavior 为空")
        for fp in fixtures:
            cand = evals_dir / fp if not os.path.isabs(fp) else Path(fp)
            if not cand.exists():
                issues.append(f"夹具缺失: {fp}")
        status = "FAIL" if issues else "PASS"
        note = ";".join(issues) if issues else f"{len(eb)} 条 expected_behavior"
        row = {"skill":skill,"scenario_id":sid,"query":query_short,"expected_count":len(eb) if isinstance(eb, list) else 0,"status":status,"note":note}
        rows.append(row)
        print(f"   {skill}\t{sid}\t{query_short}\t{row['expected_count']}\t{status}\t{note}")

pass_count = sum(1 for r in rows if r["status"] == "PASS")
partial_count = sum(1 for r in rows if r["status"] == "PARTIAL")
fail_count = sum(1 for r in rows if r["status"] == "FAIL")

generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
with results_tsv.open("w", encoding="utf-8") as fh:
    fh.write(f"# PMSkill 评估结果 — mode={mode} generated={generated}\n")
    fh.write("skill\tscenario_id\tquery\texpected_count\tstatus\tnote\n")
    for r in rows:
        fh.write(f"{r['skill']}\t{r['scenario_id']}\t{r['query']}\t{r['expected_count']}\t{r['status']}\t{r['note']}\n")

summary = {"mode":mode,"total":len(rows),"pass":pass_count,"partial":partial_count,"fail":fail_count,"scenarios":rows}
results_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"机读汇总: {results_json}")
print("\n=== 汇总 (mode=%s) ===" % mode)
print(f"总计: {len(rows)} | PASS: {pass_count} | PARTIAL: {partial_count} | FAIL: {fail_count}")
print(f"TSV : {results_tsv}")
print(f"JSON: {results_json}")
sys.exit(1 if fail_count else 0)
PY
