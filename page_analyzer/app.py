import os
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
)
load_dotenv()

BASE_DIR = os.path.dirname(__file__)        # если файл в page_analyzer — ok
template_dir = os.path.join(BASE_DIR, 'templates')
app = Flask(__name__, template_folder=template_dir)

print('HUI', template_dir)

DATABASE_URL = os.getenv('DATABASE_URL')
print("kakashka")

@app.route('/')
def index():
    print("piska")
    return render_template('index.html')

@app.route('/urls_get')
def urls_get():
    print("piska + 1")
    return "pisechka"

if __name__ == '__main__':
    app.run(debug=True)
