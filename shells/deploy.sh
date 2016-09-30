#!/bin/bash

project_dir=$1
target_directory=$2
www_dir=$3
echo $1
echo $2
echo $3

cp -R $project_dir $target_directory

cd $target_directory
pwd

echo "starting to git commint and push to centeral repository"
git stash
git remote -v
git add .
git commit -am 'update'
git push origin master
echo "ended commit and push"

echo "starting to push"
git -C $www_dir pull origin master

echo "ended to deploy"


