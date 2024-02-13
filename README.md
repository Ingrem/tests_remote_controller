## Description

Django channels application for running tests/managing test circuit/decrypting json files/running and managing load testing from one place

## File structure
##### /qa_remote_controller

projects settings
* urls - url all apps
* routing - url all сокетов
* asgi - file Asynchronous Server Gateway Interface, for nginx deploying
* settings - setting for django

##### /static

css and all pictures

##### /templates

html pages

## Deploying 

cd /home/user/apps/tests-remote-control

sudo git pull (use your login and pass from gitlab)

sudo systemctl restart daphne.service

sudo systemctl status daphne.service

## Commands

##### debug run server:

nohup python3.6 manage.py runserver 0.0.0.0:9080 &

##### restart nginx on remote server

sudo systemctl restart nginx

##### restart daphne on remote server

sudo systemctl restart daphne.service

##### setting form daphne_sed.service

/etc/systemd/system/daphne.service

##### файлы отчетов
Need to set up nginx statics share and add allure reports

/usr/share/nginx/html/stats

