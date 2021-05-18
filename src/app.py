import flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sql
import click
import os
import functools
import random


app = flask.Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_mapping(os.environ)
db = SQLAlchemy(app)


# Monkey patch dataclass so that flask.jsonify can serialize
def model_to_dataclass(cls):
  import dataclasses
  dummy = dataclasses.make_dataclass('C', ['f'])
  def to_field(col):
    field = dataclasses.field()
    field.name = col.name
    field._field_type = dummy.__dataclass_fields__['f']._field_type
    return field
  cls.__dataclass_fields__ = dict((c.name, to_field(c)) for c in cls.__table__.columns)
  return cls


@model_to_dataclass
class Puzzle(db.Model):
  id               = db.Column(db.Integer, primary_key=True)
  puzzle_id        = db.Column(db.String)
  fen              = db.Column(db.String)
  move             = db.Column(db.String)
  rating           = db.Column(db.Integer)
  rating_deviation = db.Column(db.Integer)
  popularity       = db.Column(db.Integer)
  nb_plays         = db.Column(db.Integer)
  themes           = db.Column(db.String)
  game_url         = db.Column(db.String)

  @staticmethod
  @functools.cache
  def get_all_ids():
    # SQLalchemy query is slow for the large number of rows
    connection = db.engine.raw_connection()
    ids = connection.execute('SELECT id FROM puzzle')
    ids = [x[0] for x in ids]
    connection.commit()
    connection.close()
    return ids

  @staticmethod
  def get_random(count, color=None):
    like = f"% {color[0]} %" if color else '%'
    random_ids = random.sample(Puzzle.get_all_ids(), 20 * count) # Filter randomly by python
    selected = Puzzle.query.where(Puzzle.id.in_(random_ids)).where(Puzzle.fen.like(like)).limit(count).all()
    return selected


@app.cli.command("import-csv")
@click.argument("filename")
@click.argument("progress", default=100000, type=int)
def cli_import_csv(filename, progress):
  table = Puzzle.__table__
  columns = list(table.columns)

  def to_row(id_line):
    id, line = id_line
    if progress > 0 and id % progress == 0:
      print(f"[import-csv (progress)] {id = }")
    row_str = line.strip().split(',')
    row = [id] + [y.type.python_type(x) for x, y in zip(row_str, columns[1:])]
    return row

  qmarks = ','.join(['?'] * len(columns))
  insert_into = f"INSERT INTO {table.name} VALUES ({qmarks})"

  print(f"[import-csv] Resetting table...")
  table.drop(db.engine, checkfirst=True)
  table.create(db.engine)

  # Need to use sqlite3 connection directly for performance reason
  connection = db.engine.raw_connection()
  with open(filename) as f:
    rows = map(to_row, enumerate(f.readlines()))
    connection.executemany(insert_into, rows)
  connection.commit()
  connection.close()


@app.route('/random')
def route_random():
  count = flask.request.args.get('count', default=100, type=int)
  puzzles = Puzzle.get_random(count)
  return flask.jsonify(puzzles)


@app.shell_context_processor
def _to_shell():
  return dict(filter(lambda kv: not kv[0].startswith('_'), globals().items()))
