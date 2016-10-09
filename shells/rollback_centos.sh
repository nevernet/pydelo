#!/bin/bash

target_directory=$1
www_dir=$2
echo $1
echo $2
echo $3


echo "switch user"
su - git <<HERE
cd $target_directory
pwd

echo "starting rollback"
git reset --hard HEAD~ # 这里可以改成指定的版本号
git push -f origin master
echo "ended rollback"

exit
echo "logout git user"

HERE

echo "starting to push"
cd $www_dir
pwd
#git -C $www_dir pull origin master
git fetch origin
git reset --hard origin/master
git clean -f -d
echo "ended to deploy"


