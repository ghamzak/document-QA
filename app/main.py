from app import create_app
import argparse

app = create_app()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the RAG PDF Chatbot Flask app.")
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on (default: 5000)')
    args = parser.parse_args()
    app.run(debug=True, host='0.0.0.0', port=args.port)
