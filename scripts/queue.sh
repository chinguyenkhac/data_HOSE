#!/bin/bash
# Hàng đợi job nặng: tối đa MAXP tiến trình run_grid.py cùng lúc (mỗi tiến trình 1 luồng BLAS). Dùng: queue.sh MAXP "job1" "job2" ...
cd "$(dirname "$0")/../notebooks"; MAXP=$1; shift
for j in "$@"; do
  while [ "$(pgrep -fc 'scripts/run_grid.py')" -ge "$MAXP" ]; do sleep 20; done
  n=$(echo "$j" | tr -c 'A-Za-z0-9\n' '_'); echo "$(date -u +%H:%M) start $j" >> results_v4/logs/queue.log
  nohup python3 ../scripts/run_grid.py "$j" > "results_v4/logs/job_$n.log" 2>&1 &
  sleep 5
done
wait
