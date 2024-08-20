from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulação de banco de dados
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
        image_url = request.form['image_url']
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
        post['image_url'] = request.form['image_url']
        return redirect(url_for('index'))
    return render_template('edit_post.html', post=post, post_id=post_id)

@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    posts.pop(post_id, None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)





