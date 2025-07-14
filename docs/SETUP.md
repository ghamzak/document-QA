# RAG PDF Chatbot - Setup & Usage Guide

## Prerequisites
- Python 3.9+
- pip
- (Recommended) virtualenv or venv
- Docker & Docker Compose (optional, for observability stack)

## 1. Clone the Repository
```
git clone <your-repo-url>
```

## 2. Create and Activate a Virtual Environment
```
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install Python Dependencies
```
pip install -r requirements.txt
```

## 4. Set Up Environment Variables
Create a `.env` file in the project root (if not present):
```
FLASK_ENV=development
SECRET_KEY=your-secret-key
OPENAI_API_KEY=sk-...  # Your OpenAI API key
```

## 5. Run the App
```
cd app
python -m main
```
The app will be available at http://localhost:5050

## 6. Using the App
- Upload a PDF document.
- Wait for processing (progress bar will show status).
- Select the document from the dropdown.
- Ask questions in the chatbot tab.
- See latency and LLM model info after each answer.
- Use the "Clear Chat" button to reset the chat history.

## 7. Observability (Optional)
To enable monitoring with Prometheus, Grafana, and Loki:
```
docker-compose up
```
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (default user: admin / admin)
- Loki: http://localhost:3100

## 8. Testing
```
pytest
```

## 9. Troubleshooting
- Ensure your OpenAI API key is valid and has access to the required models.
- If you change code, restart the Flask server.
- For issues with Docker, ensure Docker Desktop is running.

## 10. Project Structure
See the main `README.md` for a directory overview.

---
For more details, see the code comments and PRD in `prd.md`.
