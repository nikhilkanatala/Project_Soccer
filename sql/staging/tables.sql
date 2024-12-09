CREATE TABLE [STAGING].[GAMES](
	[GAME_ID] [NVARCHAR](MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[DATE_TIME_UTC] [NVARCHAR](MAX) NULL,
	[HOME_TEAM_ID] [NVARCHAR](MAX) NULL,
	[HOME_SCORE] [NVARCHAR](MAX) NULL,
	[AWAY_TEAM_ID] [NVARCHAR](MAX) NULL,
	[AWAY_SCORE] [NVARCHAR](MAX) NULL,
	[REFEREE_ID] [NVARCHAR](MAX) NULL,
	[STADIUM_ID] [NVARCHAR](MAX) NULL,
	[HOME_MANAGER_ID] [NVARCHAR](MAX) NULL,
	[AWAY_MANAGER_ID] [NVARCHAR](MAX) NULL,
	[EXPANDED_MINUTES] [NVARCHAR](MAX) NULL,
	[SEASON_NAME] [NVARCHAR](MAX) NULL,
	[MATCHDAY] [NVARCHAR](MAX) NULL,
	[ATTENDANCE] [NVARCHAR](MAX) NULL,
	[KNOCKOUT_GAME] [NVARCHAR](MAX) NULL,
	[LAST_UPDATED_UTC] [NVARCHAR](MAX) NULL,
	[CREATED] [DATETIME] DEFAULT GETDATE() NOT NULL
);

CREATE TABLE [STAGING].[GAMES_XGOALS](
	[GAME_ID] [NVARCHAR](MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[DATE_TIME_UTC] [NVARCHAR](MAX) NULL,
	[HOME_TEAM_ID] [NVARCHAR](MAX) NULL,
	[HOME_GOALS] [NVARCHAR](MAX) NULL,
	[HOME_TEAM_XGOALS] [NVARCHAR](MAX) NULL,
	[HOME_PLAYER_XGOALS] [NVARCHAR](MAX) NULL,
	[AWAY_TEAM_ID] [NVARCHAR](MAX) NULL,
	[AWAY_GOALS] [NVARCHAR](MAX) NULL,
	[AWAY_TEAM_XGOALS] [NVARCHAR](MAX) NULL,
	[AWAY_PLAYER_XGOALS] [NVARCHAR](MAX) NULL,
	[GOAL_DIFFERENCE] [NVARCHAR](MAX) NULL,
	[TEAM_XGOAL_DIFFERENCE] [NVARCHAR](MAX) NULL,
	[PLAYER_XGOAL_DIFFERENCE] [NVARCHAR](MAX) NULL,
	[FINAL_SCORE_DIFFERENCE] [NVARCHAR](MAX) NULL,
	[HOME_XPOINTS] [NVARCHAR](MAX) NULL,
	[AWAY_XPOINTS] [NVARCHAR](MAX) NULL,
	[CREATED] [DATETIME] DEFAULT GETDATE() NOT NULL
);

CREATE TABLE [STAGING].[TEAMS](
	[TEAM_ID] [NVARCHAR](MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[TEAM_NAME] [NVARCHAR](MAX) NULL,
	[TEAM_SHORT_NAME] [NVARCHAR](MAX) NULL,
	[TEAM_ABBREVIATION] [NVARCHAR](MAX) NULL,
	[CREATED] [DATETIME] DEFAULT GETDATE() NOT NULL
);

CREATE TABLE [STAGING].[TEAMS_SALARIES](
	[TEAM_ID] [NVARCHAR](MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[SEASON_NAME] [NVARCHAR](MAX) NOT NULL,
	[COUNT_PLAYERS] [NVARCHAR](MAX) NOT NULL,
	[TOTAL_GUARANTEED_COMPENSATION] [NVARCHAR](MAX) NOT NULL,
	[AVG_GUARANTEED_COMPENSATION] [NVARCHAR](MAX) NOT NULL,
	[MEDIAN_GUARANTEED_COMPENSATION] [NVARCHAR](MAX) NOT NULL,
	[STD_DEV_GUARANTEED_COMPENSATION] [NVARCHAR](MAX) NOT NULL,
	[CREATED_AT] [DATETIME] DEFAULT GETDATE() NOT NULL
);

CREATE TABLE [STAGING].[MANAGERS](
	[MANAGER_ID] [NVARCHAR](MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[MANAGER_NAME] [NVARCHAR](MAX) NULL,
	[NATIONALITY] [NVARCHAR](MAX) NULL,
	[CREATED] [DATETIME] DEFAULT GETDATE() NOT NULL
);

CREATE TABLE [STAGING].[REFEREES](
	[REFEREE_ID] [NVARCHAR](MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[REFEREE_NAME] [NVARCHAR](MAX) NULL,
	[BIRTH_DATE] [NVARCHAR](MAX) NULL,
	[NATIONALITY] [NVARCHAR](MAX) NULL,
	[CREATED] [DATETIME] DEFAULT GETDATE() NOT NULL
);

CREATE TABLE [STAGING].[STADIUMS](
	[STADIUM_ID] [NVARCHAR](MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[STADIUM_NAME] [NVARCHAR](MAX) NULL,
	[CAPACITY] [NVARCHAR](MAX) NULL,
	[YEAR_BUILT] [NVARCHAR](MAX) NULL,
	[ROOF] [NVARCHAR](MAX) NULL,
	[TURF] [NVARCHAR](MAX) NULL,
	[STREET] [NVARCHAR](MAX) NULL,
	[CITY] [NVARCHAR](MAX) NULL,
	[PROVINCE] [NVARCHAR](MAX) NULL,
	[COUNTRY] [NVARCHAR](MAX) NULL,
	[POSTAL_CODE] [NVARCHAR](MAX) NULL,
	[LATITUDE] [NVARCHAR](MAX) NULL,
	[LONGITUDE] [NVARCHAR](MAX) NULL,
	[FIELD_X] [NVARCHAR](MAX) NULL,
	[FIELD_Y] [NVARCHAR](MAX) NULL,
	[CREATED_DATE] [DATETIME] DEFAULT GETDATE() NOT NULL
);