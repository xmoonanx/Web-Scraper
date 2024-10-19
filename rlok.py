# import requests
# from playwright.sync_api import sync_playwright
# import time
# # playwright는 동적환경을 다룰 수 있다.
# from bs4 import BeautifulSoup
# import csv

# with sync_playwright() as p: # p = sync_playwright()
#     browser= p.chromium.launch(headless=False) #chromium으로 브라우저 설정
#     page = browser.new_page()
#     # page.set_extra_http_headers({
#     #     'User_Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
#     #     'Accept-Language': 'en-US, en;q=0.9',
#     #     'Referer' : 'https://remoteok.com/'
#     # })
    
#     page.goto("https://www.wanted.co.kr/")
#     #"https://remoteok.com/remote-flutter-jobs"
#     time.sleep(5)
    
#     page.click("button.Aside_searchButton__rajGo")
#     #검색버튼 클릭
#     time.sleep(3)
    
#     page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")
#     #'검색어를입력해주세요'의 고유값을 찾고 그 입력칸에 flutter라 채우기
#     time.sleep(3)
    
#     page.keyboard.down("Enter")
#     time.sleep(5)
     
#     page.click("a#search_tab_position")# a#은 anchor
#     time.sleep(6)
    
#     for x in range(4):
#         page.keyboard.down("End")
#         time.sleep(3)
#     time.sleep(3)
#     content = page.content()
    
#     p.stop()
    
#     soup = BeautifulSoup(content, "html.parser")
#     #BeautifulSoup으로 원하는 데이터 뽑아내기
#     jobs = soup.find_all("div", class_="JobCard_container__REty8")
#     jobs_db =[]
    
#     for job in jobs:
#         title = job.find("strong", class_="JobCard_title__HBpZf").text
#         company_name = job.find("a")["data-company-name"]
#         link =f"https://www.wanted.co.kr{job.find('a')['href']}"
#         reward =job.find("span", class_="JobCard_reward__cNlG5").text
        
#         job={
#             "title":title,
#             "company_name":company_name,
#             "reward":reward,
#             "link":link
#         }
#         jobs_db.append(job)
        
# file =open("jobs.csv", "w")
# writer = csv.writer(file)
# writer.writerow(["Title", "Company", "Reward", "Link"])
# #csv에 웹 데이터 정리하기
# for job in jobs_db:
#     writer.writerow(job.values())
#     # writerow는 list로만 데이터를 받을 수 있기 때문에 
#     # job의 dictionary형태를 values를 활용하여 list로 변경
from flask import Flask, render_template, request, send_file
import os
import time
import csv
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

app = Flask(__name__)

class JobScraper:
    def __init__(self, search_term):
        self.search_term = search_term
        self.jobs_db = []

    def launch_browser(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # headless 모드
            page = browser.new_page()
            self.scrape_jobs(page)
            browser.close()

    def scrape_jobs(self, page):
        start_time = time.time()  # 시작 시간
        page.goto("https://www.wanted.co.kr")
        time.sleep(5)
        # 검색 버튼이 보일 때까지 대기
        time.sleep(5)
        page.wait_for_selector("button.Aside_searchButton__rajGo", state="visible")
        page.click("button.Aside_searchButton__rajGo")

        # 검색어 입력
        page.get_by_placeholder("검색어를 입력해 주세요.").fill(self.search_term)
        page.keyboard.press("Enter")

        # 검색 탭이 보일 때까지 대기
        page.wait_for_selector("a#search_tab_position", state="visible")
        page.click("a#search_tab_position")

        self.scroll_to_bottom(page)
        self.extract_jobs(page.content())
        end_time = time.time()  # 종료 시간
        print(f"소요 시간: {end_time - start_time:.2f}초")

    def scroll_to_bottom(self, page):
        last_height = page.evaluate("document.body.scrollHeight")
        while True:
            page.keyboard.down("End")
            time.sleep(1)
            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def extract_jobs(self, content):
        soup = BeautifulSoup(content, "html.parser")
        jobs = soup.find_all("div", class_="JobCard_container__REty8")

        seen_jobs = set()
        for job in jobs:
            title = job.find("strong", class_="JobCard_title__HBpZf").text
            company_name = job.find("a")["data-company-name"]
            link = f"https://www.wanted.co.kr{job.find('a')['href']}"
            reward = job.find("span", class_="JobCard_reward__cNlG5").text

            job_data = (title, company_name, reward, link)
            if job_data not in seen_jobs:
                seen_jobs.add(job_data)
                self.jobs_db.append({
                    "title": title,
                    "company_name": company_name,
                    "reward": reward,
                    "link": link
                })

    def save_to_csv(self, filename):
        
        with open(filename, "w", newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["title", "company_name", "reward", "link"])
            writer.writeheader()
            writer.writerows(self.jobs_db)
       
        print(f"총 {len(self.jobs_db)}개의 정보를 '{filename}'에 저장했습니다.")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        search_term = request.form.get("search_term")
        filename = f"jobs_{search_term}.csv"

        scraper = JobScraper(search_term)
        scraper.launch_browser()
        scraper.save_to_csv(filename)

        return send_file(filename, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)




