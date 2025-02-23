# app.py
from flask import Flask, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config.update(
        SECRET_KEY=os.getenv('SECRET_KEY', os.urandom(24)),
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=1800,  # 30 minutes
    )

    # Handle proxy headers
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Set up logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Application startup')

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    # Routes
    @app.route('/')
    def index():
        app.logger.info('Index page accessed')
        return render_template('index.html', title='Welcome')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))