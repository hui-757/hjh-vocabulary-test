import sys, os, json, uuid
sys.path.insert(0, os.getcwd())

from api.app import create_app
from api.record_models import RecordManager, get_db_connection

app = create_app()
client = app.test_client()

# 1. 先注册一个测试用户
register_data = {
    'username': 'testuser_debug',
    'password': '123456',
    'nickname': 'TestUser'
}
resp = client.post('/api/register', data=json.dumps(register_data), content_type='application/json')
print('Register:', resp.status_code, resp.get_json())

# 2. 登录获取 token
login_data = {'username': 'testuser_debug', 'password': '123456'}
resp = client.post('/api/login', data=json.dumps(login_data), content_type='application/json')
login_result = resp.get_json()
print('Login:', resp.status_code, login_result)
token = login_result.get('token', '')
print('Token:', token[:20] + '...')

# 3. 保存测试记录
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
save_data = {
    'result': {
        'correctRate': 60.0,
        'vocabularySize': 3500,
        'correctCount': 30,
        'totalAnswered': 50,
        'level': '高中水平'
    },
    'wrongAnswers': [
        {'word': 'apple', 'correct': '苹果', 'level': '小学', 'difficulty': 1},
        {'word': 'banana', 'correct': '香蕉', 'level': '小学', 'difficulty': 2}
    ]
}
resp = client.post('/api/records', data=json.dumps(save_data), headers=headers, content_type='application/json')
print('Save record:', resp.status_code, resp.get_json())

# 4. 获取测试记录
resp = client.get('/api/records', headers=headers)
print('Get records:', resp.status_code, resp.get_json())

# 5. 获取错题本
resp = client.get('/api/mistakes/personal', headers=headers)
print('Get personal mistakes:', resp.status_code, resp.get_json())

# 6. 检查数据库
conn = get_db_connection()
cur = conn.cursor()
for t in ['exam_records', 'personal_mistakes', 'global_mistakes']:
    cur.execute(f'SELECT COUNT(*) FROM {t}')
    print(f'DB {t}: {cur.fetchone()[0]} rows')
conn.close()
