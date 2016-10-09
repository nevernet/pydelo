Pydelo - A Deploy Tool
======================
这是一个Python语言编写的自动化上线部署系统，只需做很少的配置就可以立即使用。
系统将整个发布过程分成两个部分：checkout 和 deploy
* checkout
此部分做代码的检出动作，并且在代码的检出前后可以分别做一些shell操作，如编译动作，配置文件修改等。
* deploy
此部分做代码的发布动作，通过rsync将代码同步到远端机器的指定目录，在代码的同步前后也可以分别做一些shell操作，如相关服务的stop、start，某些清理工作等。

前期环境配置
------

* git中心仓库，工作目录，项目目录配置

```
# 创建用户：
groupadd www
useradd -g www www

su - git # 切换到git用户
mkdir git-repository # 中心仓库
cd git-repository
mkdir test.git
cd test.git
git init --bare  # 创建bare仓库

cd ~

# 创建git 工作目录
mkdir git-working
cd git-working
mkdir test-project #创建测试项目
cd test-project
git init
git remote add origin /home/git/git-repository/test.git
touch README.md
git add . 
git commit -am 'init'
git push origin master

exit #  退出git用户

# 切换到项目实际目录地址, 假定项目网址是api.test.com
cd /opt/www
mkdir api.test.com
cd api.test.com
git init
git remote add origin /home/git/git-repository/test.git
git pull origin master
```

* 修改web/config-example.py的配置
> 把config-example.py修改成config.py然后在修改

2. Requirements
---------------

* Bash(git, rsync, ssh, sshpass)
* MySQL
* Python
* Python site-package(flask, flask-sqlalchemy, pymysql, paramiko)

That's all.

Installation
------------
```
apt-get install rsync sshpass
git clone git@github.com:meanstrong/pydelo.git
cd pydelo
pip install -r pip_requirements.txt # 建议使用virtualenv来部署
mysql -h root -p pydelo < db-schema.sql  # create database and tables
vi web/config.py # set up module config such as mysql connector
python init.py   # add some data to mysql or you can do it yourself

python manage.py # start flask web app
```

Usage
-----
#### 1.Add project
![image](https://github.com/meanstrong/pydelo/raw/master/docs/create_project.png)

#### 2.New deploy
![image](https://github.com/meanstrong/pydelo/raw/master/docs/create_deploy.png)

#### 3.Deploy progress
![image](https://github.com/meanstrong/pydelo/raw/master/docs/deploy_progress.png)

#### 4.Deploys
![image](https://github.com/meanstrong/pydelo/raw/master/docs/deploys.png)

Discussing
----------
- email: ysixin@gmail.com


Todo
----------
1.部署失败时的详细log信息展示在前台
2.rc错误码完善
3.权限控制的更合理，对资源的访问权限需要更加细化
