## Accessing Flask API
### Docker Compose
```bash
# Step 1: Navigate to the app directory
cd Stat-418-Project/docker_model_api

# Step 2: Start the container
docker-compose up -d

Basic Request Run:
curl -X POST https://model-app-594837701038.us-west1.run.app/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Hunger Games",
    "k": 5
  }'

To have a cleaner output can run:
curl -s -X POST https://model-app-594837701038.us-west1.run.app/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Hunger Games",
    "k": 5
  }' | jq

may need to install jq with: brew install jq (on macOS)

To stop and clean up:
docker-compose down
```
