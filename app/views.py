from flask import Flask, request, redirect, url_for, render_template, abort
from . import app


@app.route('/')
def home():
    return render_template('hello.html')

@app.route('/homepage')
def homepage():
    """View for the Home page of your website."""
    agent = request.user_agent
    return f"<h1>This is your homepage :) - {agent}</h1>"

@app.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме')
