#!/bin/bash
#

backup_dir='../data/backup/'

if [ ! -d $backup_dir ];then
    mkdir $backup_dir
fi

mysqldump -uroot -h127.0.0.1 -p glance > ${backup_dir}/glance_$(date +'%Y-%m-%d_%H:%M:%S').sql
