from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

import os
import psycopg2
from urllib.parse import urlparse

# Load DATABASE_URL from environment variables
DATABASE_URL = 'postgresql://web:VUgydDpJ1NCK14RYy4AUPTifXKewEy6w@dpg-cuolj8lds78s738m3etg-a.oregon-postgres.render.com/notes_zb32'
#"postgresql://postgres:7777@db.jbabxxrvperqfuermkwn.supabase.co:5432/postgres"

def get_db_connection():
    result = urlparse(DATABASE_URL)

    return psycopg2.connect(
        database=result.path[1:],  # Removes leading '/'
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        note_content = request.form["content"]
        cur.execute("INSERT INTO notes (content) VALUES (%s)", (note_content,))
        conn.commit()

    cur.execute("SELECT * FROM notes ORDER BY id DESC")
    notes = cur.fetchall()

    cur.close()
    conn.close()
    return render_template("index.html", notes=notes)

@app.route("/delete/<int:note_id>", methods=["POST"])
def delete(note_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM notes WHERE id = %s", (note_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
