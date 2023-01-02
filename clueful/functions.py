import numpy as np
import random
from PIL import Image
import secrets
import os
from flask_login import current_user
from clueful import app, db, mail, email_confirmation_Serializer
from flask_mail import Message
from flask import url_for

def sendToken(email,reason):
    if reason == 'verify':
        token = email_confirmation_Serializer.dumps(email,salt='email-confirm')
        msg = Message('Clueful email verification', sender='clueful_puzzles@gmail.com',recipients=[email])
        link = url_for('confirm_email', token = token, _external = True)
        msg.body = 'Verify your email-address now by clicking the following link: {}'.format(link)
    elif reason == 'change_password':
        token = email_confirmation_Serializer.dumps(email,salt='change-password')
        msg = Message('Clueful change password', sender='clueful_puzzles@gmail.com',recipients=[email])
        link = url_for('change_password', token = token, _external = True)
        msg.body = 'Change your password by clicking the following link: {}'.format(link)
    mail.send(msg)

def createUserImage():
    rand_red = random.randint(100,255)
    rand_green = random.randint(100,255)
    rand_blue = random.randint(100,255)
    dimension_small = 11
    array_small = np.zeros([dimension_small,dimension_small,  3], dtype=np.uint8)
    for pixel_x in range(dimension_small):
        for pixel_y in range(dimension_small):
            rand_num_red = random.uniform(.9, 1.1)
            rand_num_green = random.uniform(.9, 1.1)
            rand_num_blue = random.uniform(.9, 1.1)
            rand_red = 255 if rand_num_red * rand_red > 255 else rand_num_red * rand_red
            rand_green = 255 if rand_num_green * rand_green > 255 else rand_num_green * rand_green
            rand_blue = 255 if rand_num_blue * rand_blue > 255 else rand_num_blue * rand_blue
            for color in [rand_red,rand_green,rand_blue]:
                if color > 255.:
                    color = 255.
            array_small[pixel_x,pixel_y]=[int(rand_red),int(rand_green),int(rand_blue)]
            #print([int(rand_red),int(rand_green),int(rand_blue)])
    
    
    empty = [[0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0]]       
            
    img0 = [[0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,1,0,0],
            [0,0,1,0,1,0,1,0,1,0,0],
            [0,0,1,1,1,1,1,1,1,0,0],
            [0,0,0,1,0,1,0,1,0,0,0],
            [0,0,0,0,1,1,1,0,0,0,0],
            [0,0,0,0,1,1,1,0,0,0,0],
            [0,0,0,1,0,1,0,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0]]
    
    img1 = [[0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,1,1,1,0,0,0],
            [0,0,0,1,1,1,1,1,1,0,0],
            [0,0,1,1,1,0,0,1,1,0,0],
            [0,0,1,1,0,0,0,0,1,0,0],
            [0,0,1,1,1,0,1,0,1,0,0],
            [0,0,0,1,1,1,1,0,0,0,0],
            [0,0,0,0,1,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0]]
    
    img2 = [[0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,1,1,1,1,0,0,0],
            [0,0,1,1,1,1,1,1,1,0,0],
            [0,0,1,0,0,1,0,0,1,0,0],
            [0,0,1,1,0,1,0,1,1,0,0],
            [0,0,1,1,1,0,1,1,1,0,0],
            [0,0,1,1,0,0,0,1,1,0,0],
            [0,0,0,1,0,1,0,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0]]  
    
    img3 = [[0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,1,0,0,0],
            [0,0,1,0,0,0,0,0,1,0,0],
            [0,0,1,1,1,1,1,1,1,0,0],
            [0,0,0,1,1,1,1,1,0,0,0],
            [0,0,0,0,1,1,1,0,0,0,0],
            [0,0,0,0,1,1,1,0,0,0,0],
            [0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0]]  
    
    img4 = [[0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,0,1,0,0,0,0,0],
            [0,0,1,1,1,0,1,0,0,0,0],
            [0,0,0,1,1,1,0,0,0,0,0],
            [0,0,1,0,1,1,0,1,1,0,0],
            [0,0,0,1,0,1,0,1,1,0,0],
            [0,0,0,0,0,1,0,0,1,0,0],
            [0,0,0,0,0,0,1,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0]]  
    
    images = [empty,img0,img1,img2,img3,img4]
    
    start_color = 20
    
    for ind1, x in enumerate(images[random.randint(0,4)]):
        for ind2, y in enumerate(x):
            if y == 1:
                array_small[ind1,ind2] = [start_color, start_color, start_color]
                start_color += 2
    

    return array_small.tolist()

def enlargeUserImage(image_small):
    array_small = np.array(image_small)
    dimension_large = 150
    array_large = np.zeros([dimension_large,dimension_large,  3], dtype=np.uint8)
    
    resize_factor = dimension_large / 11
    for pixel_x in range(dimension_large):
        for pixel_y in range(dimension_large):
            #print(image_small[int(pixel_x/resize_factor),int(pixel_y/resize_factor)])
            array_large[pixel_x,pixel_y]=array_small[int(pixel_x/resize_factor),int(pixel_y/resize_factor)]
            pass

    square_img = Image.fromarray(array_large, mode="RGB")
    return square_img

def saveUserImage(image):
    image_small = image
    image_large = enlargeUserImage(image_small)
    random_hex = secrets.token_hex(8)
    picture_fn = random_hex + '.jpg'
    picture_path = os.path.join(app.root_path, 'static/img/profile_pics', picture_fn)
    image_large.save(picture_path)
    current_user.image_file = picture_fn
    current_user.image_values = str(image_small)
    db.session.commit()
    return picture_fn

def is_int(value):
  try:
    int(value)
    return True
  except:
    return False