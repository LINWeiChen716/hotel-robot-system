import sys

sys.path.insert(0, 'services')

from services import repo
from services.pudu_client import call_pudu


def main():
    store = repo.get_or_create_default_store()
    sid = store['id']
    robots = repo.list_robots(sid)
    by = {str(x.get('nickname') or '').strip(): x.get('sn') for x in robots}

    print('=== recharge test ===')
    pairs = [
        ('豆豆', '/open-platform-service/v2/recharge'),
        ('高高', '/open-platform-service/v2/recharge'),
        ('喵喵', '/open-platform-service/v2/recharge'),
        ('託託', '/open-platform-service/v1/recharge'),
        ('轉轉', '/open-platform-service/v2/recharge'),
        ('閃閃', '/open-platform-service/v2/recharge'),
    ]
    for nick, path in pairs:
        res = call_pudu('GET', path, query={'sn': by[nick]}, timeout=12)
        print(nick, path, res.get('status_code'), (res.get('json') or {}).get('message'))

    print('\n=== call test ===')
    for nick in ['豆豆', '高高', '喵喵', '託託', '轉轉', '閃閃']:
        body = {
            'sn': by[nick],
            'point': f'{nick}待機點',
            'map_name': '1#1#內湖展間v20',
            'point_type': 'table',
        }
        res = call_pudu('POST', '/open-platform-service/v1/custom_call', body=body, timeout=12)
        print(nick, '/open-platform-service/v1/custom_call', res.get('status_code'), (res.get('json') or {}).get('message'))

    print('\n=== clean return test ===')
    for nick in ['聰聰', '讓讓']:
        body = {
            'sn': by[nick],
            'type': 6,
            'clean': {'status': 1},
        }
        res = call_pudu('POST', '/cleanbot-service/v1/api/open/task/exec', body=body, timeout=12)
        print(nick, '/cleanbot-service/v1/api/open/task/exec', res.get('status_code'), (res.get('json') or {}).get('message'))


if __name__ == '__main__':
    main()
