import undetected_chromedriver as uc 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import *
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options




url = "https://www.goodreads.com/list/show/2681.Time_Magazine_s_All_Time_100_Novels"



def TransformDatetime(date):
    return datetime.strptime(date.strip(), '%B %d, %Y').strftime('%Y-%m-%d')


def ParseAuthor(auth_url):
    print(id)
    driver.get(auth_url)

    if id == 1:
        b = int(input("Close AD window and input smth: "))
    
    soup = BeautifulSoup(driver.page_source, "html5lib") 

    author = soup.find(True, {'itemprop': ['name']}).text.replace("'", "''").replace('"', "''")
    birth_date = soup.find(True, {'itemprop': ['birthDate']})

    if birth_date == None:
        birth_date = '1982-01-01'
    else:
        birth_date = TransformDatetime(str(birth_date.text))

    death_date = (soup.find(True, {'itemprop': ['deathDate']}))
    if death_date == None:
        death_date = 'NULL'
    else:
        death_date = TransformDatetime(str(death_date.text))

    author_info = str(soup.find(True, {'id': re.compile("freeTextContainerauthor+")}))
    first_br_index = author_info.find('<br/>')  
    if first_br_index != -1:
        text_before_br = author_info[:first_br_index]
    else:
        text_before_br = author_info  
    soup1 = BeautifulSoup(text_before_br, "html.parser")
    author_info = soup1.text.replace("'", "''").replace('"', "''")
    author_info = re.sub(r'\s+', ' ', author_info).strip()
    author_img = soup.find('img', {'itemprop': ['image']})['src']

    table_name = 'Authors'
    column_a_name = 'FullName'
    column_birth = 'BirthDate'
    column_death = 'DeathDate'
    column_biography = 'Biography'
    column_a_img = 'ImageUrl'
    column_a_id = "Id"

    table_ab = 'AuthorBook'
    column_ab_auth_id = "AuthorsId"
    column_ab_books_id = "BooksId"

    ab_id = len(authors_arr) + 1
    auth_id = len(authors_arr) + 1

    if author in authors_arr:
        ab_id = authors_arr.index(author) + 1
    else:
        authors_arr.append(author)
        file2.write(f"INSERT INTO {table_name} ({column_a_id}, {column_a_name}, {column_birth}, {column_biography}, {column_death}, {column_a_img})\nVALUES({auth_id}, '{author}', '{birth_date}', '{author_info}', '{death_date}', '{author_img}')\n\n")

    file3.write(f"INSERT INTO {table_ab} ({column_ab_auth_id}, {column_ab_books_id})\nVALUES({ab_id}, {id})\n\n")



def ParseBook(evr_url, i):
    print(i)


    html = requests.get(evr_url)

    soup = BeautifulSoup(html.text, "html5lib") 

    title = soup.find_all(True, {'data-testid': ['bookTitle']})[0].text.replace("'", "''").replace('"', "''")
    #rating = soup.find(True, {'class': ['RatingStatistics__rating']}).text
    details = soup.find_all(True, {'class': ['DetailsLayoutRightParagraph__widthConstrained']})[0].text.replace("'", "''").replace('"', "''")
    details = re.sub(r'\s+', ' ', details).strip()
    genres = [i.text for i in soup.find_all(True, {'class': ['BookPageMetadataSection__genreButton']})]
    genres = ', '.join(genres).replace("'", "''").replace('"', "''")
    date_published = str(soup.find(True, {'data-testid': ['publicationInfo']}).text)[16:]
    date_published = TransformDatetime(date_published)
    available_copies = 1
    book_img = soup.find(True, {'class': ['ResponsiveImage']})['src']
    
    author_url = soup.find(True, {'class': ['ContributorLink']})['href']
    ParseAuthor(author_url)

    #column names
    table_name = 'Books'
    column_title = 'Title'
    column_description = 'Description'
    column_published = 'DatePublished'
    column_genre = 'Genre'
    column_available = 'AvailableCopies'
    column_book_img = 'ImageUrl'
    column_b_id = 'Id'


    file1.write(f"INSERT INTO {table_name} ({column_b_id}, {column_title}, {column_description}, {column_published}, {column_genre}, {column_available}, {column_book_img})\nVALUES({id}, '{title}', '{details}', '{date_published}', '{genres}', {available_copies}, '{book_img}')\n\n")


options = uc.ChromeOptions()
#options.add_argument('--load-extension=D:/extension')


driver = uc.Chrome(use_subprocess=True)
file1 = open("your path for books", "w", encoding='utf-8')
file2 = open("your path for authors", "w", encoding='utf-8')
file3 = open("your path for authors_books", "w", encoding='utf-8')
authors_arr = []

driver.get(url)
print('start')
html = BeautifulSoup(driver.page_source, "html5lib") 
urls = html.find_all(True, attrs={'class': 'bookTitle'})

id = 1
for i in urls:
    ParseBook('https://www.goodreads.com' + str(i['href']), i['href'])
    id += 1

driver.quit()
print('finish')



