#!/bin/bash

set -e

if [[ -e ~/hfsql-installed ]]; then
    echo "hfsql driver already installed"
    exit
fi

apt-get update
apt-get -fyq install wget iodbc
cd /tmp/
wget https://package.windev.com/pack/wx23_42u/fr/commun/WX230PACKODBCLINUX64042u.zip
unzip WX230PACKODBCLINUX64042u.zip -d hfsql_drive
cd hfsql_driver
chmod +x install.sh
./install.sh

touch ~/.odbc.ini

echo '[ODBC Data Sources]
<Source Name> = HFSQL
[<Source Name>]
Server Name = <Name of server>
Server Port = <Port to use>
Database = <Name of database>
UID = <Name of user>
PWD = <Password of user>' >> ~/.odbc.ini
