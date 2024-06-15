#!/usr/bin/env bash

if [ -f pid ]; then
    bash stop.bash
fi

echo "Starting Cover Letter Generator App"

gunicorn cover_letter_generator_app_wsgi:app \
	-p ./pid \
	-k eventlet \
	-b 0.0.0.0:5000 \
	--name=cover_letter_generator_app \
	--workers 4 \
	--log-level 0 \
	--log-file logs/cover_letter_generator_app.log \
	--error-logfile logs/cover_letter_generator_app.error.log \
	--access-logfile logs/cover_letter_generator_app.access.log \
	--capture-output \
	--daemon
sleep 1
if [ -f pid ]; then
	echo "	started master worker pid:$(cat pid)"
else
	echo "	failed starting master worker"
fi
