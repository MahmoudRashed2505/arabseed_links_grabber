import requests
from bs4 import BeautifulSoup
from os import system as sys
from selenium import webdriver
from time import sleep
from datetime import datetime
episodes_links = []
episode_pages = []
download_pages = []

def gtDownloadPages():
    sys('cls')
    url = input('Enter arabseed link: ')
    website = requests.get(url)
    website_text = website.text

  

    soup = BeautifulSoup(website_text, 'lxml')

    episodes_list = soup.find('div', class_='ContainerEpisodesList')
    episodes = episodes_list.find_all('a')
    print("Getting Episodes")
    for episode in episodes:
        
        episodes_links.append(episode.get('href'))
    print("Getting Episode Links")
    for episode in episodes_links:
        
        website = requests.get(episode).text
        soup = BeautifulSoup(website, 'lxml')
        episode_pages.append(soup.find('a', class_='downloadBTn').get('href'))

    print("Getting Episodes Download pages.")
    for episode_page in episode_pages:
        
        website = requests.get(episode_page).text
        soup = BeautifulSoup(website, 'lxml')
        downloadBlock = soup.find('ul', class_='download-items')
        download_pages.append(downloadBlock.find('a', class_="downloadsLink HoverBefore ArabSeedServer").get('href'))

    with open('downloadlinks.txt','a') as downloadLinks:
        for page in download_pages:
            downloadLinks.write(page+'\n')
    filename = input("Enter File Name: ")
    sys('cls')
    op = webdriver.ChromeOptions()
    op.add_argument("--log-level=3")
    op.add_argument('headless')
    fname = filename + '.txt'
    f = open(fname, "a")
    print("Opened The txt file....")
    directList = []
    for link in download_pages:
        browser =webdriver.Chrome(options=op)
        print("Opening Download Page")
        browser.get(link)
        p = browser.current_window_handle
        sleep(7)
        print("Clicking Download BTN..")
        browser.find_element_by_xpath('/html/body/div/div[3]/div[2]/div[3]/div/form/div/div[3]/center/button').click()
        sleep(2)
        print("Switching Tabs")
        browser.switch_to_window(p)
        print("Getting Direct Link")
        downloadLink = browser.find_element_by_xpath('/html/body/div/div[3]/div[2]/div[3]/span/a').get_attribute('href')
        print("Save direct link to the text file")
        f.write(downloadLink+'\n')
        directList.append(downloadLink)
        sleep(2)
        print("Closing Window")
        browser.quit()
        print("---------------------------------------------------------------")
    f.close()
    print("Adding Direct Link to the Qeue")
    for link in directList:
        sys("idman /d {} /a".format(link))
    print("Starting the Qeue")
    sys('idman /s')


   

gtDownloadPages()


