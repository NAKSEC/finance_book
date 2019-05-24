''' controller and routes for users '''
import json
import os

import calculation
import logger
from app import app, mongo
from bson import json_util
from flask import request, jsonify

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@app.route('/user', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def user():
    if request.method == 'GET':
        query = request.args
        data = mongo.db.users.find_one(query)
        return jsonify(data), 200

    data = request.get_json()
    if request.method == 'POST':
        if data.get('name', None) is not None and data.get('email', None) is not None:
            mongo.db.users.insert_one(data)
            return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'DELETE':
        if data.get('email', None) is not None:
            db_response = mongo.db.users.delete_one({'email': data['email']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'PATCH':
        if data.get('query', {}) != {}:
            mongo.db.users.update_one(
                data['query'], {'$set': data.get('payload', {})})
            return jsonify({'ok': True, 'message': 'record updated'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400


@app.route('/ticker', methods=['GET'])
def get_summary_data_by_ticker():
    if request.method == 'GET':
        ticker = request.args
        cursor = mongo.db.summary_data.find({"ticker": ticker})
        json_docs = []
        for doc in cursor:
            print "in doc"
            json_doc = json.dumps(doc, default=json_util.default)
            json_docs.append(json_doc)
        return jsonify(json_docs), 200


@app.route('/ticker_fin', methods=['GET'])
def get_finance_by_ticker():
    if request.method == 'GET':
        ticker = request.args.get('ticker', type=str)
        LOG.info("ticker : %s " % ticker)
        cursor = mongo.balance_sheet.find({"ticker": ticker})
        json_docs = []
        for doc in cursor:
            current_assest = float(doc["totalCurrentAssets"])
            current_liabilites = float(doc["totalCurrentLiabilities"])
            current_ratio = calculation.calculator.get_current_ratio(current_assest, current_liabilites)
            json_docs.append("Liquid : {:10.4f}".format(current_ratio))
        return jsonify(json_docs), 200
