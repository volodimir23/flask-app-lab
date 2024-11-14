from flask import request, redirect, url_for, render_template, flash, session, make_response

from app.users import user_bp


@user_bp.route('/hi/<string:name>')
def greetings(name):
    name = name.upper()
    age = request.args.get('age', 0, type=int)
    return render_template('hi.html', name=name, age=age)

@user_bp.route('/admin')
def admin():
    to_url = url_for("user.greetings", name="administrator", age=45, _external=True)
    return redirect(to_url)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin':
            flash('Ви увійшли в систему', 'success')
            session['username'] = username
            return redirect(url_for('user.get_profile'))
        else:
            flash('Помилку входу в систему', 'danger')
            return redirect(url_for('user.login'))
    return render_template('login.html')

@user_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('user.get_profile'))

@user_bp.route('/profile')
def get_profile():
    if 'username' not in session:
        flash('Спочатку увійдіть в систему', 'danger')
        return redirect(url_for('user.login'))
    cookies = request.cookies
    return render_template('profile.html', cookies=cookies)

@user_bp.route('/set_cookie', methods=['POST'])
def set_cookie():
    key = request.form.get('cookie_key')
    value = request.form.get('cookie_value')
    expire = int(request.form.get('cookie_time'))
    response = make_response(redirect(url_for('user.get_profile')))
    response.set_cookie(key, value, max_age=expire)
    flash('Кукі додано', 'success')
    return response

@user_bp.route('/remove_cookie', methods=['POST'])
def remove_cookie():
    key = request.form.get('cookie_key')
    response = make_response(redirect(url_for('user.get_profile')))
    if key:
        response.set_cookie(key, '', expires=0)
    else:
        for cookie in request.cookies:
            response.set_cookie(cookie, '', expires=0)
    flash('Кукі видалено', 'success')
    return response

@user_bp.route('/toggle_theme')
def toggle_theme():
    theme = session.get('theme', 'light')
    new_theme = 'dark' if theme == 'light' else 'light'
    session['theme'] = new_theme
    return redirect(url_for('user.get_profile'))
