#!/bin/bash

source venv/bin/activate
export FLASK_APP=main.py
cd src
flask run --host=172.20.10.9

