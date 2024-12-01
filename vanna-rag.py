
# import os
# print(os.environ.get("SSL_CERT_FILE"))

# import json
# API_KEYS = json.load(open('api_keys.json'))
# vanna_key = API_KEYS['vanna_key']
# openai_key = API_KEYS['openai_key']

import pandas as pd
import sqlite3

def import_csv_to_sqlite(csv_path, db_name='nba_shots.db'):
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(db_name)
    df.to_sql('nba_shots', conn, if_exists='replace', index=False)
    conn.close()

    print(f"Data imported successfully to {db_name}")

import_csv_to_sqlite('NBA_2024_Shots.csv')

from vanna.ollama import Ollama
from vanna.chromadb import ChromaDB_VectorStore

class MyVanna(ChromaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)

vn = MyVanna(config={'model': 'llama3.1'})

vn.connect_to_sqlite('nba_shots.db')



documentation = '''
SEASON_1 & SEASON_2: Season indicator variables
TEAM_ID: NBA's unique ID variable of that specific team in their API.
PLAYER_ID: NBA's unique ID variable of that specific player in their API.
PLAYER_NAME: Name of the player.
GAME_DATE: Date of the game (M-D-Y // Month-Date-Year).
GAME_ID: NBA's unique ID variable of that specific game in their API.
EVENT_TYPE: Character variable denoting a shot outcome (Made Shot // Missed Shot).
SHOT_MADE: True/False variable denoting a shot outcome (TRUE // FALSE).
ACTION_TYPE: Description of shot type (layup, dunk, jump shot, etc.).
…LOC_Y: Y coordinate of the shot in the x, y plane of the court (0, 50).
SHOT_DISTANCE: Distance of the shot with respect to the center of the hoop, in feet.
QUARTER: Quarter of the game.
MINS_LEFT: Minutes remaining in the quarter.
SECS_LEFT: Seconds remaining in minute of the quarter.
'''

vn.train(documentation=f"Please refer to the following content to understand the meaning of all the columns in the source of truth, note the table is nba_shots. {documentation}")

response = vn.ask("How many shots in total?")
response

question = "Who done most shots? Give me the player name"
vn.ask(question)

sql = vn.generate_sql(question)
sql

result = vn.run_sql(sql)
result

code = vn.generate_plotly_code(result)
code

figure = vn.get_plotly_figure(code, result)
figure

figure.write_image("plot.png")

vn.ask("Show me Luka Doncic's shot made percentage. Note that 1 means shot made, 0 shot miss")

question = "Plot the shooting percentages of the top 3 players with the highest shot made percentage. Note that 1 means shot made, 0 shot miss"
vn.ask(question)

documentation = '''
SEASON_1 & SEASON_2: Season indicator variables
TEAM_ID: NBA's unique ID variable of that specific team in their API.
PLAYER_ID: NBA's unique ID variable of that specific player in their API.
PLAYER_NAME: Name of the player.
GAME_DATE: Date of the game (M-D-Y // Month-Date-Year).
GAME_ID: NBA's unique ID variable of that specific game in their API.
EVENT_TYPE: Character variable denoting a shot outcome (Made Shot // Missed Shot).
SHOT_MADE: variable denoting a shot outcome (1 // 0).
ACTION_TYPE: Description of shot type (layup, dunk, jump shot, etc.).
SHOT_TYPE: Type of shot (2PT or 3PT).
BASIC_ZONE: Name of the court zone the shot took place in.
Restricted Area, In the Paint (non-RA), Midrange, Left Corner 3, Right Corner 3, Above the Break, Backcourt.
ZONE_NAME: Name of the side of court the shot took place in.
left, left side center, center, right side center, right
ZONE_ABB: Abbreviation of the side of court.
(L), (LC), (C), (RC), (R).
ZONE_RANGE: Distance range of shot by zones.
Less than 8 ft., 8-16 ft. 16-24 ft. 24+ ft.
LOC_X: X coordinate of the shot in the x, y plane of the court (0, 50).
LOC_Y: Y coordinate of the shot in the x, y plane of the court (0, 50).
SHOT_DISTANCE: Distance of the shot with respect to the center of the hoop, in feet.
QUARTER: Quarter of the game.
MINS_LEFT: Minutes remaining in the quarter.
SECS_LEFT: Seconds remaining in minute of the quarter.
'''

vn.train(documentation=f"Please refer to the following content to understand the meaning of all the columns in the source of truth. {documentation}")
sql = vn.generate_sql(question)
sql

result = vn.run_sql(sql)
print(type(result))
print(result)

import plotly.express as px

figure = px.bar(result, x='PLAYER_NAME', y='SHOOTING_PERCENTAGE', title='Top Shooters')

figure.update_layout(
    xaxis_title="Player Name",
    yaxis_title="Shot Made %",
    bargap=0.2,  # gap between bars
)

figure.write_image("plot.png")


# question = "Every 5 feet as a range, plot the total shots per shot distance, note you can calculate base on the given range start and end for SHOT_DISTANCE, query syntax is sqlite, plot to histogram"
question = "Every 5 feet as a range, plot the total shots per shot distance, note calculation can be base on the given range start and end for shot distance, plot to histogram"
vn.ask(question)

sql = vn.generate_sql(question)
sql

result = vn.run_sql(sql)
result

code = vn.generate_plotly_code(result)
code

from vanna.flask import VannaFlaskApp
VannaFlaskApp(vn).run()
