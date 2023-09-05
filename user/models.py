from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid

class User:

  def start_session(self, user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    return jsonify(user), 200

  def signup(self):
    print(request.form)

    # Create the user object
    user = {
      "_id": uuid.uuid4().hex,
      "name": request.form.get('name'),
      "email": request.form.get('email'),
      "password": request.form.get('password')
    }

    # Encrypt the password
    user['password'] = pbkdf2_sha256.encrypt(user['password'])

    # Check for existing email address
    if db.users.find_one({ "email": user['email'] }):
      return jsonify({ "error": "Email address already in use" }), 400

    if db.users.insert_one(user):
      return self.start_session(user)

    return jsonify({ "error": "Signup failed" }), 400
  
  def signout(self):
    session.clear()
    return redirect('/')
  
  def login(self):

    user = db.users.find_one({
      "email": request.form.get('email')
    })

    if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
      return self.start_session(user)
    
    
    return jsonify({ "error": "Invalid login credentials" }), 401
  
  def edit_collection(self):
    return redirect('/edit_collection/')
  

class coins:
  def get_coins(self):
    return db.coins.find()
  
  def add_coin(self):
    coin = {
      "_id": uuid.uuid4().hex,
      "name": request.form.get('name'),
      "symbol": request.form.get('symbol'),
      "price": request.form.get('price')
    }
    
    if db.coins.find_one({ "name": coin['name'] }):
      return jsonify({ "error": "Coin already in collection" }), 400
    
    if db.coins.insert_one(coin):
      return redirect('/edit_collection/')
    
    return jsonify({ "error": "Coin not added" }), 400
  
  def delete_coin(self):
    coin = {
      "_id": uuid.uuid4().hex,
      "name": request.form.get('name'),
      "symbol": request.form.get('symbol'),
      "price": request.form.get('price')
    }
    
    if db.coins.find_one({ "name": coin['name'] }):
      db.coins.delete_one({ "name": coin['name'] })
      return redirect('/edit_collection/')
    
    return jsonify({ "error": "Coin not deleted" }), 400
  
  def update_coin(self):
    coin = {
      "_id": uuid.uuid4().hex,
      "name": request.form.get('name'),
      "symbol": request.form.get('symbol'),
      "price": request.form.get('price')
    }
    
    if db.coins.find_one({ "name": coin['name'] }):
      db.coins.update_one({ "name": coin['name'] }, { "$set": { "price": coin['price'] } })
      return redirect('/edit_collection/')
    
    return jsonify({ "error": "Coin not updated" }), 400