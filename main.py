from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-blog-done:soccer1990@localhost:8889/get-blog-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'dgfstGsfS'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text(2000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)

@app.route('/blog')
def blog():

    if request.args:
        id = request.args.get('id')
        blog = Blog.query.get(id)
        return render_template('post.html', blog=blog, id=id)

    else:
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs) 

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    
    if request.method == 'GET':
        return render_template('newpost.html')

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if len(title) == 0 or len(body) == 0:
            flash('Please fill in both title and body', 'error')
            return redirect('newpost')
        
        if len(title) > 0 and len(body) > 0:
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog?id=' + str(new_post.id))
       
    #return render_template('single_post.html', blog=blog)


if __name__ == '__main__':
    app.run()