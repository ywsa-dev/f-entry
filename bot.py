import requests
import os

USERNAME = os.environ.get('ENTRY_USER')
PASSWORD = os.environ.get('ENTRY_PW')

def login():
    # 세션을 만들어서 쿠키를 자동으로 관리하게 합니다.
    session = requests.Session()
    
    # 1. 먼저 메인 페이지에 접속해서 기본 쿠키를 받습니다.
    session.get("https://playentry.org")
    
    # 2. 로그인 주소 (가장 확률 높은 곳)
    url = "https://playentry.org/api/user/login/local"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Referer': 'https://playentry.org/signin',
        'Content-Type': 'application/json'
    }
    
    payload = {"username": USERNAME, "password": PASSWORD}
    
    # 3. 로그인 시도
    res = session.post(url, json=payload, headers=headers)
    
    if res.status_code == 200:
        print("✅ 드디어 로그인 성공!")
        return session
    else:
        print(f"❌ 실패 (코드: {res.status_code})")
        # 실패하면 다른 주소로 딱 한 번만 더 시도
        url2 = "https://playentry.org/api/v2/user/login/local"
        res2 = session.post(url2, json=payload, headers=headers)
        if res2.status_code == 200:
            print("✅ 재시도로 로그인 성공!")
            return session
        return None

def follow_random_users(session):
    # 자유게시판에서 유저 가져오기
    list_url = "https://playentry.org/api/discuss/find?category=free"
    res = session.get(list_url)
    if res.status_code == 200:
        data = res.json()
        user_ids = list(set([item['user']['_id'] for item in data['list'] if 'user' in item]))
        
        for t_id in user_ids[:10]:
            f_url = f"https://playentry.org/api/discuss/follow/{t_id}"
            f_res = session.post(f_url, headers={'Referer': f'https://playentry.org/profile/{t_id}'})
            print(f"결과: {t_id} -> {f_res.status_code}")

if __name__ == "__main__":
    s = login()
    if s:
        follow_random_users(s)
    else:
        print("😭 엔트리 보안이 너무 강력합니다. 나중에 다시 시도해봐야 할 것 같아요.")
