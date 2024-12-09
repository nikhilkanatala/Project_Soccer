"""
Load American Soccer Analysis API to Azure DB
"""

import logging
import pandas as pd
import numpy as np
from modules.asa_api.api import (get_games, get_game_xgoals, get_teams,
                 get_team_salaries, get_players, get_player_salaries,
                 get_managers, get_referees, get_stadiums)
from modules.utils.db import AzureDBConn


# Mapping for the raw columns to Azure DB table columns
GAME_COLS = {
    'game_id': 'GAME_ID',
    'date_time_utc': 'DATE_TIME_UTC',
    'home_score': 'HOME_SCORE',
    'away_score': 'AWAY_SCORE',
    'home_team_id': 'HOME_TEAM_ID',
    'away_team_id': 'AWAY_TEAM_ID',
    'referee_id': 'REFEREE_ID',
    'stadium_id': 'STADIUM_ID',
    'home_manager_id': 'HOME_MANAGER_ID',
    'away_manager_id': 'AWAY_MANAGER_ID',
    'expanded_minutes': 'EXPANDED_MINUTES',
    'season_name': 'SEASON_NAME',
    'matchday': 'MATCHDAY',
    'attendance': 'ATTENDANCE',
    'knockout_game': 'KNOCKOUT_GAME',
    'last_updated_utc': 'LAST_UPDATED_UTC'
}

GAME_XGOAL_COLS = {
    'game_id': 'GAME_ID',
    'date_time_utc': 'DATE_TIME_UTC',
    'home_team_id': 'HOME_TEAM_ID',
    'home_goals': 'HOME_GOALS',
    'home_team_xgoals': 'HOME_TEAM_XGOALS',
    'home_player_xgoals': 'HOME_PLAYER_XGOALS',
    'away_team_id': 'AWAY_TEAM_ID',
    'away_goals': 'AWAY_GOALS',
    'away_team_xgoals': 'AWAY_TEAM_XGOALS',
    'away_player_xgoals': 'AWAY_PLAYER_XGOALS',
    'goal_difference': 'GOAL_DIFFERENCE',
    'team_xgoal_difference': 'TEAM_XGOAL_DIFFERENCE',
    'player_xgoal_difference': 'PLAYER_XGOAL_DIFFERENCE',
    'final_score_difference': 'FINAL_SCORE_DIFFERENCE',
    'home_xpoints': 'HOME_XPOINTS',
    'away_xpoints': 'AWAY_XPOINTS'
}

TEAM_COLS = {
    'team_id': 'TEAM_ID',
    'team_name': 'TEAM_NAME',
    'team_short_name': 'TEAM_SHORT_NAME',
    'team_abbreviation': 'TEAM_ABBREVIATION'
}

TEAM_SALARIES_COLS = {
    'team_id': 'TEAM_ID',
    'season_name': 'SEASON_NAME',
    'count_players': 'COUNT_PLAYERS',
    'total_guaranteed_compensation': 'TOTAL_GUARANTEED_COMPENSATION',
    'avg_guaranteed_compensation': 'AVG_GUARANTEED_COMPENSATION',
    'median_guaranteed_compensation': 'MEDIAN_GUARANTEED_COMPENSATION',
    'std_dev_guaranteed_compensation': 'STD_DEV_GUARANTEED_COMPENSATION'
}

PLAYER_COLS = {
    'player_id': 'PLAYER_ID',
    'player_name': 'PLAYER_NAME',
    'birth_date': 'BIRTH_DATE',
    'height_ft': 'HEIGHT_FT',
    'height_in': 'HEIGHT_IN',
    'weight_lb': 'WEIGHT_LB',
    'nationality': 'NATIONALITY',
    'primary_broad_position': 'PRIMARY_BROAD_POSITION',
    'primary_general_position': 'PRIMARY_GENERAL_POSITION',
    'start_season': 'START_SEASON',
    'end_season': 'END_SEASON'
}

MANAGER_COLS = {
    'manager_id': 'MANAGER_ID',
    'manager_name': 'MANAGER_NAME',
    'nationality': 'NATIONALiTY'
}

REFEREE_COLS = {
    'referee_id': 'REFEREE_ID',
    'referee_name': 'REFEREE_NAME',
    'birth_date': 'BIRTH_DATE',
    'nationality': 'NATIONALITY'
}

STADIUM_COLS = {
    'stadium_id': 'STADIUM_ID',
    'stadium_name': 'STADIUM_NAME',
    'capacity': 'CAPACITY',
    'year_built': 'YEAR_BUILT',
    'roof': 'ROOF',
    'turf': 'TURF',
    'street': 'STREET',
    'city': 'CITY',
    'province': 'PROVINCE',
    'country': 'COUNTRY',
    'postal_code': 'POSTAL_CODE',
    'latitude': 'LATITUDE',
    'longitude': 'LONGITUDE',
    'field_x': 'FIELD_X',
    'field_y': 'FIELD_Y'
}

def clean_data_and_transform(df_raw, key_cols):
    """
    Clean data and transform to Azure DB table format.
    
    Add more cleaning steps as needed.
    """
    df_output = df_raw.copy()
    
    # Drop rows with missing key_cols
    df_output = df_output.dropna(subset=key_cols)
    
    # Remove duplicates
    df_output = df_output.drop_duplicates(subset=key_cols)
    
    # Convert all NaN values to None as Azure DB does not support NaN
    df_output = df_output.replace({np.nan: None})
    
    return df_output
    

def set_cols(df_raw, cols):
    """
    Rename columns and remove unnecessary columns
    """
    for i in cols:
        if i not in df_raw:
            df_raw[i] = None
    df_output = df_raw.rename(columns=cols)
    df_output = df_output[list(cols.values())]

    return df_output

def load_games(start_date=None, end_date=None, year=None, game_id=None):
    """
    Load games data from ASA API to Azure DB
    """
    if start_date and end_date:
        logging.info(f"Loading games for the date range: {start_date} to {end_date}")
        with AzureDBConn() as conn:            
            # Get game_ids for the given date range
            # The BASE_URL/games endpoint does not support date range filtering but BASE_URL/games_xgoals does
            # So, we will get the updated game_ids from MLS.GAMES_XGOALS table
            # And then get the games data from BASE_URL/games endpoint using the game_ids
            query = f"""
                    SELECT 
                        DISTINCT GAME_ID
                    FROM MLS.GAMES_XGOALS
                    WHERE DATE_TIME_UTC BETWEEN '{start_date}' AND '{end_date}'
                    """
            games = conn.executemany(query)
            game_ids = [game[0] for game in games]

        df_games = pd.DataFrame()
        if len(game_ids) > 0:
            for game_id in game_ids:
                df_game = get_games(game_id=game_id)
                df_games = pd.concat([df_games, df_game])
    else:
        logging.info(f"Loading games...")
        df_games = get_games(year=year,game_id=game_id)
        
    df_games = set_cols(df_games, GAME_COLS)
    
    # Convert DATE_TIME_UTC and LAST_UPDATED_UTC to datetime
    df_games['DATE_TIME_UTC'] = pd.to_datetime(df_games['DATE_TIME_UTC'])
    df_games['LAST_UPDATED_UTC'] = pd.to_datetime(df_games['LAST_UPDATED_UTC'])
    
    # clean data and transform
    logging.info(f"Cleaning and transforming data...")
    df_games = clean_data_and_transform(df_games, ['GAME_ID'])
    
    if len(df_games) > 0:
        # Load data to Azure DB
        logging.info(f"Connecting to Azure DB...")
        with AzureDBConn() as conn:
            logging.info(f"Inserting data to GAMES table...")
            conn.insert_dataframe_to_staging(df_games, 'GAMES')
            logging.info(f"Data inserted successfully to GAMES table.")

    logging.info(f"Games loaded successfully.")


def load_game_xgoals(start_date=None, end_date=None, year=None, game_id=None):
    """
    Load game xgoals data from ASA API to Azure DB
    """
    logging.info(f"Loading game xgoals...")
    df_xgoals = get_game_xgoals(start_date, end_date, year, game_id)
    # Rename columns to match the Azure DB table columns
    df_xgoals = set_cols(df_xgoals, GAME_XGOAL_COLS)
    
    # Convert DATE_TIME_UTC to datetime
    df_xgoals['DATE_TIME_UTC'] = pd.to_datetime(df_xgoals['DATE_TIME_UTC'])

    # clean data and transform
    logging.info(f"Cleaning and transforming data...")
    df_xgoals = clean_data_and_transform(df_xgoals, ['GAME_ID'])
    
    if len(df_xgoals) > 0:
        # Load data to Azure DB
        logging.info(f"Connecting to Azure DB...")
        with AzureDBConn() as conn:
            logging.info(f"Inserting data to GAME_XGOALS table...")
            conn.insert_dataframe_to_staging(
                df=df_xgoals,
                table_name = 'GAMES_XGOALS'
            )
            logging.info(f"Data inserted successfully to GAME_XGOALS table.")
    
    logging.info(f"Game xgoals loaded successfully.")

def load_teams(team_id=None):
    """
    Load teams data from ASA API to Azure DB
    """
    logging.info(f"Loading teams...")
    df_teams = get_teams(team_id)
    df_teams = set_cols(df_teams, TEAM_COLS)
    
    # clean data and transform
    logging.info(f"Cleaning and transforming data...")
    df_teams = clean_data_and_transform(df_teams, ['TEAM_ID'])
    
    if len(df_teams) > 0:
        # Load data to Azure DB
        logging.info(f"Connecting to Azure DB...")
        with AzureDBConn() as conn:
            logging.info(f"Inserting data to TEAMS table...")
            conn.insert_dataframe_to_staging(df_teams, 'TEAMS')
            logging.info(f"Data inserted successfully to TEAMS table.")
            
    logging.info(f"Teams loaded successfully.")
    
def load_team_salaries(split_by='teams', year=None, team_id=None):
    """
    Load team salaries data from ASA API to Azure DB
    """
    logging.info(f"Loading team salaries...")
    df_salaries = get_team_salaries(split_by, year, team_id)
    df_salaries = set_cols(df_salaries, TEAM_SALARIES_COLS)

    # clean data and transform
    logging.info(f"Cleaning and transforming data...")
    df_salaries = clean_data_and_transform(df_salaries, ['TEAM_ID', 'SEASON_NAME'])
    
    if len(df_salaries) > 0:
        # Load data to Azure DB
        logging.info(f"Connecting to Azure DB...")
        with AzureDBConn() as conn:
            logging.info(f"Inserting data to TEAMS_SALARIES table...")
            conn.insert_dataframe_to_staging(df_salaries, 'TEAMS_SALARIES')
            logging.info(f"Data inserted successfully to TEAMS_SALARIES table.")
    
    logging.info(f"Team salaries loaded successfully.")

def load_players(player_id=None):
    """
    Load players data from ASA API to Azure DB
    """
    df = get_players(player_id)
    
    if len(df) > 0:
        # Load data to Azure DB
        pass

def load_managers():
    """
    Load managers data from ASA API to Azure DB
    """
    logging.info(f"Loading managers...")
    df_managers = get_managers()
    df_managers = set_cols(df_managers, MANAGER_COLS)
    
    # clean data and transform
    logging.info(f"Cleaning and transforming data...")
    df_managers = clean_data_and_transform(df_managers, ['MANAGER_ID'])
    
    if len(df_managers) > 0:
        # Load data to Azure DB
        logging.info(f"Connecting to Azure DB...")
        with AzureDBConn() as conn:
            logging.info(f"Inserting data to MANAGERS table...")
            conn.insert_dataframe_to_staging(df_managers, 'MANAGERS')
            logging.info(f"Data inserted successfully to MANAGERS table.")
        
    logging.info(f"Managers loaded successfully.")

def load_referees():
    """
    Load referees data from ASA API to Azure DB
    """
    logging.info(f"Loading referees...")
    df_refrees = get_referees()
    df_refrees = set_cols(df_refrees, REFEREE_COLS)
    
    # clean data and transform
    logging.info(f"Cleaning and transforming data...")
    df_refrees = clean_data_and_transform(df_refrees, ['REFEREE_ID'])
    
    if len(df_refrees) > 0:
        # Load data to Azure DB
        logging.info(f"Connecting to Azure DB...")
        with AzureDBConn() as conn:
            logging.info(f"Inserting data to REFEREES table...")
            conn.insert_dataframe_to_staging(df_refrees, 'REFEREES')
            logging.info(f"Data inserted successfully to REFEREES table.")

    logging.info(f"Referees loaded successfully.")

def load_stadiums():
    """
    Load stadiums data from ASA API to Azure DB
    """
    logging.info(f"Loading stadiums...")
    df_stadiums = get_stadiums()
    df_stadiums = set_cols(df_stadiums, STADIUM_COLS)
    
    # clean data and transform
    logging.info(f"Cleaning and transforming data...")
    df_stadiums = clean_data_and_transform(df_stadiums, ['STADIUM_ID'])
    
    if len(df_stadiums) > 0:
        # Load data to Azure DB
        logging.info(f"Connecting to Azure DB...")
        with AzureDBConn() as conn:
            logging.info(f"Inserting data to STADIUMS table...")
            conn.insert_dataframe_to_staging(df_stadiums, 'STADIUMS')
            logging.info(f"Data inserted successfully to STADIUMS table.")
            
    logging.info(f"Stadiums loaded successfully.")

def load(start_date, end_date):
    """
    Load all data from ASA API to Azure DB
    """
    logging.info(f"Loading games data for the date range: {start_date} to {end_date}")
    load_game_xgoals(start_date, end_date)
    load_games(start_date, end_date)
    logging.info(f"Loaded games data for the date range: {start_date} to {end_date}")

def historical_load(year):
    """
    Load historical data from ASA API to Azure DB
    """
    logging.info(f"Loading historical data for the year: {year}")
    load_games(year=year)
    load_game_xgoals(year=year)
    load_team_salaries(year=year)
    # load_player_salaries(year=year)
    logging.info(f"Loaded historical data for the year: {year}")

def load_all():
    """
    Load all data from ASA API to Azure DB
    """
    logging.info(f"Loading all data...")
    load_games()
    load_game_xgoals()
    load_teams()
    load_team_salaries()
    # load_players()
    load_managers()
    load_referees()
    load_stadiums()
    logging.info(f"Loaded all data.")