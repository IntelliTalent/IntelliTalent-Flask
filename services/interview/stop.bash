#!/usr/bin/env bash

PID=pid
WORKERS=$(ps -Ao pid,comm,args | grep "interview_app_wsgi:app" | awk '{print $1}')
if [ -f pid ]; then
    echo "stop master worker $(cat pid)."
    kill -9 $(cat pid)
    rm pid
fi
for worker in $WORKERS; do
    echo "stop worker $worker."
    kill -9 $worker
done
