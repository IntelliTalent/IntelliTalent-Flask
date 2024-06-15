#!/usr/bin/env bash

echo "Starting CV Generator App"

gunicorn cv_generator_app_wsgi:app \
	-p ./pid \
	-k eventlet \
	-b 0.0.0.0:5000 \
	--name=cv_generator_app \
	--workers 4 \
	--log-level 0 \
	--log-file logs/cv_generator_app.log \
	--error-logfile logs/cv_generator_app.error.log \
	--access-logfile logs/cv_generator_app.access.log \
	--capture-output \
	--daemon
sleep 1
if [ -f pid ]; then
	echo "	started master worker pid:$(cat pid)"
else
	echo "	failed starting master worker"
fi
