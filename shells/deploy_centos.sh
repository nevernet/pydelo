#!/bin/bash

project_dir=$1
target_directory=$2
www_dir=$3
echo "project dir:", $1
echo "target dir:", $2
echo "www dir:", $3

cp -R $project_dir/* $target_directory

cd $target_directory
pwd
echo "chown"
chown -R git:git $target_directory

echo "switch user"
su - git <<HERE
cd $target_directory
pwd

echo "starting to git commit and push to central repository"
git remote -v
git add .
git commit -am 'update'
git push origin master
echo "ended commit and push"

exit
echo "logout git user"

HERE

cd $www_dir
pwd
echo "starting to pull"
# git -C $www_dir pull origin master
git pull origin master

echo "ended to deploy"


