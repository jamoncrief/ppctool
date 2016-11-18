from app import app
from flask import render_template, flash, redirect
from .forms import LoginForm



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/')
    return render_template('login.html', 
                           title='Sign In',
                           form=form,
						    providers=app.config['OPENID_PROVIDERS'])
							

@app.route('/')
def home():
    user = {'nickname': 'Miguel'}  # fake user
    posts = [  # fake array of posts
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template("home.html",
                           title='Home',
                           user=user,
                           posts=posts)
if __name__ == '__main__':
    app.run(debug=True)
