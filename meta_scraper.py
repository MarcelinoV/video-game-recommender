from bs4 import BeautifulSoup
import csv
import requests
#from multiprocessing import Pool


# Establish link to page and store source content
print('Connecting...')

page_limit = 100 # how many pages desired, change val here

pages = range(0,page_limit+1) # first 65 pages of games on metacritic game reviews

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}

# declare list where data will be stored
all_data = []


for i in pages:

    page = requests.get('https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?sort=desc&page=' + str(i), # url
                        headers=headers)
    src = page.content

    # Verify connection to page is good

    print('Connection established') if page.status_code == 200 else 'Error'

    print('Reading page...')

    # create BS4 object
    soup = BeautifulSoup(src, 'html.parser')
    #print(soup)
    # CSS selector of specific div tag targeted for scraping
    # container = soup.select('#vanilla_discussion_index > div.container > div.row > div.content.column > div.CommentsWrap > div.DataBox.DataBox-Comments > ul')

    # select and store div classes of targets (title, date, summary, platform, metascore, userscore)
    title = soup.find_all('a', class_='title')
    date = soup.select('.clamp-details')
    desc = soup.select('.summary')
    platform = soup.find_all('span', class_='data')
    metascore = soup.find_all('div', class_ = 'metascore_w large game positive')
    userscore = soup.find_all('div', class_ = 'metascore_w user large game positive')

    #print(list(title)[0:3])
    # print(list(metascore)[0:3])
    # print(list(userscore)[0:3])

    # parse/scrape data and store in all_data
    print('Parsing data...\n')

    for t, dat, d, p, m, u in zip(title, date, desc, platform, metascore, userscore):
        all_data.append([t.get_text(strip=True, separator='\n'),
                         dat.find('span', class_=False).get_text(strip=True),
                         d.get_text(strip=True, separator='\n'),
                         p.get_text(strip=True, separator='\n'),
                         m.get_text(strip=True, separator='\n'),
                         u.get_text(strip=True, separator='\n')])

    print(i, 'iteration, {}% complete.'.format(round(i/page_limit, 4) * 100))

# write to csv file
print('Writing to CSV...')

with open('metacritic_test_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['title', 'release date', 'summary', 'platform', 'metascore', 'userscore']) # column names
    for row in all_data:
        writer.writerow(row)



# End program
print('Done')
