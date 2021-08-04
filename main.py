import requests
from bs4 import BeautifulSoup
from os import system as sys
from downloader import getDownloadLinks
from selenium import webdriver
from time import sleep
from datetime import datetime
browser =webdriver.Chrome()


def gtDownloadPages():
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
    getDownloadLinks(download_pages,input("What are you Download: "))

def getDownloadLinks(list,filename = str(datetime.now())):
    fname = filename + '.txt'
    f = open("fname", "a")
    directList = []
    for link in list:
        browser.get(link)
        p = browser.current_window_handle
        sleep(7)
        browser.find_element_by_xpath('/html/body/div/div[3]/div[2]/div[3]/div/form/div/div[3]/center/button').click()
        sleep(2)
        browser.switch_to_window(p)
        downloadLink = browser.find_element_by_xpath('/html/body/div/div[3]/div[2]/div[3]/span/a').getAttribute('href')
        f.write(downloadLink+'\n')
        directList.append(downloadLink)
        browser.close()
    f.close()
    for link in directList:
        sys("idman /d {} /a".format(link))
    sys('idman /s')




