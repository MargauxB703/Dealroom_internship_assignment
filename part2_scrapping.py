#pip install selenium
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
from openpyxl import load_workbook
import pandas as pd
pd.set_option('display.max_columns', 15)
pd.set_option('display.max_colwidth', None)

#Please provide the complete path to your chrome driver
path_to_chrome_driver = "chromedriver.exe"
driver = webdriver.Chrome(executable_path = path_to_chrome_driver)
driver.get('https://www.ycombinator.com/companies/')

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    

companies_list = []
soup = BeautifulSoup(driver.page_source, 'lxml')
for company in soup.find_all('a', class_='SharedDirectory-module__company___AVmr6 no-hovercard'):
    companies_list.append('https://www.ycombinator.com' + company['href'])


companies_df = pd.DataFrame(columns=['Name', 'Legend', 'Text', 'Link', 'Founded', 'Team_size', 'Location'])
count = 0

for company in companies_list:
    soup = BeautifulSoup(requests.get(company).text, 'html.parser')
    name = soup.find('h1').text
    legend = soup.find('h3').text
    text = soup.find('p').text
    text = text.replace('\r', '')
    text = text.replace('\n', ' ')
    link = soup.find('a', {'target': '_blank'}).text
    facts = soup.find('div', class_='facts').find_all('span')
    founded = facts[0].text
    team_size = facts[1].text
    location = facts[2].text
    companies_df.loc[len(companies_df), :] = [name, legend, text, link, founded, team_size, location]
    count += 1
    if count%10 == 0:
        print('Progress: {}%'.format(count//10), end='\r')

#----------------------------------Export to Excel----------------------------
book = load_workbook(r'Data_Science_Internship_Assignment_Answer.xlsx')
writer = pd.ExcelWriter(r'Data_Science_Internship_Assignment_Answer.xlsx', engine='openpyxl') 
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
companies_df.to_excel(writer, "Scraping results", index = False)
writer.save()