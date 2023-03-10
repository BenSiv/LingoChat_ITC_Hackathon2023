#!/bin/bash

# root read only
chmod 400 Ben-key-pair.pem

# connect to server via ssh
ssh -i "~/Documents/ITC/Main/Deployment/DeployConfig/Ben-key-pair.pem" "ubuntu@ec2-18-196-35-85.eu-central-1.compute.amazonaws.com"

# clone git repo
git clone https://github.com/BenSiv/LingoChat_ITC_Hackathon2023.git

# installing mysql
sudo apt install mysql-server
sudo apt install mysql-client

# connecting to mysql server
sudo mysql --user root

# from remote
mysql -h eu-central.connect.psdb.cloud -u m1ow7xhhjf2u87ondhja -ppscale_pw_kI2oJ1yIUdgQQHMK4ovdB6UARJB4cf8UAmWwJliuuJp --ssl-ca=/etc/ssl/certs/ca-certificates.crt
