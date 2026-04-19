import requests
import os

USERNAME = os.environ.get('ENTRY_USER')
PASSWORD = os.environ.get('ENTRY_PW')

def login():
    # 주소를 /api/user/login 에서 /api/users/login 으로 수정 시도
    url = "https://playentry.org/api/users/login"
    data = {"username": USERNAME, "password": PASSWORD}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://playentry.org/'
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        print("✅ 로그인 성공!")
        return response.cookies
    else:
        print(f"❌ 로그인 실패 (에러 코드: {response.status_code})")
        # 404가 계속 뜨면 주소를 다시 이전 것으로 시도해봅니다.
        if response.status_code == 404:
            url_alt = "https://playentry.org/api/user/login"
            response = requests.post(url_alt, json=data, headers=headers)
            if response.status_code == 200:
                print("✅ (재시도) 로그인 성공!")
                return response.cookies
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
    headers = {
        'Referer': 'https://playentry.org/',
        'User-Agent': 'Mozilla/5.0'
    }
    res = requests.post(url, cookies=cookies, headers=headers)
    print(f"결과: {target_id} -> {res.status_code}")

if __name__ == "__main__":
    if not USERNAME or not PASSWORD:
        print("⚠️ 환경변수(Secrets) 설정 확인 필요!")
    else:
        entry_cookies = login()
        if entry_cookies:
            targets = get_random_users()
            print(f"찾은 유저 수: {len(targets)}")
            for t_id in targets:
                follow(entry_cookies, t_id)
