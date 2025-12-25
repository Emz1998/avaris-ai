#!/bin/bash
# launch-claudes.sh - Launch multiple Claude Code terminals in VS Code

COUNT=${1:-2}  # Default to 2 terminals

for i in $(seq 1 $COUNT); do
  code -r --command "workbench.action.terminal.new"
  sleep 0.3
done

echo "Opened $COUNT terminals - type 'claude' in each"
