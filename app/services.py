from flask_restful import Resource
from flask import request, jsonify, url_for
from flasgger import swag_from
from spyne import rpc, ServiceBase, Unicode, Float, Integer
import json
from database import db
from models import User
from models import Account


class UsersServiceRest(Resource):
    @swag_from(
        {
            "summary": "Lista todos os usuários",
            "responses": {
                200: {
                    "description": "Lista de usuários cadastrados",
                    "schema": {
                        "type": "array",
                        "items": {
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "name": {"type": "string", "example": "João"},
                                "email": {
                                    "type": "string",
                                    "example": "joao@email.com",
                                },
                            }
                        },
                    },
                }
            },
        }
    )
    def get(self):
        users = User.query.all()
        return jsonify(
            [
                {
                    "id": u.id,
                    "name": u.name,
                    "email": u.email,
                    "_links": {
                        "self": url_for(
                            "usersservicerest", user_id=u.id, _external=True
                        ),
                        "accounts": url_for(
                            "accountsservicerest", user_id=u.id, _external=True
                        ),
                    },
                }
                for u in users
            ]
        )

    @swag_from(
        {
            "summary": "Cria um novo usuário",
            "parameters": [
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {
                        "properties": {
                            "name": {"type": "string", "example": "João"},
                            "email": {"type": "string", "example": "joao@email.com"},
                        }
                    },
                }
            ],
            "responses": {
                201: {
                    "description": "Usuário criado com sucesso",
                }
            },
        }
    )
    def post(self):
        data = request.get_json()
        new_user = User(name=data["name"], email=data["email"])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(
            {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "_links": {
                    "self": url_for(
                        "usersservicerest", user_id=new_user.id, _external=True
                    ),
                    "accounts": url_for(
                        "accountsservicerest", user_id=new_user.id, _external=True
                    ),
                },
            }
        )


class AccountsServiceRest(Resource):
    @swag_from(
        {
            "summary": "Lista todas as contas",
            "responses": {
                200: {
                    "description": "Lista de contas cadastradas",
                    "schema": {
                        "type": "array",
                        "items": {
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "user_id": {"type": "integer", "example": 1},
                                "balance": {"type": "float", "example": 100.50},
                            }
                        },
                    },
                }
            },
        }
    )
    def get(self):
        accounts = Account.query.all()
        return jsonify(
            [
                {
                    "id": a.id,
                    "user_id": a.user_id,
                    "balance": a.balance,
                    "_links": {
                        "self": url_for(
                            "accountsservicerest", account_id=a.id, _external=True
                        ),
                        "user": url_for(
                            "usersservicerest", user_id=a.user_id, _external=True
                        ),
                    },
                }
                for a in accounts
            ]
        )

    @swag_from(
        {
            "summary": "Cria uma nova conta",
            "parameters": [
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {
                        "properties": {
                            "user_id": {"type": "integer", "example": 1},
                            "balance": {"type": "float", "example": 100.50},
                        }
                    },
                }
            ],
            "responses": {
                201: {
                    "description": "Conta criada com sucesso",
                }
            },
        }
    )
    def post(self):
        data = request.get_json()
        new_account = Account(user_id=data["user_id"], balance=data.get("balance", 0.0))
        db.session.add(new_account)
        db.session.commit()
        return jsonify(
            {
                "id": new_account.id,
                "user_id": new_account.user_id,
                "balance": new_account.balance,
                "_links": {
                    "self": url_for(
                        "accountsservicerest", account_id=new_account.id, _external=True
                    ),
                    "user": url_for(
                        "users", user_id=new_account.user_id, _external=True
                    ),
                },
            }
        )


class AccountServiceSOAP(ServiceBase):
    @rpc(Integer, _returns=Unicode)
    # <tns:get_user>
    def get_user(ctx, user_id):
        #  <tns:user_id>
        user = User.query.get(user_id)
        if user:
            return json.dumps({"id": user.id, "name": user.name, "email": user.email})
        return "User not found"

    @rpc(Integer, Float, _returns=Unicode)
    def add_account(ctx, user_id, balance):
        new_account = Account(user_id=user_id, balance=balance)
        db.session.add(new_account)
        db.session.commit()
        return "Account added successfully"

    @rpc(Integer, _returns=Unicode)
    def get_account(ctx, account_id):
        account = Account.query.get(account_id)
        if account:
            return json.dumps(
                {
                    "id": account.id,
                    "user_id": account.user_id,
                    "balance": account.balance,
                }
            )
        return "Account not found"
