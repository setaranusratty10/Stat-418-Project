## Accessing the App

**NOTE:** The app is currently deployed on Google Cloud Run. If you'd like to run the app locally or reproduce the setup, follow the instructions below.

### 🔗 Live App (Cloud Run)
[Click here to launch the app]([https://your-cloud-run-url.com](https://shiny-app-594837701038.us-west1.run.app/))

---

## 🧪 Running the App Locally / Reproducing the Project

You can run this app locally in two ways:  
1. Using **Python Shiny + virtual environment** (ideal for development)  
2. Using **Docker Compose** (ideal for reproducibility or deployment testing)

---

### Option 1: Python Virtual Environment (Recommended for Development)

```bash
# Step 1: Navigate to the app directory
cd Stat-418-Project/docker_files

# Step 2: Set up a virtual environment
python3 -m venv venv
source venv/bin/activate     # (Windows: .\venv\Scripts\activate)

# Step 3: Install dependencies
pip install -r requirements

# Step 4: Launch the app
python3 -m shiny run --reload app.py

Once the app is running, open your browser and visit:
http://localhost:8000
```

### Option 2: Docker Compose
```bash
# Step 1: Navigate to the app directory
cd Stat-418-Project/docker_files

# Step 2: Start the container
docker-compose up
```

Once the app is running, open your browser and visit:
http://localhost:8000

To stop and clean up:
```bashdocker-compose down```

