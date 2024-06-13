from flask import Flask, render_template
app = Flask(__name__)

posts = [
    {
      'name':"jeo felix",
      'work':"coding",
      'start_date':"2022,nowember 18"
      
    },
    {
        'name':"albert",
      'work':"coding",
      'start_date':"2022,nowember 10"
      
    }
]

@app.route('/')
def hello_name():
    return render_template("index.html",posts=posts)

@app.route('/about')
def about():
    return "<h1>about page</h1>"

if __name__ =="__main__":
    app.run(debug = True)


