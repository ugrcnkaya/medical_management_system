from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    data = request.form
    print(data)
            #text = argument to send towards the template
    return render_template("login.html", boolean= False)

@auth.route('/logout')
def logout():
    return '<p>Logout</p>'

@auth.route('/sign_up', methods= ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email)  < 4:
            flash('E-Mail must be greater than 3 characters.', category='error')
            pass
        elif len(firstName) < 2:
            flash('First name must be greater than 1 characters.', category='error')
            pass
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
            pass
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
            pass
        else:
            flash('User is created.', category='success')

            # add user to the database
    return render_template("sign_up.html")


