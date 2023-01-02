from flask import flash, redirect, url_for
from clueful import socket, db, app
from clueful.models import HideFlash, Riddles, RiddleData, User
from clueful.functions import saveUserImage
from flask_login import current_user
from flask import render_template
from clueful.functions import createUserImage, enlargeUserImage
from PIL import Image
import os
import secrets
from datetime import datetime, timedelta



# 01 DON NOT SHOW AGAIN #
@socket.on('dont_show_again')
def dont_show_again(flashID):
    flashID = flashID.replace('alert__close-btn_', '')
    if not HideFlash.query.filter_by(user_id = current_user.id, flash_id = flashID).first():
        hide_flash_data = HideFlash(user_id = current_user.id, flash_id = flashID)
        db.session.add(hide_flash_data)
        db.session.commit()


# 02 SAVE USER IMAGE #
@socket.on('saveUserImage')
def saveImage(image):
    saveUserImage(image)
    socket.emit('reload')
    #return picture_fn    


# 03 CHECK ANSWER #
@socket.on('correctAnswer')
def check_answer(data):
    game_id = data['game_id']
    #Check if id of url exists

    if Riddles.exists(str(game_id)):
        #Load User_data of Game
        user_game_data = RiddleData.query.filter_by(user_id = current_user.id, riddle_id = game_id).first()
        if user_game_data.points <= 0:
            user_game_data.datetime_end = datetime.now()
            user_game_data.final_time = round((user_game_data.datetime_end - user_game_data.datetime_start).total_seconds())
            points=int(1000 * 0.985 ** (user_game_data.final_time / 60)) if int(1000 * 0.985 ** (user_game_data.final_time / 60)) >= 1 else 1
            user_game_data.points = points
            #update user totalpoints
            RiddleData.update_total_points()
            db.session.commit()
            socket.emit('riddle_data_saved')
        else:
            #socket.emit('riddle_data_saved')
            socket.emit('redirect', {'url': url_for('home')})
    else:
        socket.emit('redirect', {'url': url_for('home')})

    

# 04 PUZZLE RATING #
@socket.on('riddle_rating')
def riddle_rating(data):
    riddle_rating = data['riddle_rating']
    riddle_id = data['game_id']
    
    user_game_data = RiddleData.query.filter_by(user_id = current_user.id, riddle_id = riddle_id).first()
    #Check if the riddle was rated yet by the current user
    if RiddleData.not_rated_yet(riddle_id):
        if not current_user.is_admin:
            user_game_data.rating = riddle_rating    
            riddle_data = Riddles.query.filter_by(id=riddle_id).first()
            number_of_ratings = riddle_data.number_of_ratings
            sum_of_ratings = riddle_data.sum_of_ratings
            riddle_data.number_of_ratings = number_of_ratings + 1
            riddle_data.sum_of_ratings = sum_of_ratings + riddle_rating
            riddle_data.rating = (sum_of_ratings + riddle_rating)/(number_of_ratings + 1)
            db.session.commit()
        socket.emit('redirect', {'url': url_for('home')})
    else:
        socket.emit('redirect', {'url': url_for('home')})

# 05 UPDATE RIDDLE START TIME #        
@socket.on('updateTimeData')
def updateTimeData(data):
    
    riddle_id = data['game_id']
    current_time = RiddleData.query.filter_by(user_id = current_user.id, riddle_id = riddle_id).first().datetime_start
    
    print(data['new_start_date'])
    print(current_time - timedelta(hours=0, minutes=30))
    RiddleData.query.filter_by(user_id = current_user.id, riddle_id = riddle_id).first().datetime_start = current_time - timedelta(hours=0, minutes=30)
    db.session.commit()
    
    


# 06 GET HINTS #
@socket.on('getHint')
def getHint(data):
    riddle_id = data['game_id']
    
    #Store used hint in DB
    hint_nr = data['hint_nr']
    if hint_nr == 1:
        RiddleData.query.filter_by(user_id = current_user.id, riddle_id = riddle_id).first().hint1_used = True
    elif hint_nr == 2:
        RiddleData.query.filter_by(user_id = current_user.id, riddle_id = riddle_id).first().hint2_used = True
    elif hint_nr == 3:
        RiddleData.query.filter_by(user_id = current_user.id, riddle_id = riddle_id).first().hint3_used = True
    db.session.commit()

    #get all hints to fetch
    riddle = Riddles.query.filter_by(id = riddle_id).first()
    hints = [riddle.hint1,riddle.hint2,riddle.hint3]

    data={'hint_nr':hint_nr,'hint_text':hints[int(hint_nr)-1]}
    socket.emit('receiveHint',data)
    



# 07 GET MUSIC STATUS #
@socket.on('getMusicStatus')
def getMusicStatus():
    data={'music_status':current_user.music_on}
    socket.emit('receiveMusicStatus',data)



# 08 SAVE MUSIC STATUS #
@socket.on('saveMusicStatus')
def saveMusicStatus(data):
    current_user.music_on = data['status']
    db.session.commit()