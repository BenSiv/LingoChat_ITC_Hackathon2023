#!/bin/bash

# root read only
chmod 400 Ben-key-pair.pem

# connect to server via ssh
ssh -i "~/Documents/ITC/Main/Deployment/DeployConfig/Ben-key-pair.pem" "ubuntu@ec2-35-159-22-109.eu-central-1.compute.amazonaws.com"

# clone git repo
git clone https://github.com/BenSiv/LingoChat_ITC_Hackathon2023.git

# installing mysql
sudo apt install mysql-server
sudo apt install mysql-client

# connecting to mysql server
sudo mysql --user root

# from remote
mysql -h eu-central.connect.psdb.cloud -u 46p23e3ut8foc76nyqwj -ppscale_pw_u34i747OWB9j9dbDuiIut2hSba4gW3703Mn4RX7T3BM --ssl-ca=/etc/ssl/certs/ca-certificates.crt

