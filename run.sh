#!/bin/bash

containers=$(docker container ls -a -q)
images=$(docker image ls -a -q)

docker container kill $containers
docker container rm $containers
docker image rm $images

read -p "Build/run new instance? [y/n] " run_app
if [$run_app = y]
then
	docker build --name jobfinder .
	docker run -d -p 5000:5000 jobfinder
fi

docker ps


