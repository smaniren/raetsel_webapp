from datetime import datetime,timedelta
from logging.handlers import RotatingFileHandler
from clueful import db, login_manager
from flask_login import UserMixin
from flask_login import current_user
from sqlalchemy import func

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20),nullable=False, default='default_user_img.jpg')
    image_values = db.Column(db.String(2500), unique=False,nullable=False, default='tbd')
    password = db.Column(db.String(60), nullable=False)
    points_sum = db.Column(db.Integer, default = 0)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    music_on = db.Column(db.Boolean, nullable=False, default=True)
    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.points_sum}', '{self.image_file}')"
        
    def get_top_ten():
        return User.query.order_by(User.points_sum.desc()).filter_by(is_admin=0).limit(10).all()
    
    def get_admin_ids():
        return [x.id for x in User.query.filter_by(is_admin=1).all()]
    
class Riddles(db.Model):
    __tablename__ = 'riddles'
    id = db.Column(db.Integer, primary_key=True)
    hint1 = db.Column(db.String(240), nullable=False)
    hint2 = db.Column(db.String(240), nullable=True, default='')
    hint3 = db.Column(db.String(240), nullable=True, default='')
    solution = db.Column(db.String(240), nullable=False)
    number_of_ratings = db.Column(db.Integer,unique=False,nullable=False, default=0)
    sum_of_ratings = db.Column(db.Integer,unique=False,nullable=False, default=0)
    rating = db.Column(db.Float,unique=False,nullable=False, default=0.0)
    active = db.Column(db.Boolean, nullable=False, default=False)
    def exists(riddleId):
        return riddleId in [str(riddle.id) for riddle in db.session.query(Riddles.id).distinct()]
    
    def is_active(riddleId):
        return db.session.query(Riddles).filter_by(id=riddleId).first().active
    
    def get_riddles():
        riddles = []
        #Only get active Riddles
        for riddle in db.session.query(Riddles).filter_by(active=1).all():
            riddle_data={}
            #get fastest user(s)
            
            sub_q = db.session.query(func.min(RiddleData.final_time)).filter(RiddleData.riddle_id==riddle.id,RiddleData.user_id.not_in(User.get_admin_ids()))
            user_ids = db.session.query(RiddleData).filter(RiddleData.riddle_id==riddle.id,RiddleData.final_time==sub_q,RiddleData.points!=0).all()
            usernames = []
            for id in user_ids:
                username = db.session.query(User).filter(User.id == id.user_id).first().username
                usernames.append(username)
            if len(usernames)<1:
                usernames.append('none')
                
            #get average time
            avg_time = db.session.query(func.avg(RiddleData.final_time)).filter(RiddleData.riddle_id == riddle.id, RiddleData.points != 0, RiddleData.user_id.not_in(User.get_admin_ids())).first()[0]
            if avg_time is not None:
                avg_time = str(timedelta(seconds=avg_time) - timedelta(microseconds=timedelta(seconds=avg_time).microseconds))
            else:
                avg_time = '--:--:--'
            
            riddle_data = {
                'riddle_id':riddle.id,
                'riddle_nr':riddle.id,
                'riddle_rating':riddle.rating,
                'riddle_fastest_player':usernames,
                'riddle_mean_time': avg_time
            }
            riddles.append(riddle_data)
        return riddles
    
class RiddleData(db.Model):
    __tablename__ = 'riddle_data'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    riddle_id = db.Column(db.Integer, db.ForeignKey('riddles.id'), nullable=False)
    """ riddle_id = db.Column(db.Integer, db.ForeignKey('riddle_data.id'), nullable=False) """
    datetime_start = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    datetime_end = db.Column(db.DateTime)
    final_time = db.Column(db.Integer, default = 0)
    points = db.Column(db.Integer, default = 0)
    rating = db.Column(db.Integer,unique=False,nullable=False, default=0)
    hint1_used = db.Column(db.Boolean, nullable=False, default=False)
    hint2_used = db.Column(db.Boolean, nullable=False, default=False)
    hint3_used = db.Column(db.Boolean, nullable=False, default=False)
    
    
    def __repr__(self):
        return f"Riddle_Data:(riddle_id = '{self.riddle_id}', user_id = '{self.user_id}', final_time = '{self.final_time}', points = '{self.points}', hint1_used = '{self.hint1_used}', hint2_used = '{self.hint2_used}', hint3_used = '{self.hint3_used}')"
    def not_rated_yet(riddle_id):
        if RiddleData.query.filter_by(user_id = current_user.id, riddle_id = riddle_id).first().rating != 0:
            return 0
        else:
            return 1
    
    def update_total_points():
        current_user.points_sum = db.session.query(func.sum(RiddleData.points)).filter(RiddleData.user_id == current_user.id).first()[0]
        db.session.commit()
    
    def get_stats_total():
        total_time_exists = db.session.query(func.sum(RiddleData.final_time)).filter(RiddleData.user_id == current_user.id).first()[0] is not None
        total_points_exists = current_user.points_sum
        if total_time_exists and total_points_exists:
            total_time = str(timedelta(seconds=db.session.query(func.sum(RiddleData.final_time)).filter(RiddleData.user_id == current_user.id).first()[0]))
            total_points = User.query.filter_by(id=current_user.id).first().points_sum
        else:
            total_time='--:--:--'
            total_points='--'
        return {'total_time':total_time,'total_points':total_points}
    
    def get_stats():
        stats_result=[]
        stats = RiddleData.query.filter_by(user_id = current_user.id).all()
        for stat in stats:
            stats_result.append([stat.riddle_id,str(timedelta(seconds=stat.final_time)),stat.points])
        return stats_result

class HideFlash(db.Model):
    __tablename__ = 'hide_flash'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flash_id = db.Column(db.String(240), nullable=False)
    do_not_show = db.Column(db.Boolean)
    def exists(flash_id):
        return flash_id in [x.flash_id for x in HideFlash.query.filter_by(user_id=current_user.id).all()]