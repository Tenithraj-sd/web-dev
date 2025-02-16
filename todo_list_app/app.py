from flask import Flask, render_template, request, redirect
import psycopg2
from urllib.parse import urlparse

app = Flask(__name__)

# Database Connection String
# DATABASE_URL = 'postgresql://web:VUgydDpJ1NCK14RYy4AUPTifXKewEy6w@dpg-cuolj8lds78s738m3etg-a/notes_zb32'
DATABASE_URL = 'postgresql://web:VUgydDpJ1NCK14RYy4AUPTifXKewEy6w@dpg-cuolj8lds78s738m3etg-a.oregon-postgres.render.com/notes_zb32'

# Function to Connect to Database
def get_db_connection():
    result = urlparse(DATABASE_URL)
    return psycopg2.connect(
        database=result.path[1:],  # Removes leading '/'
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )

# Initialize Database (Run Once)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Route: Show All Tasks
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY id ASC")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Route: Add Task
@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    if task:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task) VALUES (%s)", (task,))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect('/')

# Route: Mark Task as Completed
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = TRUE WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

# Route: Delete Task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

# Run the App
if __name__ == '__main__':
    init_db()  # Run this once to create the table
    app.run(debug=True)
