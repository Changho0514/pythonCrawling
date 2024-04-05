from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime, timedelta

# 크롤링할 날짜 범위 지정
start_date = datetime(1996, 5, 10)
end_date = datetime(2001, 5, 10)  # 예시로 10일간의 날짜를 크롤링합니다.

# 결과를 저장할 리스트 초기화
all_headlines = []

# 날짜를 순회하면서 크롤링 진행
current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime("%Y%m%d")
    url = f"https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=230&sid1=100&date={date_str}"
    header = {"user-agent": "Mozilla/5.0"}
    html = requests.get(url, headers=header)
    soup = BeautifulSoup(html.text, 'html.parser')

    # 기사 제목 찾기   
    headlines = soup.find('strong', class_='sa_text_strong')
    
    if headlines:
        # 각 날짜의 기사 제목을 리스트에 추가
        for headline in headlines:
            title = headline.text.strip()
            all_headlines.append([current_date, title])

    # 다음 날짜로 이동
    current_date += timedelta(days=1)


# DataFrame으로 변환
news_df = pd.DataFrame(all_headlines, columns=['Date', 'Headline'])

# CSV로 저장
news_df.to_csv('news.csv', index=False, encoding='utf-8-sig')
