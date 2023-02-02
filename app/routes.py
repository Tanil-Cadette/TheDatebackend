from app import db
from app.models.friends import Friend
from app.models.dates import Date
from flask import Blueprint, jsonify, abort, request, make_response
from datetime import datetime


friends_bp = Blueprint("friends", __name__, url_prefix="/friends")
dates_bp = Blueprint("dates", __name__, url_prefix="/dates")

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
@friends_bp.route("/<id>", methods=["PUT"])
def update_friend(id):
  friend= validate_model(Friend, id)
  request_body= request.get_json()
  
  friend.update(request_body)
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
@dates_bp.route("/<id>", methods=["PUT"])   
def update_date(id):
    date = validate_model(Date, id)
    request_body = request.get_json()
    
    date.update(request_body)
    date_dict = date.to_dict()
    db.session.commit()

    return make_response(jsonify({date_dict}), 200)
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
    













