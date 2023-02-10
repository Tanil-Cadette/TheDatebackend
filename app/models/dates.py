from app import db
from datetime import datetime

class Date(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    place = db.Column(db.String)
    location= db.Column(db.String)
    category= db.Column(db.String)
    rank= db.Column(db.Integer)
    date_completed = db.Column(db.Boolean, nullable= True, default=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('friend.id'))
    friend = db.relationship('Friend', back_populates='dates')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='dates')
    
    
    def to_dict(self):
        if self.date_completed:
            completed= True
        else:
            completed= None
        
        date_as_dict = {}
        date_as_dict["id"]= self.id
        date_as_dict["place"]= self.place
        date_as_dict["location"]= self.location
        date_as_dict["category"]= self.category
        date_as_dict["rank"]= self.rank
        date_as_dict["date_completed"]= completed
        if self.friend:
            date_as_dict["friend_id"]= self.friend_id
        if self.user:
            date_as_dict["user_id"] = self.user_id
        
        
        return date_as_dict
    
    @classmethod
    def from_dict(cls, date_data):
        new_date= Date(place=date_data["place"],
                    location=date_data["location"],
                    category=date_data["category"],
                    rank=date_data["rank"],
                    date_completed=False)
        return new_date
    
    def update(self, req_body):
        try:
            self.date_completed= req_body["date_completed"]
            
        except KeyError as error:
            raise error