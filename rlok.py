import requests
from playwright.sync_api import sync_playwright
import time
# playwright는 동적환경을 다룰 수 있다.
from bs4 import BeautifulSoup
import csv

with sync_playwright() as p: # p = sync_playwright()
    browser= p.chromium.launch(headless=False) #chromium으로 브라우저 설정
    page = browser.new_page()
    # page.set_extra_http_headers({
    #     'User_Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    #     'Accept-Language': 'en-US, en;q=0.9',
    #     'Referer' : 'https://remoteok.com/'
    # })
    
    page.goto("https://www.wanted.co.kr/")
    #"https://remoteok.com/remote-flutter-jobs"
    time.sleep(5)
    
    page.click("button.Aside_searchButton__rajGo")
    #검색버튼 클릭
    time.sleep(3)
    
    page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")
    #'검색어를입력해주세요'의 고유값을 찾고 그 입력칸에 flutter라 채우기
    time.sleep(3)
    
    page.keyboard.down("Enter")
    time.sleep(5)
     
    page.click("a#search_tab_position")# a#은 anchor
    time.sleep(6)
    
    for x in range(4):
        page.keyboard.down("End")
        time.sleep(3)
    
    content = page.content()
    
    p.stop()
    
    soup = BeautifulSoup(content, "html.parser")
    #BeautifulSoup으로 원하는 데이터 뽑아내기
    jobs = soup.find_all("div", class_="JobCard_container__REty8")
    jobs_db =[]
    
    for job in jobs:
        title = job.find("strong", class_="JobCard_title__HBpZf").text
        company_name = job.find("a")["data-company-name"]
        link =f"https://www.wanted.co.kr{job.find('a')['href']}"
        reward =job.find("span", class_="JobCard_reward__cNlG5").text
        
        job={
            "title":title,
            "company_name":company_name,
            "link":link,
            "reward":reward
        }
        jobs_db.append(job)
        
file =open("jobs.csv", "w")
writer = csv.writer(file)
writer.writerow(["Title", "Company", "Reward", "Link"])
#csv에 웹 데이터 정리하기
for job in jobs_db:
    writer.writerow(job.values())
    # writerow는 list로만 데이터를 받을 수 있기 때문에 
    # job의 dictionary형태를 values를 활용하여 list로 변경