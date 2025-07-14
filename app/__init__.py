from flask import Flask
from flask_cors import CORS
import os

def create_app():

    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'app', 'static', 'uploads')
    app.secret_key = os.environ.get('SECRET_KEY', 'dev')
    CORS(app)

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from .routes.upload import upload_bp
    from .routes.chat import chat_bp
    from .routes.progress import progress_bp
    app.register_blueprint(upload_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(progress_bp)

    return app
