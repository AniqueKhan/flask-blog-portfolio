from flask import url_for,current_app
import secrets 
import os
from PIL import Image
from flask_mail import Message

from flaskblog import mail

def send_reset_email(user):
    # Getting the reset token by the custom method in the model User
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                    sender='noreply@demo.com',
                    recipients=[user.email])
    msg.body=f'''To reset your password , visit the following link:
{url_for('users.reset_token',token=token,_external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

def save_picture(pic):
    # Changing the name of the file to a random hex 
    # because we dont want the file to collide with the file we already have in our pp folder
    random_hex = secrets.token_hex(8)
    _ , file_extension = os.path.splitext(pic.filename)
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(current_app.root_path,'static/profile_pics',picture_filename)

    # Changing the size of the pictures to 125x125 
    # So it takes less space in the db
    output_size = (125,125)
    i = Image.open(pic)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_filename