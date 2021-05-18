```bash
# Download data
wget -P data https://database.lichess.org/lichess_db_puzzle.csv.bz2
pbzip2 -d data/lichess_db_puzzle.csv.bz2

# Filter puzzles randomly to reduce file size
python src/filter_lines.py --count 200000 --i data/lichess_db_puzzle.csv --o data/lichess_db_puzzle--200K.csv

# Convert to sqlite
export FLASK_APP=src/app.py
export SQLALCHEMY_DATABASE_URI=sqlite:///$PWD/data/lichess_db_puzzle.sqlite
flask import-csv data/lichess_db_puzzle.csv

# Run server
flask run

# Local test
curl 'localhost:5000/random?count=2'
[
  {
    "fen": "r2q1rk1/pp1b1pp1/3Np3/3pn2Q/8/4P3/PPP3PP/R4RK1 b - - 3 16",
    "game_url": "https://lichess.org/cIQm1tfm/black#32",
    "id": 89302,
    "move": "e5c4 d6f7 f8f7 h5f7",
    "nb_plays": 1325,
    "popularity": 96,
    "puzzle_id": "3MI0O",
    "rating": 1836,
    "rating_deviation": 75,
    "themes": "crushing kingsideAttack middlegame short"
  },
  {
    "fen": "2k1R3/pp6/1np3pn/6Np/8/1BNq4/PP3PPP/2K5 b - - 0 22",
    "game_url": "https://lichess.org/H0UabpjC/black#44",
    "id": 153541,
    "move": "c8c7 g5e6 c7d6 e8d8 b6d7 d8d7 d6d7 e6c5",
    "nb_plays": 16,
    "popularity": 71,
    "puzzle_id": "5lN87",
    "rating": 1781,
    "rating_deviation": 100,
    "themes": "attraction crushing middlegame sacrifice veryLong"
  }
]

# Deploy
heroku apps:create hiro18181-puzzle-api
docker push registry.heroku.com/hiro18181-puzzle-api/web
heroku container:release web
curl 'https://hiro18181-puzzle-api.herokuapp.com/random?count=2'
```
