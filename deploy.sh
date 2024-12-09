aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin 833612282618.dkr.ecr.us-west-1.amazonaws.com
docker-compose build
docker-compose push
