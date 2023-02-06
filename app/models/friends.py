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
        friend_as_dict["dates"]= [date.to_dict() for date in self.dates.all()]
        
        return friend_as_dict
    
    @classmethod
    def from_dict(cls, friend_data):
        new_friend= Friend(name=friend_data["name"],
                        interest=friend_data["interest"],
                        location=friend_data["location"])
        return new_friend
    
    def update_friend(self, req_body):
        try:
            if "name" in req_body:
                self.name = req_body["name"]
            if "interest" in req_body:
                self.interest = req_body["interest"]
            if "location" in req_body:
                self.location = req_body["location"]
            if "dates" in req_body:
                new_date = Date.from_dict(req_body["dates"])
                self.dates.append(new_date)
            # self.name= req_body["name"]
            # self.interest= req_body["interest"]
            # self.location= req_body["location"]
            # new_date = Date.from_dict(req_body["dates"])
            # self.dates.append(new_date)
        except KeyError as error:
            raise error
        
        