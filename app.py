from flask import Flask, render_template
# from forms import registrationForm,LoginForm
app = Flask(__name__)

# app.confing['SECRET_KEY'] = '6ddc470b93ea6b43e950a0ad94121b27b17391a513b1c8d4'

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

# @app.route('/registr')  
# def register():
#     form = registrationForm()
#     return render_template(register.html,)

if __name__ =="__main__":
    app.run(debug = True)


