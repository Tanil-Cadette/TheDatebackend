from app import db
from app.models.dates import Date

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    interest = db.Column(db.ARRAY(db.String))
    location = db.Column(db.String)
    dates = db.relationship('Date', back_populates='friend', lazy='dynamic')

    
    def to_dict(self):
        friend_as_dict = {}
        friend_as_dict["id"]= self.id
        friend_as_dict["name"]= self.name
        friend_as_dict["interest"]= self.interest
        friend_as_dict["location"]= self.location 
        
        return friend_as_dict
    
    @classmethod
    def from_dict(cls, friend_data):
        new_friend= Friend(name=friend_data["name"],
                        interest=friend_data["interest"],
                        location=friend_data["location"])
        return new_friend
    
    def update(self, req_body):
        try:
            self.name= req_body["name"]
            self.interest= req_body["interest"]
            self.location= req_body["location"]
            new_date = Date.from_dict(req_body["dates"])
            self.dates.append(new_date)
        except KeyError as error:
            raise error
        
        