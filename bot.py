import requests
import os

# 깃허브 Secrets에서 정보를 안전하게 가져옵니다.
USERNAME = os.environ.get('ENTRY_USER')
PASSWORD = os.environ.get('ENTRY_PW')

# 팔로우할 대상의 '유저 고유 ID'(마이페이지 주소 뒷부분)를 적어주세요.
TARGET_IDS = ["target_id_1", "target_id_2"] 

def login():
    url = "https://playentry.org/api/user/login"
    # 변수를 사용하여 로그인 정보를 전달합니다.
    data = {"username": USERNAME, "password": PASSWORD}
    response = requests.post(url, json=data)
    
    if response.status_code != 200:
        print("로그인에 실패했습니다. 아이디나 비번을 확인하세요.")
        return None
    return response.cookies

def follow(cookies, target_id):
    if not cookies:
        return
    
    url = f"https://playentry.org/api/discuss/follow/{target_id}"
    headers = {
        'Referer': 'https://playentry.org/',
        'User-Agent': 'Mozilla/5.0' # 봇 차단을 방지하기 위해 추가하는 것이 좋습니다.
    }
    res = requests.post(url, cookies=cookies, headers=headers)
    
    if res.status_code == 200:
        print(f"{target_id} 팔로우 성공!")
    else:
        print(f"{target_id} 팔로우 실패 (코드: {res.status_code})")

if __name__ == "__main__":
    entry_cookies = login()
    if entry_cookies:
        for t_id in TARGET_IDS:
            follow(entry_cookies, t_id)