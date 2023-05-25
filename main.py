import requests 
from bs4 import BeautifulSoup
import pandas as pd 

def releaseSplit(text):
    returnedValue = text.split(':')
    initVal = returnedValue[1].split(',')
    dateVal = initVal[1][:5]
    release = initVal[0]+ " "+ dateVal
    genre = returnedValue[2]
    splitGenre = genre.split(',')
    lastGenre = splitGenre[-1]
    dedLen = len(lastGenre) - 8
    lastGenre = lastGenre[:dedLen]
    splitGenre.pop()
    splitGenre.append(lastGenre)
    genre = ','.join(splitGenre)
    language = returnedValue[3]
    return release, genre, language

url = "https://silverbirdcinemas.com/cinema/accra/"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find_all('div', class_='col-md-6 grid-item')

movies = []

for result in results: 
    img = result.find('img', class_='attachment-164x220')
    if img is not None:
        img_src = img['src']
    title = result.find('h4', class_='entry-title')
    if title is not None:
        title = title.text.strip()
    entry_date = result.find('div', class_= 'entry-date')
    if entry_date is not None:
        entry_date = entry_date.text
    showtime = result.find('p', class_='cinema_page_showtime')
    if showtime is not None:
        showtime = showtime.text.strip()
    concatValue = result.find('div', class_='desc-mv').text
    if concatValue is not None:
        release, genre, language = releaseSplit(concatValue)
    votes = result.find('span', class_='mcount')
    if votes is not None: 
        votes = votes.text.strip()
    rate = result.find('span', class_='rate')
    if rate is not None: 
        rate = rate.text
    
    movies.append([title, entry_date, showtime, release, genre, language, votes, rate, img_src])

    # print(f"Image: {img['src']}")
    # print(f"title: {title}")
    # print(f"entry date: {entry_date}")
    # print(f"{showtime}")
    # print(f"Release: {release}")
    # print(f"Genre - {genre}")
    # print(f"Language - {language}")
    # print(f"Votes: {votes}")
    # print(f"Rate: {rate}")



df = pd.DataFrame(movies)

df.to_csv('movies.csv', index=False, header=['Title', 'Entry Date', 'Show Time', 'Release', 'Genre', 'Language', 'Votes', 'Rate', 'Image Source'])


