#!/bin/bash

## Check user permissions ##
if [ $(id -u) != "0" ]; then
	echo "Error: NO PERMISSION! Please login as root to install Volcano."
	exit 1
fi

function yum_update()
{
	IS_64=`uname -a | grep "x86_64"`
	if [ -z "${IS_64}" ]
	then
		CPU_ARC="i386"
	else
		CPU_ARC="x86_64"
	fi

	IS_5=`cat /etc/redhat-release | grep "5.[0-9]"`
	if [ -z "${IS_5}" ]
	then
		VER="6"
		rpm_ver="epel-release-6-8.noarch.rpm"
	else
		VER="5"
		rpm_ver="epel-release-5-4.noarch.rpm"
	fi
	setenforce 0
	rpm -ivh "http://dl.fedoraproject.org/pub/epel/${VER}/${CPU_ARC}/${rpm_ver}"
	rm -rf /etc/localtime
	ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

	yum -y install yum-fastestmirror ntpdate ntp
	ntpdate -u pool.ntp.org
	/sbin/hwclock -w
}	

function install_gearman()
{
	yum -y install python26 python26-mysqldb MySQL-python python-setuptools-devel
	yum -y install gearman libgearman
	wget -c http://pypi.python.org/packages/source/g/gearman/gearman-2.0.1.tar.gz
	tar xvzf  gearman-2.0.1.tar.gz
	python2.6 setup.py install
}

function install_env()
{
	yum -y install expect
}

function build_install_dir()
{
	volcano="/usr/local/volcano"
}
