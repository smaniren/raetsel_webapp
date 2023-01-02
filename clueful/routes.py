from uuid import SafeUUID
from flask import render_template, url_for, flash, redirect, request, Markup, jsonify
from clueful import app, db, bcrypt, mail, email_confirmation_Serializer, mail
from clueful.models import User, Riddles, RiddleData, HideFlash
from clueful.forms import SignupForm, LoginForm, EditFormUsername, EditFormEmail, EditFormPassword, ForgotPasswordForm, NewPasswordForm,SqlForm
from clueful.functions import createUserImage, saveUserImage, sendToken, is_int
from flask_login import login_user, current_user, logout_user, login_required
import pandas as pd
import secrets
import os
import ast
from PIL import Image
from datetime import datetime, time
from itsdangerous import SignatureExpired, BadTimeSignature, BadSignature

@app.route('/')
@app.route('/home')
@login_required
def home():
    data = {
        'top_ten' : User.get_top_ten(),
        'riddles' : Riddles.get_riddles()
        }
    
    
    """ for riddle in data['riddles']:
        
        print(item for sublist in riddle['riddle_fastest_player'] for item in sublist.split()) """
    #print(data['riddles'][0])
    #print(data['riddles'][0]['riddle_id'])
    markup = Markup(
        'id=rules\
        add_dsa \
        <h1 class="title">RULES</h1>\
            <ul>\
                <li>You may use your phone, the internet, tools, everything you can imagine to solve the puzzles.</li>\
                <li>You''re time is tracked from the first moment you enter a puzzle.</li>\
                <li>Once you entered a puzzle, you have to solve it to enter another puzzle.</li>\
                <li>Solving puzzles without any hints grants more points.</li>\
                <li>Every puzzle can only be solved once.</li>\
            </ul>\
            <p><strong>Good luck!</strong></p>')
    if not HideFlash.exists('rules'):
        flash(markup,'info')
    return render_template('index.html',data=data)

@app.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignupForm()
    if form.validate_on_submit():
        sendToken(form.email.data,'verify')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user_image = createUserImage()
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, image_file = saveUserImage(new_user_image), image_values = str(new_user_image))
        db.session.add(user)
        db.session.commit()
        flash(f'id=signup_success We just sent you an email. Please check your email account.','success')
        return redirect(url_for('login'))
    return render_template('signup.html', form = form)

@app.route("/confirm_email/<token>")
def confirm_email(token):
    try:
        email = email_confirmation_Serializer.loads(token, salt='email-confirm', max_age=1800)
    except SignatureExpired:
        sendToken(email,'verify')
        flash(f'id=email_token_expired Your token is expired. We just sent you a new token. Please check your email account','warning')
        return redirect(url_for('login'))
    except (BadTimeSignature,BadSignature):
        flash(f'id=email_token_invalid Your token is invalid. Please sign up one more time','warning')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=email).first()
    user.verified = 1
    db.session.commit()
    flash(f'id=email_token_valid Your account has been verified. Please log in!','success')
    return redirect(url_for('login'))

        
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data) and user.verified:
            login_user(user)
            next_page = request.args.get('next')
            if not HideFlash.exists('login_welcome'):
                flash(f'id=login_welcome add_dsa Welcome back {user.username}!','info')
            return redirect(next_page) if next_page else redirect(url_for('login'))
        elif not user.verified:
            sendToken(form.email.data,'verify')
            flash(f'id=login_unsuccessful_not_verified Login unsuccessful. Please confirm your email address. We just sent you another token.','warning')
        else:
            flash(f'id=login_unsuccessful Login unsuccessful. Please check email and/or password','warning')
    return render_template('login.html', form = form)
      
@app.route('/forgot_password', methods=['GET','POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.verified:
            sendToken(user.email,'change_password')
        else:
            sendToken(user.email,'verify')
        flash(f'id=change_password_token_sent An email has been sent to your account. Please check your email to change your password.','success')
        return redirect(url_for('login'))
    return render_template('forgot_password.html', form = form)


@app.route("/change_password/<token>", methods=['GET','POST'])
def change_password(token):
    form = NewPasswordForm()
    if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        if form.validate_on_submit():
            email = email_confirmation_Serializer.loads(token, salt='change-password', max_age=1800)
            user = User.query.filter_by(email=email).first()
            if user and user.verified:
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user.password = hashed_password
                db.session.commit()
                flash(f'id=password_has_been_changed Your password has been updated','success')
                login_user(user)
                return redirect(url_for('login'))
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        try:
            email = email_confirmation_Serializer.loads(token, salt='change-password', max_age=1800)
        except SignatureExpired:
            sendToken(email,'change_password')
            flash(f'id=password_token_expired Your token is expired. We just sent you a new token. Please check your email account','warning')
            return redirect(url_for('login'))
        except (BadTimeSignature,BadSignature):
            flash(f'id=password_token_invalid Your token is invalid. Please try one more time','warning')
            return redirect(url_for('login'))
    return render_template('change_password.html', form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
   
    
@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form_username = EditFormUsername()
    form_email = EditFormEmail()
    form_password = EditFormPassword()
    data = {
        'stats_total':RiddleData.get_stats_total(),
        'stats':RiddleData.get_stats()
        }
    if "submitUsername" in request.form:
        if form_username.submitUsername.data and form_username.validate_on_submit():
            current_user.username = form_username.username.data
            db.session.commit()
            flash(f'id=edit_username_successful Username has been updated!','success')
            return redirect(url_for('account', data=data, form_username=form_username, form_password=form_password, form_email=form_email, show_modal_password=0, show_username_input = 0, show_email_input = 0, user_image_values = ast.literal_eval(current_user.image_values)))
        else:
            form_username.username.data = current_user.username
            form_email.email.data = current_user.email
            return render_template('account.html', data=data, form_username=form_username, form_password=form_password, form_email=form_email, show_modal_password=0, show_username_input = 1, show_email_input = 0, user_image_values = ast.literal_eval(current_user.image_values))

    elif "submitEmail" in request.form:
        if form_email.submitEmail.data and form_email.validate_on_submit():
            current_user.email = form_email.email.data
            db.session.commit()
            flash(f'id=edit_email_successful Email has been updated!','success')
            return redirect(url_for('account', data=data, form_username=form_username, form_password=form_password, form_email=form_email, show_modal_password=0, show_username_input = 0, show_email_input = 0, user_image_values = ast.literal_eval(current_user.image_values)))
        else:
            form_username.username.data = current_user.username
            form_email.email.data = current_user.email
            return render_template('account.html', data=data, form_username=form_username, form_password=form_password, form_email=form_email, show_modal_password=0, show_username_input = 0, show_email_input = 1, user_image_values = ast.literal_eval(current_user.image_values))

    elif "submitPassword" in request.form:
        if form_password.submitPassword.data and form_password.validate_on_submit():
            if bcrypt.check_password_hash(current_user.password,form_password.current_password.data) and current_user.verified:
                hashed_password = bcrypt.generate_password_hash(form_password.password.data).decode('utf-8')
                current_user.password = hashed_password
                db.session.commit()
                flash(f'id=edit_password_successful Password has been updated!','success')
            return redirect(url_for('account', data=data, form_username=form_username, form_password=form_password, form_email=form_email, show_modal_password=0, show_username_input = 0, show_email_input = 0, user_image_values = ast.literal_eval(current_user.image_values)))

        else:
            flash(f'id=edit_password_not_successful Password has not been updated!','warning')
            form_username.username.data = current_user.username
            form_email.email.data = current_user.email
            return render_template('account.html', data=data, form_username=form_username, form_password=form_password, form_email=form_email, show_modal_password=1, show_username_input = 0, show_email_input = 0, user_image_values = ast.literal_eval(current_user.image_values))
    
    else:
        form_username.username.data = current_user.username
        form_email.email.data = current_user.email
        return render_template('account.html', data=data, form_username=form_username, form_password=form_password, form_email=form_email, show_modal_password=0, show_username_input = 0, show_email_input = 0, user_image_values = ast.literal_eval(current_user.image_values))



@app.route('/game/<riddleId>',methods=['GET'])
@login_required
def game(riddleId):
    #Check if id of url exists
    if ((Riddles.exists(riddleId) and Riddles.is_active(riddleId)) or (Riddles.exists(riddleId) and current_user.is_admin)):
        #check if user already started with the game. if not create new entry to the db
        riddle_data = RiddleData.query.filter_by(user_id = current_user.id, riddle_id = riddleId).first()
        if not riddle_data:
            #First Visit --> Creating Game Data'
            riddle_data = RiddleData(user_id = current_user.id, riddle_id = riddleId, datetime_start = datetime.now())
            db.session.add(riddle_data)
            db.session.commit()
        #store start time in data
        data = {
            'start_time' : riddle_data.datetime_start.isoformat(),
            }
        
        #store already used hints in list
        hints_used = [riddle_data.hint1_used,riddle_data.hint2_used,riddle_data.hint3_used]
        
        #add hints to data if they exist
        riddle = Riddles.query.filter_by(id = riddleId).first()
        
        hints = []
        for index,hint in enumerate([riddle.hint1,riddle.hint2,riddle.hint3]):
            if hint != '':
                #match user_hint-Data to riddle_hints
                if hints_used[index] == True:
                    hints.append((index+1,hint))
                else:
                    hints.append((index+1,False))
                    
        data['hint'] = hints
        print(data['hint'])
        #add solution to data
        data['solution'] = riddle.solution
        
        #add game-id to data
        data['game_id'] = riddleId

        print(data) 
        return render_template(riddleId+'.html', data = data)
    else:
        flash(f'id=riddle_does_not_exist This Riddle does not exist ...yet 😉','warning')
        return redirect(url_for('home'))

@app.route('/createRandomImage', methods=['POST','GET'])
def createRandomImage():
    image_small = createUserImage()
    return jsonify(image_small)

@login_required
@app.route('/admin')
def admin():
    if current_user.email == 'renzosmania@hotmail.com' or current_user.is_admin:
        form = SqlForm()
        return render_template('admin.html', form=form)
    else:
        return redirect(url_for('login'))

@login_required
@app.route('/admin/<path:table>', methods=['GET','POST'])
def admin_table(table):
    if current_user.email == 'renzosmania@hotmail.com' or current_user.is_admin:
        form = SqlForm()
        tables_dict = {table.__tablename__: table for table in db.Model.__subclasses__()}
        df_columns = tables_dict.get(str(table).lower()).__table__.columns.keys()
        form.column.choices = [(c, c) for c in df_columns]
        
        df = pd.read_sql(sql = db.session.query(tables_dict.get(str(table).lower())).statement, con = db.session.bind).to_html(index=0,justify='center')
        
        if form.validate_on_submit():
            if form.id.data == -99:
                db.session.add(Riddles(hint1='', solution=''))
                db.session.commit()
            else:
                entry_to_change = tables_dict.get(str(table).lower()).query.filter_by(id=form.id.data).first()
                if is_int(form.value.data):
                    setattr(entry_to_change, form.column.data, int(form.value.data))
                else:
                    setattr(entry_to_change, form.column.data, form.value.data)
                db.session.commit()
            return redirect(request.url)
        return render_template('admin.html',data = df,keys = df_columns, form = form)
    else:
        return redirect(url_for('login'))

@app.route('/test')
def test():
    return render_template('base_riddle.html')
   
