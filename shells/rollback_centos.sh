#!/bin/bash

target_directory=$1
www_dir=$2
echo $1
echo $2
echo $3


echo "switch user"
su - git
cd $target_directory
pwd

echo "starting rollback"
git reset --hard HEAD~ # 这里可以改成指定的版本号
git push -f origin master
echo "ended rollback"

exit
echo "logout git user"

cd $www_dir
echo "starting to push"
git -C $www_dir pull origin master
echo "ended to deploy"


