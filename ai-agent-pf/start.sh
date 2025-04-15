#!/bin/bash

# stop services created by runsv and propagate SIGINT, SIGTERM to child jobs
sv_stop() {
    echo "$(date -uIns) - Stopping all runsv services"
    for s in $(ls -d /var/runit/*); do
        sv stop $s
    done
}

echo "Available connections:"
ls $PF_CONNECTIONS_DIR
cat $PF_CONNECTIONS_DIR/AIProjectConnectionString.yaml
# register SIGINT, SIGTERM handler
trap sv_stop SIGINT SIGTERM

# start services in background and wait all child jobs
runsvdir /var/runit &
wait
