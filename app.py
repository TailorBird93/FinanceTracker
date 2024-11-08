from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, Finance Tracker!'

if __name__ == '__main__':
    app.run(debug=True)