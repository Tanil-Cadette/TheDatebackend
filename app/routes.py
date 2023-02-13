from app import db
from app.models.friends import Friend
from app.models.dates import Date
from app.models.user import User
from flask import Blueprint, jsonify, abort, request, make_response
from datetime import datetime
import requests
import time 
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


friends_bp = Blueprint("friends", __name__, url_prefix="/friends")
dates_bp = Blueprint("dates", __name__, url_prefix="/dates")
recommendations_bp = Blueprint("recommendations", __name__, url_prefix="/recommendations")
user_bp = Blueprint("users", __name__, url_prefix="/users")

#__________________________________________________________________________________________________________
#--------------------------------HELPER FUNCTIONS----------------------------------------------------------
#__________________________________________________________________________________________________________
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

#_________________________________________________________________________________________________________
#-------------------------------ADD FRIEND----------------------------------------------------------------
#_________________________________________________________________________________________________________
@friends_bp.route("", methods=["POST"])
def create_friend():
  request_body = request.get_json()
  
  try: 
    new_friend= Friend.from_dict(request_body)
  except KeyError:
    if "name" not in request_body or "location" not in request_body or "interest" not in request_body:
      return make_response({"details": "Missing required keys in request body"}, 400)
  
  db.session.add(new_friend)
  db.session.commit()
  friend_dict= new_friend.to_dict()
  
  return make_response(jsonify({"friend": friend_dict}), 201)
  
#_________________________________________________________________________________________________________
#-------------------------------GET FRIENDS---------------------------------------------------------------
#_________________________________________________________________________________________________________  
@friends_bp.route("", methods=["GET"])
def get_friends():
  friends_list=[]
  friends= Friend.query.all()
  
  for friend in friends:
    friends_list.append(friend.to_dict())
  
  return jsonify(friends_list), 200

@friends_bp.route("/<id>", methods=["GET"])
def get_one_friend(id):
  friend= validate_model(Friend, id)
  friend_dict= friend.to_dict()
  
  return jsonify(friend_dict)

#_________________________________________________________________________________________________________
#-----------------------------UPDATE FRIENDS--------------------------------------------------------------
#_________________________________________________________________________________________________________ 
@friends_bp.route("/<id>", methods=["PATCH"])
def update_friend(id):
  friend= validate_model(Friend, id)
  request_body= request.get_json()
  
  friend.update_friend(request_body)
  friend_dict= friend.to_dict()
  db.session.commit()
  
  return make_response(jsonify(friend_dict), 200)

#_________________________________________________________________________________________________________
#-----------------------------DELETE FRIEND---------------------------------------------------------------
#_________________________________________________________________________________________________________ 
@friends_bp.route("/<id>", methods=["DELETE"])
def delete_friend(id):
  friend= validate_model(Friend, id)
  friend_dict= friend.to_dict()
  
  db.session.delete(friend)
  db.session.commit()
  
  return jsonify({'details': (f'{friend_dict["name"]} successfully deleted from friends list')})

#_________________________________________________________________________________________________________
#-----------------------------CREATE DATE ----------------------------------------------------------------
#_________________________________________________________________________________________________________ 
@dates_bp.route("", methods=["POST"])
def create_date():
  request_body = request.get_json()
  
  try: 
    new_date= Date.from_dict(request_body)
  except KeyError:
      return make_response({"details": "Missing required keys in request body"}, 400)
    
  new_date= Date.from_dict(request_body)
  
  db.session.add(new_date)
  db.session.commit()
  date_dict= new_date.to_dict()
  
  return make_response(jsonify({"date": date_dict}), 201)
#_________________________________________________________________________________________________________
#-----------------------------GET DATE -------------------------------------------------------------------
#_________________________________________________________________________________________________________ 
@dates_bp.route("", methods=["GET"])
def get_dates():   
    dates_response= []
    dates= Date.query.all()
    
    for date in dates:
        dates_response.append(date.to_dict())
    
    return jsonify(dates_response), 200


@dates_bp.route("/<id>", methods=["GET"])
def read_one_date(id):
    date= validate_model(Date, id)
    date_dict = date.to_dict()
    
    return jsonify(date_dict)

#_________________________________________________________________________________________________________
#-----------------------------UPDATE DATE ----------------------------------------------------------------
#_________________________________________________________________________________________________________ 
@dates_bp.route("/<id>", methods=["PATCH"])   
def update_date(id):
    date = validate_model(Date, id)
    request_body = request.get_json()
    
    date.update(request_body)
    date_dict = date.to_dict()
    db.session.commit()

    return make_response(jsonify(date_dict), 200)
#_________________________________________________________________________________________________________
#-----------------------------DELETE DATE ----------------------------------------------------------------
#_________________________________________________________________________________________________________ 
@dates_bp.route("/<id>", methods=["DELETE"])
def delete_date(id):
    date = validate_model(Date, id)
    date_dict= date.to_dict()
    
    db.session.delete(date)
    db.session.commit()
    
    return jsonify({'details': (f'{date_dict["place"]} successfully deleted')})


#_________________________________________________________________________________________________________
#-----------------------------CREATE DATE FOR FRIEND------------------------------------------------------
#_________________________________________________________________________________________________________ 
@friends_bp.route("/<id>/dates", methods=["POST"])
def create_date_for_friend(id):
  friend= validate_model(Friend, id)
  request_body = request.get_json()
  
  try: 
    new_date= Date.from_dict(request_body)
  except KeyError:
      return make_response({"details": "Missing required keys in request body"}, 400)
    
  new_date= Date.from_dict(request_body)
  friend.dates.append(new_date)
  
  db.session.add(new_date)
  db.session.commit()
  date_dict= new_date.to_dict()
  
  return make_response(jsonify({"friend": date_dict}), 201)

#_________________________________________________________________________________________________________
#-----------------------------GET FRIENDS WITH DATES------------------------------------------------------
#_________________________________________________________________________________________________________ 
@friends_bp.route("/<id>/dates", methods=["GET"])
def read_friend_dates(id):
  friend= validate_model(Friend, id)
  date_id= []
  
  for date in friend.dates:
    date_dict= date.to_dict()
    date_id.append(date_dict)
    
  response_dict= friend.to_dict()
  response_dict["date"]= date_id
  
  return jsonify(response_dict), 200
    

#_________________________________________________________________________________________________________
#-----------------------------GET RECOMMENDED PLACES------------------------------------------------------
#_________________________________________________________________________________________________________ 
@recommendations_bp.route("/<interest>/<location>", methods=["GET"])
def get_recommended_places(interest, location):
    # url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + interest + "in" + location + "&location=" + location + "&radius=20000&key=" + GOOGLE_API_KEY
  url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + interest + "in" + location + "&radius=20000&key=" + GOOGLE_API_KEY
  try:
    response = requests.get(url)
    if response.status_code == 200:
      data = response.json()
      data_list = data["results"]
      results = []
      for place in data_list:
        results.append({
          'name': place['name'],
          'geometry': place['geometry']['location'],
          'rating' : place['rating']
        })
      return jsonify(results)
  except requests.exceptions.HTTPError as error:
    return "An HTTP error occurred: " + str(error)
  except requests.exceptions.RequestException as error:
    return "A Request error occurred: " + str(error)

#_________________________________________________________________________________________________________
#-------------------------------ADD USER------------------------------------------------------------------
#_________________________________________________________________________________________________________
@user_bp.route("", methods=["POST"])
def create_user():
  request_body = request.get_json()
  
  try: 
    new_user= User.from_dict(request_body)
  except KeyError:
    if "name" not in request_body or "location" not in request_body or "interest" not in request_body:
      return make_response({"details": "Missing required keys in request body"}, 400)
  
  db.session.add(new_user)
  db.session.commit()
  friend_dict= new_user.to_dict()
  
  return make_response(jsonify({"User": friend_dict}), 201)
#_________________________________________________________________________________________________________
#-------------------------------GET USERS---------------------------------------------------------------
#_________________________________________________________________________________________________________  
@user_bp.route("", methods=["GET"])
def get_user():
  users_list=[]
  users= User.query.all()
  
  for user in users:
    
    users_list.append(user.to_dict())
  
  return jsonify(users_list), 200

@user_bp.route("/<id>", methods=["GET"])
def get_one_user(id):
  user= validate_model(User, id)
  user_dict= user.to_dict()
  
  return jsonify(user_dict)

#_________________________________________________________________________________________________________
#-----------------------------UPDATE USER-----------------------------------------------------------------
#_________________________________________________________________________________________________________ 
@user_bp.route("/<id>", methods=["PATCH"])
def update_user(id):
  user= validate_model(User, id)
  request_body= request.get_json()
  
  user.update_user(request_body)
  user_dict= user.to_dict()
  db.session.commit()
  
  return make_response(jsonify(user_dict), 200)

#_________________________________________________________________________________________________________
#-----------------------------DELETE USER-----------------------------------------------------------------
#_________________________________________________________________________________________________________ 
@user_bp.route("/<id>", methods=["DELETE"])
def delete_user(id):
  user= validate_model(User, id)
  user_dict= user.to_dict()
  
  db.session.delete(user)
  db.session.commit()
  
  return jsonify({'details': (f'{user_dict["name"]} account successfully deleted')})  

#_________________________________________________________________________________________________________
#-----------------------------CREATE FRIEND FOR USER------------------------------------------------------
#_________________________________________________________________________________________________________ 
@user_bp.route("/<id>/friends", methods=["POST"])
def create_friend_for_user(id):
  user= validate_model(User, id)
  request_body = request.get_json()
  
  try: 
    new_friend= Friend.from_dict(request_body)
  except KeyError:
      return make_response({"details": "Missing required keys in request body"}, 400)
    
  new_friend= Friend.from_dict(request_body)
  user.friends.append(new_friend)
  
  db.session.add(new_friend)
  db.session.commit()
  friend_dict= new_friend.to_dict()
  
  return make_response(jsonify({"user": friend_dict}), 201)

#_________________________________________________________________________________________________________
#-----------------------------GET USER WITH FRIENDS-------------------------------------------------------
#_________________________________________________________________________________________________________ 
@user_bp.route("/<id>/friends", methods=["GET"])
def read_user_friends(id):
  user= validate_model(User, id)
  friend_id= []
  
  for friend in user.friends:
    friend_dict= friend.to_dict()
    friend_id.append(friend_dict)
    
  response_dict= user.to_dict()
  response_dict["friends"]= friend_id
  
  return jsonify(response_dict), 200









