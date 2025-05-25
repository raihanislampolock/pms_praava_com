#!/bin/bash
while true; do
    echo "Running pms.py at $(date)"
    python pms.py
    sleep 300  # 5 minutes
done