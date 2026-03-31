import os
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


if __name__ == '__main__':
    app.run(debug=True)
