from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_raw_jwt
)
from passlib.hash import sha256_crypt

from app.models.records import Records
from app.models.users import User
from app.api import validate
app = Flask(__name__)
app.config['SECRET_KEY'] = "b'secert key'"
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
jwt = JWTManager(app)

INCIDENTS = []
USERS = []
blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@app.route('/api/v1/auth/register', methods=['POST'])
def create_user():

    user = request.get_json()
    email = user.get('email')
    username = user.get('username')
    password = user.get('password')
    available_emails = [x.email for x in USERS]
    dict_data = {'Email': email, 'Username': username, 'Password': password}

    if validate.key_blank(**dict_data):
        return jsonify(validate.key_blank(**dict_data)), 401
    if validate.blank(**dict_data):
        return jsonify(validate.blank(**dict_data)), 401
    if validate.email(email):   
        return jsonify(validate.email(email)), 401    
    if email in available_emails:
        return jsonify({'message': 'Email is already registered'}), 409
    if validate.key_password(password):
        return jsonify(validate.key_password(password))
    if validate.key_username(username):
        return jsonify(validate.key_username(username))

    password = sha256_crypt.encrypt(str(password))
    new_user = User(username, email, password)
    print(new_user)
    USERS.append(new_user)
    return jsonify({'message': 'User successfully registered'}), 201


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    user_request = request.get_json()
    email = user_request.get('email')
    password = user_request.get('password')
    dict_data = {'Email': email, 'Password': password}

    if validate.key_blank(**dict_data):
        return jsonify(validate.key_blank(**dict_data)), 401
    if validate.blank(**dict_data):
        return jsonify(validate.blank(**dict_data)), 401
    if validate.email(email):   
        return jsonify(validate.email(email)), 401   
    """Checks for user by email"""
    user_login = [user for user in USERS if user.email == email]
    if user_login:
        user_login = user_login[0]
        is_user_password = sha256_crypt.verify(str(password), user_login.password)
        if is_user_password and email == user_login.email:
            access_token = create_access_token(identity=email)
            response = {'token': access_token}
            return jsonify(response), 201
        return jsonify({'message': 'Password not correct'}), 403
    return jsonify({'message': 'Email not found'}), 404


@app.route('/api/v1/auth/logout', methods=["DELETE"])
@jwt_required
def logout():
    dumps = get_raw_jwt()['jti']
    blacklist.add(dumps)
    return jsonify({"msg": "Successfully logged out"}), 200   


@app.route('/api/v1/record', methods=['POST'])
@jwt_required
def register_record():
    """Registers non existing record"""
    new_record = request.get_json()
    record_name = new_record.get('recordname')
    description = new_record.get('description')
    category = new_record.get('category')
    location = new_record.get('location')
    dict_data = {'Recordsname': recordsname, 'Description': description,
                 'Category': category, 'Location': location}

    if validate.key_blank(**dict_data):
        return jsonify(validate.key_blank(**dict_data)), 401
    if validate.blank(**dict_data):
        return jsonify(validate.blank(**dict_data)), 401

    available_record = [Rec.recordname for Rec in INCIDENTS]

    if recordname in available_record:
        return jsonify({'message': 'Records already exists'}), 409

    new_record = Records(recordname, description, location, category)
    INCIDENTS.append(new_record)
    return jsonify({'message': 'Records successfully registered'}), 201


@app.route('/api/v1/record/', methods=['GET'])
def get_all_record():
    """Returns the requested record all the registered record"""
    get_record = [record for record in INCIDENTS]
    if not get_record:
            return jsonify({'message': 'Records not found'}), 409
    found_record = [{'recordtitle': record.recordtitle, 'description': record.description,
                    'category': record.category, 'location': record.location, 'id': record.id } for record in INCIDENTS]
    return jsonify(found_record), 200


@app.route('/api/v1/record/<int:record_id>', methods=['GET'])
def get_by_id(record_id):
    """Gets a particular record by id"""
    record = [record for record in INCIDENTS if record.id == record_id]
    if record:
        record = record[0]
    elif record not in INCIDENTS:
        return jsonify({'message': 'Records not found'}), 404
    found_record = {
                    'id': record.id,
                    'recordtitle': record.recordtitle,
                    'description': record.description,
                    'category': record.category,
                    'location': record.location
                   }
    return jsonify(found_record), 200


@app.route('/api/v1/record/<int:record_id>', methods=['PUT'])
@jwt_required
def update_by_id(record_id):
    """"updates record by id"""
    dict_data = request.get_json()

    if validate.key_blank(**dict_data):
        return jsonify(validate.key_blank(**dict_data)), 401
    if validate.blank(**dict_data):
        return jsonify(validate.blank(**dict_data)), 4011

    recordtitle = dict_data.get('recordtitle')
    record_names = [record.recordtitle for record in INCIDENTS]
    if recordtitle in record_names:
        return jsonify({'message': 'Records already exists'}), 409

    target_record = None
    for record in INCIDENTS:
        if record.id == record_id:
            target_record = record
            break
    if not target_record:
        return jsonify({"message": "Records not found"})
    for key in dict_data.keys():
        value = dict_data[key]
        setattr(target_record, key, value)

    updated_record = {'record.id': target_record.id, 'recordtitle': target_record.recordtitle,
                      'description': target_record.description, 'category': target_record.category,
                      'location': target_record.location}
    return jsonify(updated_record), 200


@app.route('/api/v1/record/<int:record_id>', methods=['DELETE'])
@jwt_required
def delete_record_by_id(record_id):
    """Endpoint for deleting requested record by id"""
    target_record = None
    for record in INCIDENTS:
        if record.id == record_id:
            target_record = record

    if target_record:
        INCIDENTS.remove(target_record)
        return jsonify({'message': 'Records successfully deleted'}), 202
    return jsonify({'message': 'Records not found'}), 404
