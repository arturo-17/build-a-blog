from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-blog-done:soccer1990@localhost:8889/get-blog-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'dgfstGsfS'

class Blog(db.Model):

    blog_id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    blog_content = db.Column(db.String(120))

    def __init__(self, blog_title, blog_content):
        self.blog_title = blog_title
        self.blog_content = blog_content

@app.route('/blog', methods=['POST', 'GET'])
def index():

    if request.args:
        blog_id = request.args.get('id')
        post = Blog.query.get(blog_id)
        return render_template('post.html', post=post)
    
    if request.method == 'POST':
        blog_title = request.form['blog_entry_title']
        blog_content = request.form['blog_entry_content']

        if not blog_title or not blog_content:
            flash('Please fill in', 'its wrong')
            return render_template('newpost.html')
        else:
            new_post = Blog(blog_title, blog_content)
        
            db.session.add(new_post)
            db.session.commit()

            new_post = Blog.query.filter_by(blog_title=blog_title).first()

            
            return redirect('/blog?id=' + str(new_post.blog_id))

    posts = Blog.query.all()
    return render_template('blog.html', posts=posts)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    return render_template('newpost.html')

if __name__ == '__main__':
    app.run()

