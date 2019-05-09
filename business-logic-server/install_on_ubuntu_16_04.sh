#!/usr/bin/env bash
echo "Setting up Business Logic Server"
sudo apt-get update
sudo apt-get install postgresql binutils libproj-dev gdal-bin postgresql-contrib redis-server screen gunicorn nginx

#setup database
sudo -u postgres createuser flyright_user
sudo -u postgres createdb flyright_db
psql -u postgres -d "flyright_db" -c "CREATE EXTENSION postgis;"
psql -u postgres -d "flyright_db" -c "GRANT ALL PRIVILEGES on DATABASE flyright_db to flyright_user;"

#setup nginx proxy?
sudo ln /home/ubuntu/FlyRight/business-logic-server/flyright-nginx-site /etc/nginx/sites-enabled/
sudo service nginx restart

# setup python
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6
# Setup virtualenvironment
sudo apt-get install virtualenv
virtualenv /home/ubuntu/FlyRight/business-logic-server/venv --python=python3.6
/home/ubuntu/FlyRight/business-logic-server/venv/bin/pip install -r /home/ubuntu/FlyRight/business-logic-server/requirements.txt