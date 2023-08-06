import pandas as pd 

def touches(df_boxscore):
    '''
    Touches estimate the number of times a player touched the ball in an attacking position on the floor. 
    The theory behind the formula is that once a player gets the ball, he can only do one of four things (aside from dribbling, of course):
        - pass 
        - shoot
        - draw a foul
        - commit a turnover
    Touches Formula=Field Goal Attempts + Turnovers + (Free Throw Attempts / (Team’s Free Throw Attempts/Opponents Personal Fouls)) + (Assists/0.17)
    '''

    # helper function
    def compute_touches(row):
        current_game_id = row['game_id']
        current_team = row['team_id']

        home_team_metric = df_groupby[(df_groupby['game_id'] == current_game_id) & (df_groupby['team_id'] == current_team)]
        away_team_metric = df_groupby[(df_groupby['game_id'] == current_game_id) & (df_groupby['team_id'] != current_team)]
        
        try:
            return row['fga'] + row['tov'] \
                + (row['fta'] / (home_team_metric['fga'].to_list()[0] / away_team_metric['pf'].to_list()[0]) + row['ast']/0.17)
        except:
            return 0.0

    # Touches Formula=Field Goal Attempts + Turnovers + (Free Throw Attempts / (Team’s Free Throw Attempts/Opponents Personal Fouls)) + (Assists/0.17)
    df_groupby = df_boxscore.groupby(['game_id', 'team_id']).sum().reset_index()
    df_boxscore['touches'] = df_boxscore.apply(lambda row: compute_touches(row), axis=1) 

    return df_boxscore

def versatility_index(df_boxscore): 
    '''
    Versatility Index, which is invented by John Hollinger, is a metric that measures a player’s ability to produce in more than one statistic.
    The metric uses points, assists, and rebounds. The average player will score around a five on the index, while top players score above 10.
    '''
    df_boxscore['versatility_index'] = pow(df_boxscore['pts']* df_boxscore['trb']*df_boxscore['ast'],0.33)
    return df_boxscore

def non_scoring_possessions(df_boxscore):
    '''
    Non-scoring player possessions would be a player’S missed field goals, plus free throws that weren’t rebounded by his team, plus his turnovers.
    '''
    df_boxscore['non_scoring_pos'] = df_boxscore['fga']- df_boxscore['fg'] +0.4*df_boxscore['fta']+df_boxscore['tov']
    return df_boxscore

def scoring_possessions(df_boxscore):
    '''
    Scoring player possessions would be the player’s field goals that weren’t assisted on, plus a certain percentage of his field goals that were assisted on,
    plus a certain percentage of his assists, plus his free throws made.

    Scoring Possessions Formula=(Field Goals Made) – 0.37*(Field Goals Made)*Q/R + 0.37*(Player Assists) + 0.5*(Free Throws Made)
    
    where;
        Q=5*(Player Minutes)*(Team Assist Total)/(Team Total Minutes)-(Player Assists)
        R=5*(Player Minutes)*(Team Field Goals Made)/(Team Minutes)-(Player Assists)
    '''
    def replace_string_with_zero(row):
        try:
            return float(row)
        except:
            return "0.0"

    def compute_scoring_pos(row):
        current_game_id = row['game_id']
        current_team = row['team_id']

        home_team_metric = df_groupby[(df_groupby['game_id'] == current_game_id) & (df_groupby['team_id'] == current_team)]
        away_team_metric = df_groupby[(df_groupby['game_id'] == current_game_id) & (df_groupby['team_id'] != current_team)]
        try:
            Q =(row['mins_played']*home_team_metric['ast'].to_list()[0])/(home_team_metric['mins_played'].to_list()[0]-row['ast'])
            R =(row['mins_played']*home_team_metric['fg'].to_list()[0])/(home_team_metric['mins_played'].to_list()[0]-row['ast'])

            return row['fg'] -  0.37*row['fg']*Q/R + 0.37*row['ast']+0.5*row['ft']
        except:
            return None
            
    df_boxscore['mins_played'] = df_boxscore['mp'].apply(lambda x: replace_string_with_zero(x.split(":")[0])).astype(float)
    df_groupby = df_boxscore.groupby(['game_id', 'team_id']).sum().reset_index()
    df_boxscore['scoring_pos'] = df_boxscore.apply(lambda row: compute_scoring_pos(row), axis=1) 

    return df_boxscore

def win_score(df_boxscore):
    '''
    Win Score is David Berri’s metric that indicates the relative value of a player’s points,rebounds, steals, turnovers, and field goal attempts.
    '''
    df_boxscore['win_score'] = df_boxscore['pts']+df_boxscore['trb']+df_boxscore['stl']+0.5*df_boxscore['ast']+ \
        0.5*df_boxscore['blk']-df_boxscore['fga']-df_boxscore['tov']-0.5*df_boxscore['fta']-0.5*df_boxscore['pf']

    return df_boxscore


def individual_floor_percentage(df_boxscore):
    '''
    Individual Floor Percentage is a metric that indicates the ratio of a player’s scoring possessions by his total possessions.
    When a player ends his team’s possession, it would be a possession charged to him. This gives the player’s total possessions.
    When a player scored or assisted on a score, a scoring possession would be charged to him.

    Individual Floor Percentage Formula=100*(Player’s Scoring Possessions)/(Player’s Total Possessions)
    '''
    df_boxscore['indiv_floor_percent'] = 100*df_boxscore['scoring_pos']/df_boxscore['non_scoring_pos']+df_boxscore['scoring_pos']

    return df_boxscore 

def defensive_versatility_idx(df_boxscore):
    '''
    Defensive Versatility Index is a novel metric by StrictBytheNumbers, which attempts to quantify the ability of a player
    to produce in more than more defensive statistic.
    '''
    df_boxscore['def_versatility_index'] = pow(df_boxscore['blk']* df_boxscore['stl']*df_boxscore['drb'],0.33) - 2*df_boxscore['pf']

    return df_boxscore

def player_impact_estimate(df_boxscore):
    '''
    Player Impact Estimate aka PIE is a metric to gauge a player’s all-around contribution to the game. 
    Almost all statistical categories in the box score are involved in the PIE formula.
    '''
    df_boxscore.reset_index(inplace=True)
    df_filtered = df_boxscore.groupby('game_id').sum().reset_index().drop(['starter'],axis=1)
    df_joined = df_filtered.merge(df_boxscore,how='left',on='game_id',suffixes=['_game','_p'])
    
    
    df_boxscore['pie']= (df_joined['pts_p'] + df_joined['fg_p'] + df_joined['ft_p'] - df_joined['fga_p'] - df_joined['fta_p'] \
       + df_joined['drb_p']+ 0.5*df_joined['drb_p'] + df_joined['ast_p']+ df_joined['stl_p']+ 0.5*df_joined['blk_p']+ df_joined['pf_p']+ df_joined['tov_p']) \
       /(df_joined['pts_game'] + df_joined['fg_game'] + df_joined['ft_game'] - df_joined['fga_game'] - df_joined['fta_game'] \
         + df_joined['drb_game']+ 0.5*df_joined['drb_game'] + df_joined['ast_game']+ df_joined['stl_game']+ 0.5*df_joined['blk_game']+ df_joined['pf_game']+ df_joined['tov_game'])

    return df_boxscore 

