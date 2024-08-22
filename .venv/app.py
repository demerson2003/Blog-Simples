from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('.venv', 'static', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Garante que o diretório de uploads existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Simulação de um banco de dados com um dicionário
posts = {}

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = posts.get(post_id)
    return render_template('post.html', post=post)

@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = url_for('static', filename=f'uploads/{filename}')
        else:
            image_url = ''  # Se não houver imagem ou a extensão não for permitida
        
        post_id = len(posts) + 1
        posts[post_id] = {'title': title, 'body': body, 'image_url': image_url}
        return redirect(url_for('index'))
    return render_template('new_post.html')

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = posts.get(post_id)
    if request.method == 'POST':
        post['title'] = request.form['title']
        post['body'] = request.form['body']
        
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            post['image_url'] = url_for('static', filename=f'uploads/{filename}')
        
        return redirect(url_for('index'))
    return render_template('edit_post.html', post=post, post_id=post_id)

@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    posts.pop(post_id, None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)











