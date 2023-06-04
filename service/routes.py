"""
Account Service

This microservice handles the lifecycle of Accounts
"""
from flask import jsonify, request, make_response, abort
from service.models import Account
from service.common import status
from tests.test_routes import BASE_URL
from . import app

# Health Endpoint
@app.route("/health")
def health():
    return jsonify(dict(status="OK")), status.HTTP_200_OK


# GET INDEX
@app.route("/")
def index():
    return jsonify(
        name="Account REST API Service",
        version="1.0",
        # paths=url_for("list_accounts", _external=True),
    ), status.HTTP_200_OK


# CREATE A NEW ACCOUNT
@app.route("/accounts", methods=["POST"])
def create_account():
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    location_url = BASE_URL  # Update this once get_accounts has been implemented
    return make_response(jsonify(message), status.HTTP_201_CREATED, {"Location": location_url})


# LIST ALL ACCOUNTS
@app.route("/accounts", methods=["GET"])
def list_accounts():
    app.logger.info("Request to list Accounts")
    accounts = Account.all()
    account_list = [account.serialize() for account in accounts]
    app.logger.info("Returning [%s] accounts", len(account_list))
    return jsonify(account_list), status.HTTP_200_OK


# READ AN ACCOUNT
@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    app.logger.info("Request to read an Account with id: %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
    return account.serialize(), status.HTTP_200_OK


# UPDATE AN EXISTING ACCOUNT
@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    app.logger.info("Request to update an Account with id: %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
    account.deserialize(request.get_json())
    account.update()
    return account.serialize(), status.HTTP_200_OK


# DELETE AN ACCOUNT
@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    app.logger.info("Request to delete an Account with id: %s", account_id)
    account = Account.find(account_id)
    if account:
        account.delete()
    return "", status.HTTP_204_NO_CONTENT


# Utility Functions
def check_content_type(media_type):
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
