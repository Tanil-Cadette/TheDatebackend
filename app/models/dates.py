from app import db
from datetime import datetime

class Date(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    place = db.Column(db.String)
    location= db.Column(db.ARRAY(db.Integer))
    category= db.Column(db.String)
    rank= db.Column(db.Integer)
    completed = db.Column(db.DateTime, nullable= True, default=None)
    review= db.Column(db.String)
    friend_id = db.Column(db.Integer, db.ForeignKey('friend.id'))
    friend = db.relationship('Friend', back_populates='dates')
    
    
    def to_dict(self):
        if self.completed:
            completed= datetime.now()
            review= self.review
        else:
            completed= None
            review= ''
        
        date_as_dict = {}
        date_as_dict["id"]= self.id
        date_as_dict["place"]= self.place
        date_as_dict["location"]= self.location
        date_as_dict["category"]= self.category
        date_as_dict["rank"]= self.rank
        date_as_dict["completed"]= completed
        date_as_dict["review"]= review
        if self.friend_id:
            date_as_dict["friend_id"]= self.friend_id
        
        return date_as_dict
    
    @classmethod
    def from_dict(cls, date_data):
        new_date= Date(place=date_data["place"],
                    location=date_data["location"],
                    category=date_data["category"],
                    rank=date_data["rank"],
                    completed=datetime.now(),
                    review=date_data["review"])
        return new_date
    
    def update(self, req_body):
        try:
            self.review = req_body["review"]
            
        except KeyError as error:
            raise error