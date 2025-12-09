#!/bin/bash
set -e

echo "[DEBUG] Entrypoint started"
echo "[DEBUG] FUZZER_MODE=$FUZZER_MODE"
echo "[DEBUG] INSTANCE_NAME=$INSTANCE_NAME"
echo "[DEBUG] Checking mosquitto binary..."
which mosquitto || echo "[DEBUG] mosquitto not in PATH"
ls -la /usr/sbin/mosquitto 2>/dev/null || echo "[DEBUG] mosquitto not in /usr/sbin"

# Determine fuzzer mode and run
# Note: Mosquitto is started by the fuzzer via START_COMMAND in config_docker.txt
if [ "$FUZZER_MODE" = "master" ]; then
    echo "[*] Running as MASTER instance: $INSTANCE_NAME"
    python3 -u /app/fuzz.py /app/config_docker.txt -M "$INSTANCE_NAME" -o /app/fume_sync
elif [ "$FUZZER_MODE" = "secondary" ]; then
    echo "[*] Running as SECONDARY instance: $INSTANCE_NAME"
    python3 -u /app/fuzz.py /app/config_docker.txt -S "$INSTANCE_NAME" -o /app/fume_sync
else
    echo "[*] Running in STANDALONE mode"
    python3 -u /app/fuzz.py /app/config_docker.txt -o /app/fume_sync
fi

echo "[DEBUG] Fuzzer exited with code: $?"
