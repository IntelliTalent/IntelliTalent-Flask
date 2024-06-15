#!/usr/bin/env bash

echo "Starting Scrapper App"

gunicorn scrapper_app_wsgi:app \
	-p ./pid \
	-k eventlet \
	-b 0.0.0.0:5000 \
	--name=scrapper_app \
	--log-level 0 \
	--log-file logs/scrapper_app.log \
	--error-logfile logs/scrapper_app.error.log \
	--access-logfile logs/scrapper_app.access.log \
	--capture-output \
	--reload
sleep 1
if [ -f pid ]; then
    echo "	started master worker pid:$(cat pid)"
else
	echo "	failed starting master worker"
fi
