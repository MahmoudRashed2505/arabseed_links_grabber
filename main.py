import requests
from bs4 import BeautifulSoup
from os import system
url = input('Enter arabseed link: ')


website = requests.get(url)
website_text = website.text

episodes_links = []
episode_pages = []
download_pages = []

soup = BeautifulSoup(website_text, 'lxml')

episodes_list = soup.find('div', class_='ContainerEpisodesList')
episodes = episodes_list.find_all('a')

for episode in episodes:
    episodes_links.append(episode.get('href'))

for episode in episodes_links:
    website = requests.get(episode).text
    soup = BeautifulSoup(website, 'lxml')
    episode_pages.append(soup.find('a', class_='downloadBTn').get('href'))


for episode_page in episode_pages:

    website = requests.get(episode_page).text
    soup = BeautifulSoup(website, 'lxml')
    downloadBlock = soup.find('ul', class_='download-items')
    download_pages.append(downloadBlock.find('a', class_="downloadsLink HoverBefore ArabSeedServer").get('href'))

with open('downloadlinks.txt','a') as downloadLinks:
    for page in download_pages:
        downloadLinks.write(page+'\n')

system('downloadLinks.txt')




