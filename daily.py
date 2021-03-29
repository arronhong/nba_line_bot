from datetime import datetime
import json
from string import Template
from enum import Enum
from copy import deepcopy

import requests
import pytz


game_started_bubble_template = Template('''{
  "type": "bubble",
  "size": "giga",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "${game_status}",
            "align": "center"
          }
        ],
        "paddingAll": "xs"
      },
      {
        "type": "separator",
        "margin": "md"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "filler"
              },
              {
                "type": "text",
                "text": ">",
                "align": "center"
              },
              {
                "type": "filler"
              }
            ],
            "width": "20px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "filler"
              },
              {
                "type": "text",
                "text": "${home_team_name}"
              },
              {
                "type": "text",
                "text": "${away_team_name}"
              }
            ],
            "width": "40px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "filler"
              },
              {
                "type": "text",
                "text": "${home_team_wins}-${home_team_losses}",
                "size": "xxs",
                "offsetBottom": "8px"
              },
              {
                "type": "text",
                "text": "${away_team_wins}-${away_team_losses}",
                "size": "xxs",
                "offsetBottom": "3px"
              }
            ],
            "width": "45px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "Q1"
              },
              {
                "type": "text",
                "text": "${home_team_q1_score}"
              },
              {
                "type": "text",
                "text": "${away_team_q1_score}"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "Q2"
              },
              {
                "type": "text",
                "text": "${home_team_q2_score}"
              },
              {
                "type": "text",
                "text": "${away_team_q2_score}"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "Q3"
              },
              {
                "type": "text",
                "text": "${home_team_q3_score}"
              },
              {
                "type": "text",
                "text": "${away_team_q3_score}"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "Q4"
              },
              {
                "type": "text",
                "text": "${home_team_q4_score}"
              },
              {
                "type": "text",
                "text": "${away_team_q4_score}"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "Total"
              },
              {
                "type": "text",
                "text": "${home_team_total_score}"
              },
              {
                "type": "text",
                "text": "${away_team_total_score}"
              }
            ]
          }
        ],
        "margin": "md"
      },
      {
        "type": "separator",
        "margin": "md"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "filler"
              },
              {
                "type": "text",
                "text": "得分"
              },
              {
                "type": "text",
                "text": "籃板"
              },
              {
                "type": "text",
                "text": "助攻"
              }
            ],
            "width": "40px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "${home_team_name}"
              },
              {
                "type": "text",
                "text": "${home_team_point_leader}"
              },
              {
                "type": "text",
                "text": "${home_team_rebound_leader}"
              },
              {
                "type": "text",
                "text": "${home_team_assist_leader}"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "filler"
              },
              {
                "type": "text",
                "text": "${home_team_point_highest}"
              },
              {
                "type": "text",
                "text": "${home_team_rebound_highest}"
              },
              {
                "type": "text",
                "text": "${home_team_assist_highest}"
              }
            ],
            "width": "40px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "${away_team_name}"
              },
              {
                "type": "text",
                "text": "${away_team_point_leader}"
              },
              {
                "type": "text",
                "text": "${away_team_rebound_leader}"
              },
              {
                "type": "text",
                "text": "${away_team_assist_leader}"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "filler"
              },
              {
                "type": "text",
                "text": "${away_team_point_highest}"
              },
              {
                "type": "text",
                "text": "${away_team_rebound_highest}"
              },
              {
                "type": "text",
                "text": "${away_team_assist_highest}"
              }
            ],
            "width": "40px"
          }
        ],
        "margin": "md"
      }
    ]
  }
}''')
separator = {
    "type": "separator",
    "margin": "md"
}
game_in_progress_button_template = Template('''{
    "type": "button",
    "action":
    {
        "type": "postback",
        "label": "文字直播",
        "data": "testtest"
    }
}''')
game_not_started_bubble_template = Template('''{
  "type": "bubble",
  "size": "giga",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "將於 ${start_time} 開始",
            "align": "center"
          }
        ],
        "paddingAll": "xs"
      },
      {
        "type": "separator",
        "margin": "md"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "text",
            "text": "${home_team_name}",
            "align": "center"
          },
          {
            "type": "text",
            "text": "${home_team_wins}-${home_team_losses}",
            "align": "start",
            "size": "xxs",
            "offsetTop": "4px"
          },
          {
            "type": "separator",
            "color": "#000000"
          },
          {
            "type": "text",
            "text": "${away_team_wins}-${away_team_losses}",
            "align": "end",
            "size": "xxs",
            "offsetTop": "4px"
          },
          {
            "type": "text",
            "text": "${away_team_name}",
            "align": "center"
          }
        ],
        "margin": "md"
      }
    ]
  }
}''')
no_game_bubble_template = Template('''{
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "今日無比賽",
        "align": "center"
      },
      {
        "type": "separator",
        "margin": "md"
      },
      {
        "type": "text",
        "text": "下一場  ${next_game_date}",
        "align": "center",
        "margin": "md",
        "offsetTop": "sm"
      }
    ]
  }
}''')

class GameStatus(Enum):
    NOT_STARTED = '1'
    IN_PROGRESS = '2'
    OVER = '3'


def get_game_bubble(game):
    home_team_name = game['homeTeam']['profile']['name']
    home_team_wins = game['homeTeam']['matchup']['wins']
    home_team_losses = game['homeTeam']['matchup']['losses']
    away_team_name = game['awayTeam']['profile']['name']
    away_team_wins = game['awayTeam']['matchup']['wins']
    away_team_losses = game['awayTeam']['matchup']['losses']

    if game['boxscore']['status'] in (GameStatus.OVER.value,
                                      GameStatus.IN_PROGRESS.value):
        # statusDesc: 中場, 第一節
        game_status = game['boxscore']['statusDesc']
        if game['boxscore']['periodClock']:
            game_status += f" {game['boxscore']['periodClock']}"

        game_started_bubble = game_started_bubble_template.substitute(
            game_status=game_status,
            home_team_name=home_team_name,
            home_team_wins=home_team_wins,
            home_team_losses=home_team_losses,
            home_team_total_score=game['boxscore']['homeScore'],
            home_team_q1_score=game['homeTeam']['score']['q1Score'],
            home_team_q2_score=game['homeTeam']['score']['q2Score'],
            home_team_q3_score=game['homeTeam']['score']['q3Score'],
            home_team_q4_score=game['homeTeam']['score']['q4Score'],
            home_team_point_leader=game['homeTeam']['pointGameLeader']['profile']['displayName'],
            home_team_point_highest=game['homeTeam']['pointGameLeader']['statTotal']['points'],
            home_team_rebound_leader=game['homeTeam']['reboundGameLeader']['profile']['displayName'],
            home_team_rebound_highest=game['homeTeam']['reboundGameLeader']['statTotal']['rebs'],
            home_team_assist_leader=game['homeTeam']['assistGameLeader']['profile']['displayName'],
            home_team_assist_highest=game['homeTeam']['assistGameLeader']['statTotal']['assists'],
            away_team_name=away_team_name,
            away_team_wins=away_team_wins,
            away_team_losses=away_team_losses,
            away_team_total_score=game['boxscore']['awayScore'],
            away_team_q1_score=game['awayTeam']['score']['q1Score'],
            away_team_q2_score=game['awayTeam']['score']['q2Score'],
            away_team_q3_score=game['awayTeam']['score']['q3Score'],
            away_team_q4_score=game['awayTeam']['score']['q4Score'],
            away_team_point_leader=game['awayTeam']['pointGameLeader']['profile']['displayName'],
            away_team_point_highest=game['awayTeam']['pointGameLeader']['statTotal']['points'],
            away_team_rebound_leader=game['awayTeam']['reboundGameLeader']['profile']['displayName'],
            away_team_rebound_highest=game['awayTeam']['reboundGameLeader']['statTotal']['rebs'],
            away_team_assist_leader=game['awayTeam']['assistGameLeader']['profile']['displayName'],
            away_team_assist_highest=game['awayTeam']['assistGameLeader']['statTotal']['assists'],
        )
        game_started_bubble = json.loads(game_started_bubble)
        return game_started_bubble
        # if game['boxscore']['status'] == GameStatus.IN_PROGRESS.value:
        #     game_started_bubble['body']['contents'].extend([
        #         deepcopy(separator), game_in_progress_button_template
        #     ])

    elif game['boxscore']['status'] == GameStatus.NOT_STARTED.value:
        # 顯示開始時間

        game_not_started_bubble = game_not_started_bubble_template.substitute(
            start_time=datetime.fromtimestamp(
                int(game['profile']['utcMillis'])/1000,
                pytz.timezone('Asia/Taipei')).strftime('%H:%M'),
            home_team_name=home_team_name,
            home_team_wins=home_team_wins,
            home_team_losses=home_team_losses,
            away_team_name=away_team_name,
            away_team_wins=away_team_wins,
            away_team_losses=away_team_losses,
        )
        return json.loads(game_not_started_bubble)

    raise ValueError('unknown game status')


weekday_locale = ('星期天', '星期一','星期二', '星期三', '星期四', '星期五', '星期六')


def get_daily_carousel():
    daily_url = 'https://tw.global.nba.com/stats2/scores/daily.json'
    now = datetime.now(pytz.timezone('Asia/Taipei'))
    r = requests.get(daily_url, params={'gameDate': now.strftime('%Y-%m-%d'),
                                        'tz': '+8',
                                        'locale': 'zh_TW',
                                        'countryCode': 'TW'})
    r.raise_for_status()
    daily = r.json()
    if not daily['payload']['date']:
        next_game_date = datetime.fromtimestamp(
            int(daily['payload']['nextAvailableDateMillis']) / 1000)
        return json.loads(no_game_bubble_template.substitute(
            next_game_date=f'{next_game_date.strftime("%Y-%m-%d")} '
                           f'{weekday_locale[int(next_game_date.strftime("%w"))]}'))

    return {
        'type': 'carousel',
        'contents': [get_game_bubble(g) for g in daily['payload']['date']['games']]
    }
