from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World!"

@app.route("/druga")
def druga():
    return 'Druga podstrona (widok)'

@app.route('/trzecia')
def trzecia():
    return 'Trzeci widok.'

@app.route('/template')
def html_template():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
