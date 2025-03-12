from flask import request, jsonify
from app import app, db
from models import PasswordEntry

@app.route('/store-passwords', methods=['POST'])
def store_password():
    data = request.get_json()
    user_id = data.get('user_id')
    website = data.get('website')
    username = data.get('username')
    password = data.get('password')

    if not website or not username or not password:
        return jsonify({'error': 'Missing website, username or password'}), 400
    
    new_password_entry = PasswordEntry(user_id=user_id, website=website, username=username)
    new_password_entry.encrypt_password(password)

    db.session.add(new_password_entry)
    db.session.commit()

    return jsonify({'message': 'Password stored successfully'}), 201


@app.route('/get-passwords/<int:user_id>', methods=['GET'])
def get_passwords(user_id):
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400

    password_entries = PasswordEntry.query.filter_by(user_id=user_id).all()

    return jsonify([{
        'website': password_entry.website,
        'username': password_entry.username,
        'password': password_entry.decrypt_password()
    } for password_entry in password_entries]), 200