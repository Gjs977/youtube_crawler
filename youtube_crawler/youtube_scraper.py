from playwright.sync_api import sync_playwright
import sys
from bs4 import BeautifulSoup
import time
import sentiment_analysis

video_link = sys.argv[1] #유튜브 영상 링크 받기
check_string = "https://www.youtube.com/watch?"

def run_playwright(): #유튜브 페이지 열고 댓글 로딩해 가져오는 함수
    if check_string in video_link: 

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False, #True로 하면 페이지 안뜸
                executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe"
            ) #오류로 PC에 설치된 크롬사용(senwifi 때문으로 추정)

            page = browser.new_page()
            page.goto(video_link) 
            page.wait_for_timeout(3000) #페이지 로딩

            last_count = 0
            retry = 0

            # 페이지 끝까지 스크롤하며 댓글 로딩
            while True:
                page.evaluate("window.scrollBy(0, 1000)")
                page.wait_for_timeout(1500) 
                comments = page.query_selector_all("ytd-comment-thread-renderer")
                
                if len(comments) == last_count:
                    retry += 1
                    if retry > 3:  # 연속 3번 변화 없으면 종료
                        break
                else:
                    retry = 0
                last_count = len(comments)

            html = page.content()  #BeautifulSoup하기 위해 HTML 가져옴
            browser.close()
            return html #HTML 반환
    else:
        print("올바른 유튜브 링크를 입력해주세요.")
        sys.exit(0)

def run_BeautifulSoup(html): #가져온 html에서 댓글 추출하는 함수
    soup = BeautifulSoup(html, "html.parser")
    comment_elements = soup.select("ytd-comment-thread-renderer #content-text")
    comments = [] #댓글 모음 배열

    for i in comment_elements:
        text = i.get_text(strip=True)
        comments.append(text)
    return comments


if __name__ == "__main__":
    start = time.time() #걸린 시간 측정

    html = run_playwright() #로딩된 HTML 반환
    comments = run_BeautifulSoup(html) #HTML에서 comments만 반환
    result = sentiment_analysis.analyze_sentiment(comments)# comments를 ai로 감정분석

    end = time.time()

    print(f"소요 시간: {end - start:.2f}초")
    print(f"댓글 수: {len(comments)}개")
    print(result) 
