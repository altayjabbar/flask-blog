#!/bin/bash

# Build Docker image
sudo docker build -t flask-app .

# Run Docker container
sudo docker run -d -p 5000:5000 flask-app
