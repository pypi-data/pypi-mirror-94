from kks.ejudge import Standings, TaskInfo, StandingsRow, TaskScore
from kks.util.ejudge import load_auth_data

# KKS_STAT_API = 'https://kks.darkkeks.me/api'
KKS_STAT_API = 'http://localhost:8080/api'


def send_standings(standings):
    import requests
    from requests import RequestException

    data = {}
    data.update(standings_to_dict(standings))

    auth_data = load_auth_data()
    if auth_data:
        data.update({
            'contest_id': auth_data.contest_id,
            'login': auth_data.login,
        })

    try:
        response = requests.post(f"{KKS_STAT_API}/send", json=data)
        return response.ok
    except RequestException:
        return False


def get_global_standings():
    import requests

    response = requests.get(f"{KKS_STAT_API}/get")
    if not response.ok:
        return None

    json_response = response.json()
    return standings_from_dict(json_response['standings'])


def standings_to_dict(standings):
    return {
        'standings': {
            'tasks': [{
                'contest': task.contest,
                'name': task.name,
            } for task in standings.tasks],
            'rows': [{
                'place': row.place,
                'user': row.user,
                'tasks': [{
                    'score': task.score,
                    'status': task.status,
                } for task in row.tasks],
                'solved': row.solved,
                'score': row.score,
                'is_self': row.is_self,
            } for row in standings.rows],
        }
    }


def standings_from_dict(standings):
    tasks = standings['tasks']
    rows = standings['rows']
    for row in rows:
        for task, row_task in zip(tasks, row['tasks']):
            row_task['contest'] = task['contest']

    return Standings(
        tasks=[
            TaskInfo(task['name'], task['contest'])
            for task in tasks
        ],
        rows=[
            StandingsRow(row['place'], row['user'], [
                TaskScore(task['contest'], task['score'], task['status'])
                for task in row['tasks']
            ], row['solved'], row['score'], row['is_self'])
            for row in standings['rows']
        ],
    )
