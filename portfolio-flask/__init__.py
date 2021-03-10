from flask import Flask, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

import json
import os
from datetime import datetime

app = Flask(__name__)

app.secret_key = "Aman@1234#"

## ---------- Import sensitive credentials from config.json file --------- ##
dir_path = os.path.dirname(os.path.realpath(__file__))
config_file_path = dir_path + '/config.json'

with open(config_file_path, 'r') as c:
    params = json.load(c)["params"]

## -------------------- database connection -------------------------- ##

if params["local_server"]:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["prod_uri"]

db = SQLAlchemy(app)

## ------------------------ Mail Configuration ------------------------------ ##
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
#
# msg = MIMEMultipart()
# msg.set_unixfrom('author')

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['mail_username'],
    MAIL_PASSWORD=params['mail_password']
)

mail = Mail(app)

## ------------------------- connecting to database tables ------------------------------ ##
class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(50), nullable=False)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/post", methods=["POST"])
def post():

    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')
        date = datetime.now()
        # print(name, email, subject, message)
        flash("Your message has been sent. Thank you!")
        entry = Contact(name=name, email=email, phone=phone, subject=subject, message=message, date=date)
        db.session.add(entry)
        db.session.commit()

        # msg['From'] = email
        # msg['To'] = params["mail_username"]
        # msg['Subject'] = subject
        # message = message
        # msg.attach(MIMEText(message))
        # # print(msg)
        #
        # mailserver = smtplib.SMTP(params["mail_server"], params["mail_port"])
        # mailserver.ehlo()
        # mailserver.starttls()
        # mailserver.ehlo()
        # mailserver.login(params["mail_username"], params["mail_password"])
        # response = mailserver.sendmail(email, params["mail_username"], msg.as_string())
        # mailserver.quit()

        mail.send_message(
            subject="New Message from " + name,
            sender=email,
            recipients=[params["mail_username"], ],
            body=message + '\n' + phone + '\n' + email
        )

        return redirect("/")
    else:
        return render_template("index.html")
    # return "Your message has been sent."

if __name__ == '__main__':
    app.run(debug=True)