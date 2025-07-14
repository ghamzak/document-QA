# Docker Compose Setup Guide for RAG PDF Chatbot

This guide explains how to set up and run the RAG PDF Chatbot project using Docker Compose.

---

## Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed
- Your OpenAI API key for LLM features

---

## 1. Clone the Repository
```sh
git clone <your-repo-url>
```

## 2. Configure Environment Variables
Create a `.env` file in the project root (if not present):
```
FLASK_ENV=development
SECRET_KEY=your-secret-key
OPENAI_API_KEY=sk-...  # Your OpenAI API key
```

---

## 3. Build and Start the Services
From the project root, run:
```sh
docker-compose build --no-cache
docker-compose up
```
- This will build the app and start all services (Flask app, Prometheus, Grafana, Loki).

---

## 4. Access the Services
- **App:** [http://localhost:5050](http://localhost:5050)
- **Prometheus:** [http://localhost:9090](http://localhost:9090)
- **Grafana:** [http://localhost:3000](http://localhost:3000) (default user: admin / admin)
- **Loki:** [http://localhost:3100](http://localhost:3100)

---

## 5. Stopping the Services
Press `Ctrl+C` in the terminal running Docker Compose, or run:
```sh
docker-compose down
```

---

## 6. Troubleshooting
- If you change code, rebuild with `docker-compose build --no-cache`.
- If you see port conflicts, make sure nothing else is running on ports 5050, 9090, 3000, or 3100.
- For logs, use:
  ```sh
  docker-compose logs app
  ```
- For more help, see the main `README.md` or `SETUP.md` in the `docs/` directory.

---

Enjoy your RAG PDF Chatbot with full observability!
