from flask import json, Response, request, jsonify
from flask_restful import Resource, Api
from models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.ext.declarative import DeclarativeMeta


from app import session

class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


class AddUser(Resource):
    def post(self):
        data = request.json
        try:
            user = Users(data["login"], data["password"], data["name"], data["passport"], data["address"], data["email"], data["phone_number"], data["status"])
            user.password = generate_password_hash(data['password'])

            checkuser = session.query(Users).filter(Users.login == user.login).all()
            if checkuser:
                return Response(
                    response=json.dumps({"message": "user with such login already exist"}),
                    status=409,
                    mimetype="application/json"
                )
            session.add(user)
            session.flush()
            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )

class Login(Resource):
    def post(self):
        data = request.json
        user = Users.authenticate(**data)
        token = user.get_token()
        return jsonify({'access_token': token})

class GetUser(Resource):
    @jwt_required
    def get(self, id):
        user_id = get_jwt_identity()
        checkuser = session.query(Users).filter(Users.id == user_id).one()
        if checkuser.status != "admin":
            return Response(
                response=json.dumps({"message": "Not allowed for users"}),
                status=400,
                mimetype="application/json"
            )
        user = session.query(Users).get(id)
        if user:
            return Response(
                response=json.dumps(user, cls=AlchemyEncoder),
                status=201,
                mimetype="application/json"
            )
        return Response(
                response=json.dumps({"message": "Not found"}),
                status=400,
                mimetype="application/json"
            )


class GetMyself(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = session.query(Users).get(user_id)
        if user:
            return Response(
                response=json.dumps(user, cls=AlchemyEncoder),
                status=201,
                mimetype="application/json"
            )
        return Response(
                response=json.dumps({"message": "Not found"}),
                status=400,
                mimetype="application/json"
            )

class UpdateUser(Resource):
    @jwt_required
    def put(self):
        data = request.json
        user_id = get_jwt_identity()
        try:
            user = session.query(Users).get(user_id)
            if not user:
                return Response(
                    response=json.dumps({"message": "invalid id"}),
                    status=400,
                    mimetype="application/json"
                )
            if "login" in data:
                user.login = data["login"]
            if "password" in data:
                user.password = generate_password_hash(data['password'])
            if "name" in data:
                user.name = data["name"]
            if "passport" in data:
                user.passport = data["passport"]
            if "address" in data:
                user.address = data["address"]
            if "email" in data:
                user.email = data["email"]
            if "phone_number" in data:
                user.phone_number = data["phone_number"]
            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )


class AddBank(Resource):
    @jwt_required
    def post(self):
        data = request.json
        user_id = get_jwt_identity()
        checkuser = session.query(Users).filter(Users.id == user_id).one()
        if checkuser.status != "admin":
            return Response(
                response=json.dumps({"message": "Not allowed for users"}),
                status=400,
                mimetype="application/json"
            )
        try:
            bank = Banks(data["all_money"], data["per_cent"])
            session.add(bank)
            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )


class GetBank(Resource):
    @jwt_required
    def get(self, id):
        bank = session.query(Banks).get(id)
        if bank:
            return Response(
                response=json.dumps(bank, cls=AlchemyEncoder),
                status=201,
                mimetype="application/json"
            )
        return Response(
                response=json.dumps({"message": "Not found"}),
                status=400,
                mimetype="application/json"
            )


class AddCredit(Resource):
    @jwt_required
    def post(self):
        data = request.json
        user_id = get_jwt_identity()
        checkuser = session.query(Users).filter(Users.id == user_id).one()
        if checkuser.status == "admin":
            return Response(
                response=json.dumps({"message": "Not allowed for admins"}),
                status=400,
                mimetype="application/json"
            )
        try:
            credit = Credits(data["start_date"], data["end_date"],  data["start_sum"], data["current_sum"], data["bank_id"], user_id)
            session.add(credit)
            session.commit()
            usercredit = UserCredit(credit.user_id, credit.id)
            session.add(usercredit)
            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )


class UpdateCredit(Resource):
    @jwt_required
    def put(self, credit_id):
        data = request.json
        user_id = get_jwt_identity()
        checkuser = session.query(Users).filter(Users.id == user_id).one()
        if checkuser.status == "admin":
            return Response(
                response=json.dumps({"message": "Not allowed for admins"}),
                status=400,
                mimetype="application/json"
            )
        try:
            credit = session.query(Credits).get(credit_id)
            if "current_sum" in data:
                credit.current_sum = data["current_sum"]
            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )


class GetCredit(Resource):
    @jwt_required
    def get(self, credit_id):
        credit = session.query(Credits).get(credit_id)
        if credit:
            return Response(
                response=json.dumps(credit, cls=AlchemyEncoder),
                status=201,
                mimetype="application/json"
            )
        return Response(
                response=json.dumps({"message": "Not found"}),
                status=400,
                mimetype="application/json"
            )


class AddTransaction(Resource):
    @jwt_required
    def post(self, credit_id):
        data = request.json
        user_id = get_jwt_identity()
        checkuser = session.query(Users).filter(Users.id == user_id).one()
        if checkuser.status == "admin":
            return Response(
                response=json.dumps({"message": "Not allowed for admins"}),
                status=400,
                mimetype="application/json"
            )
        try:
            transaction = Transactions(data["date"], data["summ"], credit_id)
            session.add(transaction)
            session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )


class GetTransaction(Resource):
    @jwt_required
    def get(self, credit_id, transaction_id):
        transaction = session.query(Transactions).get(transaction_id)
        if transaction:
            return Response(
                response=json.dumps(transaction, cls=AlchemyEncoder),
                status=201,
                mimetype="application/json"
            )
        return Response(
                response=json.dumps({"message": "Not found"}),
                status=400,
                mimetype="application/json"
            )