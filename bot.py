import requests
import os

USERNAME = os.environ.get('ENTRY_USER')
PASSWORD = os.environ.get('ENTRY_PW')

def login():
    # 엔트리 실제 로그인 API 주소 (v2 버전이나 local 경로 시도)
    url = "https://playentry.org/api/v2/user/login/local" 
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://playentry.org/signin',
        'Content-Type': 'application/json'
    }
    
    payload = {"username": USERNAME, "password": PASSWORD}
    
    # 첫 번째 주소 시도
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        # 실패 시 구형 주소로 한 번 더 시도
        url = "https://playentry.org/api/user/login/local"
        response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("✅ 로그인 성공!")
        return response.cookies
    else:
        print(f"❌ 실패 (코드: {response.status_code})")
        print("서버 응답:", response.text)
        return None

# (get_random_users와 follow 함수는 이전과 동일)
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
    headers = {'Referer': 'https://playentry.org/', 'User-Agent': 'Mozilla/5.0'}
    res = requests.post(url, cookies=cookies, headers=headers)
    print(f"결과: {target_id} -> {res.status_code}")

if __name__ == "__main__":
    entry_cookies = login()
    if entry_cookies:
        targets = get_random_users()
        for t_id in targets:
            follow(entry_cookies, t_id)
