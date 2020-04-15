# Author - Nikhil Patil
import csv
import os
from datetime import datetime

from flask import Flask, request
from flask_restful import abort, Api, Resource
import subprocess

import json
from http import HTTPStatus
import pandas as pd

app = Flask(__name__)
api = Api(app)


path = os.path.join(os.getcwd(), "MandiData.csv")


def get(name, village, start, end):
    # name = request.json["name"] if request.json["name"] is not "" else None
    # village = request.json["village"] if request.json["village"] is not "" else None
    # start = request.json["start_date"] if request.json["start_date"] is not "" else None
    # end = request.json["end_date"] if request.json["end_date"] is not "" else None

    checks = 0
    if name is not None:
        checks += 1
    if village is not None:
        checks += 1
    if start is not None:
        checks += 1
    if end is not None:
        checks += 1

    data = []

    with open(path, "r") as file:
        file.readline()  # Skip the first lines...headers
        line = file.readline()  # Read the first data line

        while line:
            passed = 0

            if name is not None and name in line:
                passed += 1

            if village is not None and village in line:
                passed += 1

            if start is not None:
                start_d = datetime.strptime(start, "%d/%m/%Y")
                date = datetime.strptime(line.split()[0], "%d/%m/%Y")
                if start_d <= date:
                    passed += 1

            if end is not None:
                end_d = datetime.strptime(end, "%d/%m/%Y")
                date = datetime.strptime(line.split()[0], "%d/%m/%Y")
                if date <= end_d:
                    passed += 1

            if passed == checks:
                data.append(line)

            line = file.readline()

    return data



class Entry(Resource):

    @staticmethod
    def post():
        name = request.json["name"]
        account = request.json["account_number"]
        weights = request.json["weights"]
        vegetable = request.json["vegetable"]
        village = request.json["village"]
        phone = request.json["phone_number"]
        date = datetime.now().strftime("%d/%m/%Y %H:%M.%S")
        quantity = len(weights.split(","))

        with open(path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, name, village, vegetable, quantity, weights, account, phone])

        return "Entry saved successfully!"

class GetEntry(Resource):
    @staticmethod
    def get(name=None):
        data = []

        with open(path, "r") as file:
            file.readline() #Skip the first lines...headers
            line = file.readline() #Read the first data line

            while line:
                if name is not None and name in line:
                    data.append(line)
                line = file.readline()

        return data

api.add_resource(Entry, "/entry")
api.add_resource(GetEntry, "/entry/<name>")

if __name__ == "__main__":
    app.run(debug=True)
