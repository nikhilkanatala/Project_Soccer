CREATE TABLE [MLS].[GAMES](
	[GAME_ID] [NVARCHAR](50) COLLATE SQL_Latin1_General_CP1_CI_AS PRIMARY KEY,
	[DATE_TIME_UTC] [DATETIMEOFFSET](7) NULL,
	[HOME_SCORE] [INT] NULL,
	[AWAY_SCORE] [INT] NULL,
	[HOME_TEAM_ID] [NVARCHAR](50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[AWAY_TEAM_ID] [NVARCHAR](50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[REFEREE_ID] [NVARCHAR](50) NULL,
	[STADIUM_ID] [NVARCHAR](50) NULL,
	[HOME_MANAGER_ID] [NVARCHAR](50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[AWAY_MANAGER_ID] [NVARCHAR](50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[EXPANDED_MINUTES] [INT] NULL,
	[SEASON_NAME] [NVARCHAR](10) NULL,
	[MATCHDAY] [INT] NULL,
	[ATTENDANCE] [INT] NULL,
	[KNOCKOUT_GAME] [BIT] NULL,
	[LAST_UPDATED_UTC] [DATETIMEOFFSET](7) NULL,
	[CREATED] [DATETIME] DEFAULT GETDATE() NOT NULL
);

CREATE TABLE [MLS].[GAMES_XGOALS](
	[GAME_ID] [NVARCHAR](50) COLLATE SQL_Latin1_General_CP1_CI_AS PRIMARY KEY,
	[DATE_TIME_UTC] [DATETIMEOFFSET](7) NULL,
	[HOME_TEAM_ID] [NVARCHAR](50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[HOME_GOALS] [INT] NULL,
	[HOME_TEAM_XGOALS] [DECIMAL](10, 4) NULL,
	[HOME_PLAYER_XGOALS] [DECIMAL](10, 4) NULL,
	[AWAY_TEAM_ID] [NVARCHAR](50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[AWAY_GOALS] [INT] NULL,
	[AWAY_TEAM_XGOALS] [DECIMAL](10, 4) NULL,
	[AWAY_PLAYER_XGOALS] [DECIMAL](10, 4) NULL,
	[GOAL_DIFFERENCE] [INT] NULL,
	[TEAM_XGOAL_DIFFERENCE] [DECIMAL](10, 4) NULL,
	[PLAYER_XGOAL_DIFFERENCE] [DECIMAL](10, 4) NULL,
	[FINAL_SCORE_DIFFERENCE] [INT] NULL,
	[HOME_XPOINTS] [DECIMAL](10, 4) NULL,
	[AWAY_XPOINTS] [DECIMAL](10, 4) NULL,
	[CREATED] [DATETIME] DEFAULT GETDATE() NOT NULL
);

CREATE TABLE [MLS].[TEAMS](
	[TEAM_ID] [NVARCHAR](50) COLLATE SQL_Latin1_General_CP1_CI_AS PRIMARY KEY,
	[TEAM_NAME] [VARCHAR](100) NULL,
	[TEAM_SHORT_NAME] [VARCHAR](50) NULL,
	[TEAM_ABBREVIATION] [VARCHAR](5) NULL,
	[CREATED] [DATETIME] DEFAULT GETDATE() NOT NULL
);


CREATE TABLE [MLS].[TEAMS_SALARIES](
	[TEAM_ID] [NVARCHAR](50) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[SEASON_NAME] [INT] NOT NULL,
	[COUNT_PLAYERS] [INT] NOT NULL,
	[TOTAL_GUARANTEED_COMPENSATION] [FLOAT] NOT NULL,
	[AVG_GUARANTEED_COMPENSATION] [FLOAT] NOT NULL,
	[MEDIAN_GUARANTEED_COMPENSATION] [FLOAT] NOT NULL,
	[STD_DEV_GUARANTEED_COMPENSATION] [FLOAT] NOT NULL,
	[CREATED_AT] [DATETIME] DEFAULT GETDATE() NOT NULL,
	PRIMARY KEY ([TEAM_ID], [SEASON_NAME])
);


CREATE TABLE [MLS].[MANAGERS](
	[MANAGER_ID] [NVARCHAR](50) COLLATE SQL_Latin1_General_CP1_CI_AS PRIMARY KEY,
	[MANAGER_NAME] [VARCHAR](144) NULL,
	[NATIONALITY] [VARCHAR](100) NULL,
	[CREATED] [DATETIME] DEFAULT GETDATE() NOT NULL
);

CREATE TABLE [MLS].[REFEREES](
	[REFEREE_ID] [NVARCHAR](50) COLLATE SQL_Latin1_General_CP1_CI_AS PRIMARY KEY,
	[REFEREE_NAME] [VARCHAR](144) NULL,
	[BIRTH_DATE] [DATE] NULL,
	[NATIONALITY] [VARCHAR](100) NULL,
	[CREATED] [DATETIME] DEFAULT GETDATE() NOT NULL
);

CREATE TABLE [MLS].[STADIUMS](
	[STADIUM_ID] [NVARCHAR](50) COLLATE SQL_Latin1_General_CP1_CI_AS PRIMARY KEY,
	[STADIUM_NAME] [VARCHAR](255) NULL,
	[CAPACITY] [INT] NULL,
	[YEAR_BUILT] [INT] NULL,
	[ROOF] [BIT] NULL,
	[TURF] [BIT] NULL,
	[STREET] [VARCHAR](255) NULL,
	[CITY] [VARCHAR](255) NULL,
	[PROVINCE] [VARCHAR](255) NULL,
	[COUNTRY] [VARCHAR](255) NULL,
	[POSTAL_CODE] [VARCHAR](10) NULL,
	[LATITUDE] [FLOAT] NULL,
	[LONGITUDE] [FLOAT] NULL,
	[FIELD_X] [FLOAT] NULL,
	[FIELD_Y] [FLOAT] NULL,
	[CREATED_DATE] [DATETIME] DEFAULT GETDATE() NOT NULL
);
