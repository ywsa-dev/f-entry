import os
from entry_api import Entry

# 깃허브 Secrets에서 가져오기
USERNAME = os.environ.get('ENTRY_USER')
PASSWORD = os.environ.get('ENTRY_PW')

def run_bot():
    try:
        # 라이브러리를 이용해 로그인 시도
        user = Entry(USERNAME, PASSWORD)
        print("✅ 로그인 성공!")

        # 최근 활동 중인 유저 가져오기 (자유게시판 기준)
        # 라이브러리마다 방식이 다르지만, 보통 아래처럼 씁니다.
        # 여기서는 간단하게 본인에게 알림을 보낸 사람 등을 타겟팅할 수도 있어요.
        
        print("랜덤 유저 탐색 중...")
        # 엔트리 API 특성상 커뮤니티 데이터를 긁어옵니다.
        # (이 부분은 라이브러리 업데이트에 따라 조금씩 다를 수 있습니다.)
        
        print("팔로우를 시도합니다.")
        # 예시: 특정 기능을 이용해 팔로우 실행
        # user.follow('유저고유ID') 

    except Exception as e:
        print(f"❌ 에러 발생: {e}")

if __name__ == "__main__":
    run_bot()
