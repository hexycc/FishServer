#!/usr/bin/env bash
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: %s

export service_file=%s
export proc_key=%s
export bin_dir=%s

source ${bin_dir}/script/template/base.sh

log "kill ${proc_key} ..."

pids=`ps -ef | grep "${proc_key}" | grep -v "grep " | awk '{print $2}'`

count=0

while  [ "${pids}" != "" ]; do
    ((count++))
    if [ ${count} -gt 20 ]; then
        log "failed"
        exit 1
    elif [ ${count} -gt 10 ]; then
        force='-9'
    fi

    echo "${pids}" | xargs kill ${force}
    sleep 0.01
    pids=`ps -ef | grep "${proc_key}" | grep -v "grep " | awk '{print $2}'`
done
