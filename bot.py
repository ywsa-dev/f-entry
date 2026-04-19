import requests
import os
import random

USERNAME = os.environ.get('ENTRY_USER')
PASSWORD = os.environ.get('ENTRY_PW')

def login():
    url = "https://playentry.org/api/user/login"
    data = {"username": USERNAME, "password": PASSWORD}
    response = requests.post(url, json=data)
    return response.cookies

def get_random_users():
    # 엔트리 커뮤니티(묻답)에서 최근 활동 중인 유저 ID 10개를 가져옵니다.
    url = "https://playentry.org/api/discuss/find?category=free"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        # 유저 고유 ID만 추출 (중복 제거)
        user_ids = list(set([post['user']['_id'] for post in data['list']]))
        return user_ids[:10] # 상위 10명만 선택
    return []

def follow(cookies, target_id):
    url = f"https://playentry.org/api/discuss/follow/{target_id}"
    headers = {'Referer': 'https://playentry.org/'}
    res = requests.post(url, cookies=cookies, headers=headers)
    if res.status_code == 200:
        print(f"성공: {target_id} 팔로우 완료!")
    else:
        print(f"실패: {target_id} (에러 코드: {res.status_code})")

if __name__ == "__main__":
    entry_cookies = login()
    if entry_cookies:
        targets = get_random_users()
        print(f"{len(targets)}명의 유저를 찾았습니다. 팔로우를 시작합니다!")
        for t_id in targets:
            follow(entry_cookies, t_id)
