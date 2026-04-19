import requests
import os
import random

# 깃허브 Secrets 설정값
USERNAME = os.environ.get('ENTRY_USER')
PASSWORD = os.environ.get('ENTRY_PW')

def run_bot():
    # 1. 사람처럼 보이게 만드는 '위장용' 정보
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://playentry.org/signin',
        'Origin': 'https://playentry.org',
        'Content-Type': 'application/json'
    }

    session = requests.Session()

    # 2. 로그인 시도 (가장 최신화된 주소)
    login_url = "https://playentry.org/api/user/login/local"
    login_data = {"username": USERNAME, "password": PASSWORD}
    
    login_res = session.post(login_url, json=login_data, headers=headers)
    
    if login_res.status_code != 200:
        print(f"❌ 로그인 실패 (코드: {login_res.status_code})")
        return

    print("✅ 로그인 성공!")

    # 3. 자유게시판에서 최근 활동 중인 유저 10명 찾기
    list_url = "https://playentry.org/api/discuss/find?category=free"
    list_res = session.get(list_url, headers=headers)
    
    if list_res.status_code == 200:
        data = list_res.json()
        # 최근 글 쓴 사람들의 고유 ID 추출
        user_ids = list(set([item['user']['_id'] for item in data['list'] if 'user' in item]))
        targets = user_ids[:10]
        
        print(f"탐색 완료: {len(targets)}명을 찾았습니다.")

        # 4. 팔로우 실행
        for t_id in targets:
            follow_url = f"https://playentry.org/api/discuss/follow/{t_id}"
            # 팔로우할 때는 리퍼러를 프로필 주소로 바꿔서 더 사람처럼 위장
            headers['Referer'] = f'https://playentry.org/profile/{t_id}'
            
            f_res = session.post(follow_url, headers=headers)
            if f_res.status_code == 200:
                print(f"✨ {t_id} 팔로우 성공!")
            else:
                print(f"⚠️ {t_id} 실패 (코드: {f_res.status_code})")
    else:
        print("❌ 유저 목록을 가져오지 못했습니다.")

if __name__ == "__main__":
    run_bot()
