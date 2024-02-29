#!/usr/bin/env bash

source venv/bin/activate

echo "Starting Interview App"

gunicorn interview_app_wsgi:app \
	-p ./pid \
	-k eventlet \
	-b 0.0.0.0:5000 \
	--name=interview_app \
	--workers 4 \
	--log-level 0 \
	--log-file logs/interview_app.log \
	--error-logfile logs/interview_app.error.log \
	--access-logfile logs/interview_app.access.log \
	--capture-output \
	--daemon
sleep 1
if [ -f pid ]; then
	echo "	started master worker pid:$(cat pid)"
else
	echo "	failed starting master worker"
fi
