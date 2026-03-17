#! /usr/bin/env bash
sleep 10s
flask db init
flask db migrate
flask db upgrade
flask run --host=0.0.0.0