#!/usr/bin/env bash
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: %s

export service_file=%s
export bin_dir=%s
export svrd=%s
export proc_key=%s
export log_file=%s
export PYTHONPATH=${bin_dir}/lemon:${bin_dir}/script

source ${bin_dir}/script/template/base.sh

log "cd ${bin_dir}"
cd ${bin_dir}

log "pypy ${svrd} ${proc_key} ${log_file}"
nohup pypy ${svrd} ${proc_key} ${log_file} >> ${log_file} 2>&1 &
