# Player Metrics: 
This repository contains the source code for the <em>#StrictlyBytheNumbers</em> PlayerMetric module. The PlayerMetric module attempts to provide key player metrics that could be then leveraged in a variety ways for a multitude of downstream baskebtall applications. 

## Installation:

- 1.) Install python package depedencies.
```shell
$ pip install strictly-metric
```

## Example Usage:

```python
from player_metric import player_metric

player_object = player_metric.PlayerMetric(df_all=df_all, df_boxscore=df_boxscore)

#Calculate aggregate and per game metrics for the player.

player_object.calculate_aggregate_metric()
player_object.calculate_per_game_metric()

#Examine transformed data 
player_object.df_all.head()
player_object.df_boxscore.head()
```
