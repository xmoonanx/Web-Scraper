import requests
from playwright.sync_api import sync_playwright
# playwright는 동적환경을 다룰 수 있다.

with sync_playwright() as p: # p = sync_playwright()
    browser= p.chromium.launch(headless=False) #chromium으로 브라우저 설정
    page = browser.new_page()
    # page.set_extra_http_headers({
    #     'User_Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    #     'Accept-Language': 'en-US, en;q=0.9',
    #     'Referer' : 'https://remoteok.com/'
    # })
    
    page.goto("https://google.com")
    #"https://remoteok.com/remote-flutter-jobs"
    
    print(page.title())
    