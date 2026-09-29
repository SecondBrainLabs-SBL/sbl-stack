from pathlib import Path
import json
import re

instructions = (Path(__file__).resolve().parents[1] / "sbl-triage/INSTRUCTIONS.md").read_text()
step = instructions.split("## Step 1 — Get all running campaigns", 1)[1].split("## Step 2", 1)[0]
call = step.split("Call `sbl_list_campaigns` MCP tool with:", 1)[1].split("Show a brief table", 1)[0]
arrays = re.findall(r"(?m)^- `statuses`: (\[[^\n]+\])$", call)
assert len(arrays) == 1, f"Expected one statuses array in triage list_campaigns call, found {len(arrays)}"
assert json.loads(arrays[0]) == ["7", "4", "5", "6"], f"Invalid triage statuses: {arrays[0]}"
