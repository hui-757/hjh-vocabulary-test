import sys, os, json, traceback
sys.path.insert(0, os.getcwd())

from api.app import create_app
from api.routes.auth import token_store

app = create_app()
client = app.test_client()

# 1. 登录获取 token
login_data = {'username': 'huajianghui', 'password': '123456'}
resp = client.post('/api/login', data=json.dumps(login_data), content_type='application/json')
print('Login:', resp.status_code, resp.get_json())

result = resp.get_json()
if not result or not result.get('success'):
    print('Login failed, cannot proceed')
    sys.exit(1)

token = result['token']
user_id = result['user']['id']

# 2. 模拟前端发送的真实数据结构
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

# 这个结构和前端 exam.js 传给 saveExamRecord 的完全一致
save_data = {
    'result': {
        'correctRate': 60.0,
        'vocabularySize': 3500,
        'correctCount': 30,
        'totalAnswered': 50,
        'level': '高中水平'
    },
    'wrongAnswers': [
        {'word': 'abandon', 'correct': '放弃', 'level': '高中', 'difficulty': 1},
        {'word': 'ability', 'correct': '能力', 'level': '初中', 'difficulty': 2}
    ]
}

print('\nSending save request...')
print('Data:', json.dumps(save_data, ensure_ascii=False, indent=2))

resp = client.post('/api/records', data=json.dumps(save_data), headers=headers, content_type='application/json')
print('\nResponse:', resp.status_code)
try:
    data = resp.get_json()
    print('Body:', json.dumps(data, ensure_ascii=False, indent=2))
except:
    print('Raw:', resp.data.decode('utf-8'))

# 3. 查询验证
print('\n--- Query records ---')
resp = client.get('/api/records', headers=headers)
print('Records:', resp.status_code, resp.get_json())

print('\n--- Query mistakes ---')
resp = client.get('/api/mistakes/personal', headers=headers)
print('Mistakes:', resp.status_code, resp.get_json())
