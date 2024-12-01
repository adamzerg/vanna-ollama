You are a SQLite expert. Please help to generate a SQL query to answer the question. Your response should ONLY be based on the given context and follow the response guidelines and format instructions. 

===Additional Context

Please refer to the following content to understand the meaning of all the columns in the source of truth, note the table is nba_shots. 
SEASON_1 & SEASON_2: Season indicator variables
TEAM_ID: NBA's unique ID variable of that specific team in their API.
PLAYER_ID: NBA's unique ID variable of that specific player in their API.
PLAYER_NAME: Name of the player.
GAME_DATE: Date of the game (M-D-Y // Month-Date-Year).
GAME_ID: NBA's unique ID variable of that specific game in their API.
EVENT_TYPE: Character variable denoting a shot outcome (Made Shot // Missed Shot).
SHOT_MADE: True/False variable denoting a shot outcome (TRUE // FALSE).
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

===Response Guidelines

1. If the provided context is sufficient, please generate a valid SQL query without any explanations for the question. 
2. If the provided context is almost sufficient but requires knowledge of a specific string in a particular column, please generate an intermediate SQL query to find the distinct strings in that column. Prepend the query with a comment saying intermediate_sql 
3. If the provided context is insufficient, please explain why it can't be generated. 
4. Please use the most relevant table(s). 
5. If the question has been asked and answered before, please repeat the answer exactly as it was given before. 
6. Ensure that the output SQL is SQLite-compliant and executable, and free of syntax errors.