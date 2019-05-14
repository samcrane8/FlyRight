#!/usr/bin/env bash
echo "Setting up Business Logic Server"
sudo yum update
sudo yum install postgresql binutils libproj-dev gdal-bin postgresql-contrib redis-server screen gunicorn nginx

#postgis
sudo yum -y install epel-release
sudo yum install https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/postgis23_10-2.3.7-1.rhel7.x86_64.rpm
sudo yum install postgis23_10

#redis
sudo yum install yum-utils
sudo yum install http://rpms.remirepo.net/enterprise/remi-release-7.rpmsudo yum-config-manager --enable remi
sudo yum install redis

sudo systemctl start redis
sudo systemctl enable redis

#setup database
sudo -u postgres createuser flyright_user
sudo -u postgres psql -c "ALTER USER flyright_user PASSWORD 'password';"
sudo -u postgres createdb flyright_db
sudo -u postgres psql -d "flyright_db" -c "CREATE EXTENSION postgis;"
sudo -u postgres psql -d "flyright_db" -c "GRANT ALL PRIVILEGES on DATABASE flyright_db to flyright_user;"
sudo -u postgres psql -c "ALTER USER flyright_user with SUPERUSER";

sudo systemctl restart postgresql10.service

#setup nginx proxy?
sudo ln flyright-nginx-site /etc/nginx/sites-enabled/
sudo service nginx restart

# Setup virtualenvironment
python3 -m venv venv
venv/bin/pip install -r requirements.txt
