# ⚽ FIFA World Cup 2026 — Enterprise AI Analytics & Simulator

An autonomous AI sports analyst and match simulator built for the expanded **48-team, 104-match** 2026 FIFA World Cup. This full-stack application utilizes **Google Cloud Run**, **PostgreSQL with `pgvector`**, and **Google Gemini** to allow users to ask tactical questions and simulate match outcomes based on the upcoming tournament format.

---

## 🏗️ Architecture & Features

This project bridges real-world sports data with a production-ready cloud architecture:

- **Interactive AI Analyst:** A Streamlit dashboard where users can query an AI agent about tournament rules (like the new 12-group format and the introduction of the Round of 32) or team statistics.
- **Predictive Match Simulation:** A custom Python algorithm (`simulator.py`) that calculates win/draw/loss probabilities using dynamic attack and defense multipliers. *Note: Standings are static based on initial data to preserve baseline accuracy during hypothetical simulations.*
- **Vector Database (RAG):** Uses `pgvector` on Google Cloud SQL to index tactical news reports, allowing the Gemini model to retrieve relevant, factual context before answering user questions.
- **Serverless Deployment:** Fully containerized backend (FastAPI) and frontend (Streamlit) deployed on **Google Cloud Run**, with secure communication to Cloud SQL via IAM service accounts and Unix sockets.

---

## 🛠️ Technology Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Backend:** FastAPI (Python 3.10+)
- **Database:** PostgreSQL on Google Cloud SQL (with `pgvector` & `psycopg` v3)
- **AI Engine:** Google `gemini-3.5-flash` via LangChain
- **Infrastructure:** Docker, Docker Compose, Google Cloud Platform (GCP)

---

## 🚀 Quick Start Guide (Local Setup)

To run this project on your local machine, you will use Docker Compose to spin up the complete infrastructure, including a local PostgreSQL instance.

### 1. Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- A **Google Gemini API Key** (Get one from Google AI Studio).

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/fifa-ai-simulator.git
cd fifa-ai-simulator
```

### 3. Set Environment Variables

Create a `.env` file in the root directory and add your API key:

```
GOOGLE_API_KEY=your_api_key_here
```

### 4. Build and Start the Containers

Run the following command to build the frontend, backend, and database images:

```bash
docker-compose up --build -d
```

### 5. Seed the Database

Wait a few seconds for PostgreSQL to initialize, then populate the 48 World Cup teams and tactical news reports into the database:

```bash
docker-compose exec backend python src/init_db.py
docker-compose exec backend python src/seed_db.py
```

### 6. Access the Application

Open your browser and navigate to: `http://localhost:8501`

---

## ☁️ Google Cloud Deployment Notes

If you are trying to replicate the cloud architecture, please note the following DevOps configurations were required:

1. **Cloud SQL Auth Proxy:** Required for local-to-cloud database connections during development.
2. **Driver Compatibility:** The Cloud Run deployment environment requires the `postgresql+psycopg://` dialect prefix in the `DATABASE_URL` for `psycopg3` compatibility.
3. **IAM Permissions:** The Compute Engine default service account (`[PROJECT_NUMBER]-compute@developer.gserviceaccount.com`) must be granted the `roles/cloudsql.client` role to prevent `Connection refused` socket errors.

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
