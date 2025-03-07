from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

from urllib.parse import urlparse
DATABASE_URL = 'postgresql://web:VUgydDpJ1NCK14RYy4AUPTifXKewEy6w@dpg-cuolj8lds78s738m3etg-a/notes_zb32'

#DATABASE_URL = 'postgresql://web:VUgydDpJ1NCK14RYy4AUPTifXKewEy6w@dpg-cuolj8lds78s738m3etg-a.oregon-postgres.render.com/notes_zb32'
def connect_db():
    result = urlparse(DATABASE_URL)

    return psycopg2.connect(
        database=result.path[1:],  # Removes leading '/'
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
# Home Page - Show All Blog Posts
@app.route('/')
def index():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content FROM posts ORDER BY id DESC")
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', posts=posts)

# Add New Post
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

# Edit Post
@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute("UPDATE posts SET title=%s, content=%s WHERE id=%s", (title, content, post_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    # Fetch post details properly
    cursor.execute("SELECT id, title, content FROM posts WHERE id=%s", (post_id,))
    post = cursor.fetchone()

    if post is None:  # If the post does not exist
        return "Post not found", 404

    cursor.close()
    conn.close()
    return render_template('edit.html', post=post)

# Delete Post
@app.route('/delete/<int:post_id>')
def delete(post_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id=%s", (post_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080)

