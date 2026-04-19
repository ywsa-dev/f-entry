import requests
import os

USERNAME = os.environ.get('ENTRY_USER')
PASSWORD = os.environ.get('ENTRY_PW')

def login():
    url = "https://playentry.org/api/user/login"
    data = {"username": USERNAME, "password": PASSWORD}
    response = requests.post(url, json=data)
    
    # [진단] 로그인 결과 확인
    if response.status_code == 200:
        print("✅ 로그인 성공!")
        return response.cookies
    else:
        print(f"❌ 로그인 실패 (에러 코드: {response.status_code})")
        print("아이디/비번이 틀렸거나 해외 접속이 차단되었을 수 있습니다.")
        return None

def get_random_users():
    url = "https://playentry.org/api/discuss/find?category=free"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        user_ids = list(set([post['user']['_id'] for post in data['list']]))
        return user_ids[:10]
    return []

def follow(cookies, target_id):
    url = f"https://playentry.org/api/discuss/follow/{target_id}"
    headers = {'Referer': 'https://playentry.org/'}
    res = requests.post(url, cookies=cookies, headers=headers)
    print(f"결과: {target_id} -> {res.status_code}")

if __name__ == "__main__":
    if not USERNAME or not PASSWORD:
        print("⚠️ 환경변수(Secrets)가 설정되지 않았습니다!")
    else:
        entry_cookies = login()
        if entry_cookies:
            targets = get_random_users()
            print(f"찾은 유저 수: {len(targets)}")
            for t_id in targets:
                follow(entry_cookies, t_id)
