import time
import requests
from bs4 import BeautifulSoup

# Send get request:
try:
  URL = 'https://realpython.github.io/fake-jobs/'
  page = requests.get(URL)

  # Get Job title:
  title = []

  soup = BeautifulSoup(page.content, "html.parser")

  jobs = soup.find(id='ResultsContainer')
  
  job_spec = "Python"

  job_elements = jobs.find_all('div', class_='card-content')
  job_selected = jobs.find_all('h2', string= lambda text: job_spec.lower() in text.lower() )

  start = time.time()
  
  python_job_elements = [
    h2_element.parent.parent.parent for h2_element in job_selected
]
  
  for job_elt in python_job_elements:
    title = job_elt.find("h2", class_="title").text.strip()
    location = job_elt.find("p", class_="location").text.strip()
    company = job_elt.find("h3", class_="company").text.strip()
    
    links = job_elt.find_all("a", string="Apply")
    for link in links:
        # print(link.text.strip())
        link_url = link["href"]
        print(f"Apply here: {link_url}\n")
    
    
    print({title, location, company}, end='\n'*2)
  
  end = time.time()
  total = end-start
  print(total)
  
except ConnectionError:
  print("Check your internet connection")