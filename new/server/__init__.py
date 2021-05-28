from flask import Flask

def create_app():
    app = Flask(__name__,static_folder="assets")

    app.config['SECRET_KEY'] = '6S\xb3\xdeF\xf1\x92Be0\x9e;\x90\xf9\x81\xa2d\x8c\x17i\xca6\x1e\xbc\xa1\x07\t\xa4\xd5\xac+\x95>\xcf\xcaf&Y\xbe\x11Ti\x05\xc8\x9f\xd3O\x9du\xff(Y\xadV\xa5\x19\xddd?!\xb7\xf7\xefl'

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main__blueprint
    app.register_blueprint(main__blueprint)

    return app