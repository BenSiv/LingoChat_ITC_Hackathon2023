#!/bin/bash

# root read only
chmod 400 Ben-key-pair.pem

# connect to server via ssh
ssh -i Ben-key-pair.pem "ubuntu@ec2-18-198-4-32.eu-central-1.compute.amazonaws.com"

# clone git repo
git clone https://github.com/BenSiv/LingoChat_ITC_Hackathon2023.git

# installing mysql
sudo apt install mysql-server
sudo apt install mysql-client

# connecting to mysql server
sudo mysql --user root

# from remote
mysql --user root --host "ubuntu@ec2-18-198-4-32.eu-central-1.compute.amazonaws.com"