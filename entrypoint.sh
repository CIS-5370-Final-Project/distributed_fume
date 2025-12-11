#!/bin/bash
set -e

# Determine fuzzer mode and run
# Note: Mosquitto is started by the fuzzer via START_COMMAND in config_docker.txt
if [ "$FUZZER_MODE" = "master" ]; then
    echo "[*] Running as MASTER instance: $INSTANCE_NAME"
    python3 -u /app/fuzz.py /app/config_master.txt -M "$INSTANCE_NAME"
elif [ "$FUZZER_MODE" = "secondary" ]; then
    echo "[*] Running as SECONDARY instance: $INSTANCE_NAME"
    python3 -u /app/fuzz.py /app/config_secondary.txt -S "$INSTANCE_NAME"
elif [ "$FUZZER_MODE" = "third" ]; then
    echo "[*] Running as THIRD instance: $INSTANCE_NAME"
    python3 -u /app/fuzz.py /app/config_third.txt -S "$INSTANCE_NAME"
else
    echo "[*] Running in STANDALONE mode"
    python3 -u /app/fuzz.py /app/config_docker.txt
fi
