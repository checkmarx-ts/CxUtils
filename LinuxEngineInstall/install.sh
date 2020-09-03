#!/bin/bash

#install instructions from 
#https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html

echo "installing docker based on https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html and making it so you can run docker without sudo"
yum update -y
amazon-linux-extras install docker
sudo service docker start 
sudo usermod -a -G docker ec2-user
docker info
