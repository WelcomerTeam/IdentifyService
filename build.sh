echo "docker build and push"
docker build --tag 1345/identify-service:latest .
docker push 1345/identify-service:latest