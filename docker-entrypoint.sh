#!/bin/sh

export FLASK_APP=src/app.py
export FLASK_ENV=production
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=${PORT:-5000}
export SQLALCHEMY_DATABASE_URI=sqlite:///$PWD/data/lichess_db_puzzle.sqlite
exec flask run
