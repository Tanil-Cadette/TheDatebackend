from app import db
from app.models.dates import Date
from app.models.friends import Friend

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name= db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    friends = db.relationship('Friend', back_populates='user', lazy='dynamic')
    dates = db.relationship('Date', back_populates='user', lazy='dynamic')
    
    
    def to_dict(self):
        user_as_dict = {}
        user_as_dict["id"]= self.id
        user_as_dict["name"]= self.name
        user_as_dict["email"]= self.email
        user_as_dict["password"] = self.password
        user_as_dict["friends"] = [friend.to_dict() for friend in self.friends] if self.friends else []
        user_as_dict["dates"] = [date.to_dict() for date in self.dates] if self.dates else []
        
        return user_as_dict
    
    @classmethod
    def from_dict(cls, user_data):
        new_user= User(name=user_data["name"],
                        email=user_data["email"],
                        password=user_data["password"])
        return new_user
    
    def update_user(self, req_body):
        try:
            if "name" in req_body:
                self.name = req_body["name"]
            if "email" in req_body:
                self.email = req_body["email"]
            if "password" in req_body:
                self.password = req_body["password"]
        except KeyError as error:
            raise error
