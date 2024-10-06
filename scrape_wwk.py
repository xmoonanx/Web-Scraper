import requests
from bs4 import BeautifulSoup

all_jobs = []
url = "https://weworkremotely.com/categories/remote-full-stack-programming-jobs#job-listings"
def scrape_page(url): #all page를 scrape 하기 위해 함수생성
    print(f"Scrapping {url}...")
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser",)
    #BeautifulSoup를 사용해서 url의 Elements를 불러옴, html.parser은 형태지정
    jobs =soup.find("section", class_="jobs").find_all("li")[1:-1] #li의 첫번째, 마지막은 안보이게
    #불러온 Elemets에서 찾고 싶은 요소 지정 -> section class="jobs" 혹은 id="category-2"에서 모든 li찾기

    for job in jobs: # jobs에서 필요한 부분들만 빼서 .text를 붙이면 가져오려는 텍스트만 가져옴
        title = job.find("span", class_="title").text
        company, position, region = job.find_all("span", class_="company")
        '''
        company class가 3개가 있음, 그래서 우리가 직접 이름을 바꿔 3개로 나눠줌
        ex) 
        arr = ['a', 'b', 'c']
        1, 2, 3 = arr
        1=a, 2=b, 3=c 가 가능하다    
        '''
        url =job.find("div", class_="tooltip--flag-logo").next_sibling["href"]#우리가 얻고 싶은 url을 위해 tooltip 다음의 href를 가져옴
        job_data = { #job data를 dictinary화 하고 url 앞부분을 추가해줌
            "title" : title,
            "company" : company.text,
            "position" : position.text,
            "region" : region.text,
            "url" : f"https://weworkremotely.com{url}",
        }
        all_jobs.append(job_data) #job data를 list 형태로 추가

def get_pages(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    check_pagination = soup.find("div", class_="pagination")
    if(check_pagination):
        page_count =len(check_pagination.find_all("span",class_="page"))    
    return page_count

total_pages = get_pages("https://weworkremotely.com/remote-full-time-jobs?page=1")

for x in range(total_pages):
    url = f"https://weworkremotely.com/remote-full-time-jobs?page={x+1}"
    scrape_page(url)

# scrape_page("https://weworkremotely.com/categories/remote-full-stack-programming-jobs#job-listings")
print(len(all_jobs))
