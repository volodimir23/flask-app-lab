from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/homepage')
def homepage():
    """View for the Home page of your website."""
    agent = request.user_agent
    return f"<h1>This is your homepage :) - {agent}</h1>"

@app.route('/hi/<string:name>/')
def greetings(name):
    name = name.upper()
    age = request.args.get('age', 0, type=int)
    return f"Welcome {name=} {age=}", 200

@app.route('/admin')
def admin():
    to_url = url_for("greetings", name="administrator", _external=True)
    return redirect(to_url)

@app.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме')


if __name__ == '__main__':
    app.run(debug=True)
