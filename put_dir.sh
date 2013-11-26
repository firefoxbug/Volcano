#!/bin/bash

# Function : transfer directory from localhost to remote node
# args     : ip password local_dir remote_dir
# Author   : firefoxbug
# Date     : 2013/10/01

if [ $# -ne 4 ]
then
	echo "[ERROR] usage : ./put_dir ip password source_dir dst_dir"
	exit 1
fi

ip=$1
port="22"
passwd=$2
local_dir=$3
remote_dir=$4

expect -c "
	spawn scp -oConnectTimeout=3 -r -P $port $local_dir root@$ip:$remote_dir
	expect {
		\"*assword\" {set timeout 300; send \"$passwd\r\";}
		\"yes/no\" {send \"yes\r\"; exp_continue;}
	}
	expect eof"