## Accessing Flask API
### Deployed Through Google Cloud Run

```bash
Basic Request Run:
curl -X POST https://model-app-594837701038.us-west1.run.app/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Hunger Games",
    "k": 5
  }'

note you can add any title or k that you want this is just an example

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
Example output:
<img width="562" alt="image" src="https://github.com/user-attachments/assets/c1e001f0-7ddd-4ebc-935e-53d168416bec" />


