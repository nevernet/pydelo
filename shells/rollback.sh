#!/bin/bash

target_directory=$1
www_dir=$2
echo $1
echo $2
echo $3


cd $target_directory
pwd

echo "starting rollback"
git reset --hard HEAD~
git push -f origin master
echo "ended rollback"

echo "starting to push"
git -C $www_dir pull origin master
echo "ended to deploy"


