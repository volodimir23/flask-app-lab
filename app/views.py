from flask import Flask, request, redirect, url_for, render_template, abort, current_app


@current_app.route('/')
def home():
    return render_template('hello.html')

@current_app.route('/homepage')
def homepage():
    """View for the Home page of your website."""
    agent = request.user_agent
    return f"<h1>This is your homepage :) - {agent}</h1>"

@current_app.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме')

@current_app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
