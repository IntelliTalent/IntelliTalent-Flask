#!/usr/bin/env bash

cp -r /tmp/venv /usr/src/app/venv

cp /tmp/requirements.txt /usr/src/app/requirements.txt

if [ "$APP" = "cover-letter-generator" ]; then
    python -m spacy download en_core_web_lg
else
    echo "APP is not cover-letter-generator, skipping command"
fi

bash /usr/src/app/startDev.bash

while true; do sleep 1; done
