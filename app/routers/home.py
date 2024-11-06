from flask import Blueprint, jsonify, request, redirect, url_for  # Импортируем необходимые модули из Flask

home_bp = Blueprint('home', __name__, url_prefix='/')

@home_bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        return redirect(url_for('greet_user', name=name))
    return '''
        <h2>Welcome to the home page!</h2><h1>Hello, Flask!</h1>
        <form method="post">
            <label for="name">Enter your name:</label>
            <input type="text" id="name" name="name" required>
            <input type="submit" value="Submit">
        </form>
    '''
