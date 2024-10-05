import requests
from bs4 import BeautifulSoup
url = "https://weworkremotely.com/categories/remote-full-stack-programming-jobs#job-listings"

res = requests.get(url)

soup = BeautifulSoup(res.content, "html.parser",)
#BeautifulSoup를 사용해서 url의 Elements를 불러옴, html.parser은 형태지정
jobs =soup.find("section", class_="jobs").find_all("li")
#불러온 Elemets에서 찾고 싶은 요소 지정 -> section class="jobs" 혹은 id="category-2"에서 모든 li찾기
print(jobs)


