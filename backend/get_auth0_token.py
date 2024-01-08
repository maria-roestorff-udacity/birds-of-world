import os
import requests

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
API_AUDIENCE = os.environ['API_AUDIENCE']

AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
AUTH0_CLIENT_SECRET = os.environ['AUTH0_CLIENT_SECRET']
AUTH0_OWNER_USERNAME = os.environ['AUTH0_OWNER_USERNAME']
AUTH0_OWNER_PASSWORD = os.environ['AUTH0_OWNER_PASSWORD']
AUTH0_VIEWER_USERNAME = os.environ['AUTH0_VIEWER_USERNAME']
AUTH0_VIEWER_PASSWORD = os.environ['AUTH0_VIEWER_PASSWORD']

owner_payload = {'client_id': f'{AUTH0_CLIENT_ID}',
                 'client_secret': f'{AUTH0_CLIENT_SECRET}',
                 'audience': f'{API_AUDIENCE}',
                 'grant_type': 'password',
                 'username': f'{AUTH0_OWNER_USERNAME}',
                 'password': f'{AUTH0_OWNER_PASSWORD}'
                 }

viewer_payload = {'client_id': f'{AUTH0_CLIENT_ID}',
                  'client_secret': f'{AUTH0_CLIENT_SECRET}',
                  'audience': f'{API_AUDIENCE}',
                  'grant_type': 'password',
                  'username': f'{AUTH0_VIEWER_USERNAME}',
                  'password': f'{AUTH0_VIEWER_PASSWORD}'
                  }

headers = {'content-type': "application/json"}

url = f'https://{AUTH0_DOMAIN}/oauth/token'

owner_role = requests.post(url, headers=headers, json=owner_payload)
viewer_role = requests.post(url, headers=headers, json=viewer_payload)

owner_access_token = owner_role.json().get('access_token', None)
viewer_access_token = viewer_role.json().get('access_token', None)

print(f'owner_access_token: {owner_access_token}')
print(f'viewer_access_token: {viewer_access_token}')
