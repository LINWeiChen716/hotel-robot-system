import sys
sys.path.insert(0, "services")
from services import repo

MAP_NAME = "1#1#內湖展間v20"
store = repo.get_or_create_default_store(); sid = store['id']
robots = repo.list_robots(sid)
by = {str(r.get('nickname') or '').strip(): r for r in robots}

for b in repo.list_buttons(sid):
    repo.delete_button(b['id'])
for a in repo.list_action_templates(sid):
    repo.delete_action_template(a['id'])

for nick in ['豆豆','高高','喵喵','託託','轉轉','閃閃']:
    sn = by[nick]['sn']
    repo.create_action_template(sid, {
        'name': f'呼叫任務-{nick}',
        'method': 'POST',
        'path': '/open-platform-service/v1/custom_call',
        'query_template': {},
        'body_template': {'sn': sn, 'point': f'{nick}待機點', 'map_name': MAP_NAME, 'point_type': 'table'},
        'timeout_ms': 20000,
        'is_enabled': True,
    })

for nick in ['豆豆','高高','喵喵','託託','轉轉','閃閃']:
    sn = by[nick]['sn']
    path = '/open-platform-service/v1/recharge' if nick == '託託' else '/open-platform-service/v2/recharge'
    repo.create_action_template(sid, {
        'name': f'一鍵回充-{nick}',
        'method': 'GET',
        'path': path,
        'query_template': {'sn': sn},
        'body_template': {},
        'timeout_ms': 20000,
        'is_enabled': True,
    })

for nick in ['聰聰','讓讓']:
    sn = by[nick]['sn']
    repo.create_action_template(sid, {
        'name': f'清潔返航-{nick}',
        'method': 'POST',
        'path': '/cleanbot-service/v1/api/open/task/exec',
        'query_template': {},
        'body_template': {'sn': sn, 'type': 6, 'clean': {'status': 1}},
        'timeout_ms': 20000,
        'is_enabled': True,
    })

a = repo.list_action_templates(sid)
id_map = {x.get('name'): x.get('id') for x in a}

def make_button(name, action_names, order):
    b = repo.create_button(sid, name=name, description=name, sort_order=order)
    tids = [id_map[n] for n in action_names if id_map.get(n)]
    repo.set_button_actions(b['id'], tids)

make_button('運送展示', [f'呼叫任務-{n}' for n in ['豆豆','高高','喵喵','託託','轉轉','閃閃']], 10)
make_button('一鍵回充', [f'一鍵回充-{n}' for n in ['豆豆','高高','喵喵','託託','轉轉','閃閃']], 20)
make_button('清潔展示', [f'清潔返航-{n}' for n in ['聰聰','讓讓']], 30)

print('ACTIONS', len(repo.list_action_templates(sid)))
buttons = repo.list_buttons(sid)
print('BUTTONS', len(buttons))
for b in buttons:
    print((b.get('name') or '').encode('unicode_escape').decode('ascii'), len(b.get('actions') or []))
