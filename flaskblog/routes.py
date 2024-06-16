from flask import  render_template, url_for,flash,redirect
from flaskblog import app
from flaskblog.forms import registrationForm,LoginForm
from flaskblog.models import User,Post


posts = [
    {
      'author':"jeo felix",
      'title':"coding",
      'date_posted':"2022,nowember 18"
      
    },
    {
        'author':"jeo felix",
      'title':"coding",
      'date_posted':"2022,nowember 18"
    
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html",posts=posts)

@app.route('/about')
def about():
    return render_template("about.html",title='About')

@app.route('/register',methods=["GET","POST"])  
def register():
    form = registrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!",'success')
        return redirect(url_for('home'))   
    flash(f"Account not created for !",'error')
    
    return render_template("register.html",title='Register',form = form)

@app.route('/login',methods=["GET","POST"])  
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@block.com' and form.password.data == 'password':
            flash("You have been logged in!",'success')
            return redirect(url_for('home'))
        else:
            flash('Log in Unsuccessful.Please check username and password','danger')
    return render_template("login.html",title='Login',form = form)