from flask import Flask
from routes.homepage import home_page

app = Flask(__name__, static_folder='static', static_url_path='')

app.register_blueprint(home_page)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)