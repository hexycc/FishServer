#!/usr/bin/env bash
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: %s

export service_file="%s"
export bin_dir="%s"
export redis_host="%s"
export redis_port="%s"
export redis_db="%s"


source ${bin_dir}/script/template/base.sh
redis_cli="redis-cli"

type ${redis_cli} 1>/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "not exist cmd: ${redis_cli}"
    exit 1
fi

redis_cmd="${redis_cli} -h ${redis_host} -p ${redis_port} -n ${redis_db}"
result=`echo "PING" | ${redis_cmd} 2>/dev/null`
if [ "${result}" != "PONG" ]; then
    echo -e "Could not connect to Redis at ${redis_host}:${redis_port}:${redis_db}"
    exit 2
fi

keys_alias=KEYS
info=`${redis_cmd} COMMAND INFO KEYS`
if [ "${info}" == "" ]; then
    keys_alias=REDIS-KEYS
fi

${redis_cmd} ${keys_alias} "quick:*" | awk '{print "del " $1}' | ${redis_cmd} >/dev/null 2>&1
${redis_cmd} ${keys_alias} "area:*" | awk '{print "del " $1}' | ${redis_cmd} >/dev/null 2>&1
${redis_cmd} ${keys_alias} "table:*" | awk '{print "del " $1}' | ${redis_cmd} >/dev/null 2>&1
${redis_cmd} ${keys_alias} "location:*" | awk '{print "del " $1}' | ${redis_cmd} >/dev/null 2>&1
${redis_cmd} ${keys_alias} "online.info*" | awk '{print "del " $1}' | ${redis_cmd} >/dev/null 2>&1
${redis_cmd} ${keys_alias} "cache.*.info.hash" | awk '{print "del " $1}' | ${redis_cmd} >/dev/null 2>&1
${redis_cmd} del global.playing.lock >/dev/null 2>&1
