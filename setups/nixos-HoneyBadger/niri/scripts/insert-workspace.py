#!/usr/bin/env python3

import json
import subprocess


def niri(*args):
    return subprocess.run(
        ["niri", "msg", *args], check=True, capture_output=True, text=True
    ).stdout


workspaces = json.loads(niri("--json", "workspaces"))
focused = next(w for w in workspaces if w["is_focused"])
idx = focused["idx"]
last = max(w["idx"] for w in workspaces if w["output"] == focused["output"])

# Already on the empty trailing workspace: nothing to insert
if idx >= last:
    raise SystemExit

# Jump to the trailing empty workspace and move it up to where you started
niri("action", "focus-workspace", str(last))
for _ in range(last - idx):
    niri("action", "move-workspace-up")

