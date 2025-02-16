
# Install Flask and Gunicorn
echo "Installing Flask and Gunicorn..."
pip install flask gunicorn

# Create project structure
echo "Setting up Flask project..."
mkdir -p templates

# Create app.py
cat > app.py <<EOF
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
EOF

# Create index.html
cat > templates/index.html <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello World</title>
    <style>
        body {
            background-color: #121212;
            color: #ffffff;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        h1 {
            font-size: 3rem;
        }
    </style>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>
EOF

# Run the Flask app
echo "Starting Flask app..."
flask run --host=0.0.0.0 --port=5000
