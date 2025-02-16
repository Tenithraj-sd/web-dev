from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from forms import ContactForm

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

mail = Mail(app)

@app.route("/", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        attachment = request.files['attachment']
        
        msg = Message("New Contact Form Submission", 
                      sender=app.config['MAIL_USERNAME'], 
                      recipients=[email])
        msg.body = f"From: {name} <{email}>\n\nMessage:\n{message}"
        
        if attachment:
            filename = secure_filename(attachment.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            attachment.save(filepath)
            with open(filepath, 'rb') as f:
                msg.attach(filename, attachment.content_type, f.read())
        
        mail.send(msg)
        flash("Message sent successfully!", "success")
        return redirect(url_for("success"))
    
    return render_template("contact.html", form=form)

@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
