import os

from flask import Flask

from extensions import db
from routes.admin import admin_bp
from routes.auth import auth_bp
from routes.main import main_bp
from routes.staff import staff_bp
from routes.user import user_bp
from seed import seed_admin, seed_sample_data
from utils import current_user

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'trekking.db')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key-change-me'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    os.makedirs(os.path.join(BASE_DIR, 'instance'), exist_ok=True)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(user_bp)

    @app.context_processor
    def inject_user():
        return {'current_user': current_user()}

    with app.app_context():
        db.create_all()
        seed_admin()
        seed_sample_data()

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)