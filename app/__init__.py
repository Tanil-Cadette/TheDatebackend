from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
        app = Flask(__name__)
        
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
                "SQLALCHEMY_DATABASE_URI")
        
        from app.models.dates import Date
        from app.models.friends import Friend
        from app.models.user import User
        
        db.init_app(app)
        migrate.init_app(app, db)
        
        from .routes import friends_bp
        app.register_blueprint(friends_bp)
        
        from .routes import dates_bp
        app.register_blueprint(dates_bp)
        
        from .routes import recommendations_bp
        app.register_blueprint(recommendations_bp)
        
        from .routes import user_bp
        app.register_blueprint(user_bp)
        
        CORS(app)
        return app


