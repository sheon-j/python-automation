import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime
import time

import warnings
warnings.filterwarnings(action='ignore')

def crawler(key_word, dir_name='.'):
    # Selenium Scroll Action
    def scroll_action(url):
        driver.get(url)
        time.sleep(.5)
        # 스크롤 내리기
        last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True: 
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(.5)
            new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_page_height == last_page_height:
                time.sleep(.5)
                if new_page_height == driver.execute_script("return document.documentElement.scrollHeight"):
                    break
            else:
                last_page_height = new_page_height
        # get resource
        html = driver.page_source
        return html

    # Selenium Scroll and More Action
    def comment_action(url):
        driver.get(url)
        time.sleep(.5)
        # 스크롤 내리기
        last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True: 
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(.5)
            new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_page_height == last_page_height:
                time.sleep(.5)
                if new_page_height == driver.execute_script("return document.documentElement.scrollHeight"):
                    break
            else:
                last_page_height = new_page_height
        # 유튜브 팝업 닫기
        try:
            driver.find_element_by_css_selector("#dismiss-button > a").click()
        except:
            pass
        # 유튜브 대댓글 열기
        elements = driver.find_elements_by_css_selector("#more-replies > a")
        if elements:
            for element in elements :
                element.send_keys(Keys.ENTER)
                time.sleep(.5)
                element.click()
        else:
            pass
        # get resource
        html = driver.page_source
        return html

    # Beautiful Soup URL Parsing
    def get_url_list(html):
        soup = BeautifulSoup(html, 'html.parser')
        # get url
        url_list = [a.get('href') 
                    for a in soup.select('a#video-title') 
                    if not 'shorts' in a.get('href')]
        return url_list

    # Beautiful Soup Comment Parsing
    def get_comment(html):
        soup = BeautifulSoup(html, 'html.parser')
        if soup.select("yt-formatted-string#content-text"):    
            comment_dict = {}
            # title
            comment_dict['title'] = soup.select_one('h1 > yt-formatted-string').text
            # id
            comment_dict['id'] = [
                s.text.strip() for s in soup.select('#author-text span.style-scope')
            ]
            # comment
            comment_dict['comment'] = [
                p.text for p in soup.select("yt-formatted-string#content-text")
            ]
            # url
            comment_dict['url'] = url_list[0]
            # search
            comment_dict['search'] = search.replace('+', ' ')
            return comment_dict
        else:
            return None

    # set driver
    driver = webdriver.Chrome('./chromedriver')
    driver.implicitly_wait(3)
    driver.set_window_size(800, 600)

    # result = '베스킨라빈스 오레오 쿠키앤 스트로베리'
    search = key_word.replace(' ', '+')
    youtube_url ='https://www.youtube.com'
    query_url = f'/results?search_query={search}&sp=CAISBAgEEAE%253D'

    # scroll video links
    html = scroll_action(youtube_url + query_url)
    url_list = get_url_list(html)
    url_list = [youtube_url + a for a in url_list]
    print(f'크롤링 타겟 URL은 총 {len(url_list)}개 입니다.')
    print(*url_list, sep="\n")
    print('-'*45)

    comment_list = []
    url_num = 1
    for url in url_list:
        print(f'{url_num}번 크롤링', end=' ')

        # selenium action
        html = comment_action(url)
        # soup parsing
        data = get_comment(html)
        if not data:
            print("댓글 없음.")
            pass

        else:
            df = pd.DataFrame(data)
            comment_list.append(df)

            print(f'총 {len(df)}개 완료.')

        url_num += 1

    driver.close()
    print('-'*45)

    df = pd.concat(comment_list)
    print(f'크롤링된 댓글은 총 {len(df)}개 입니다.')

    csv_name = dir_name + '/result_' + datetime.now().strftime('%Y%m%d') +'.csv'
    df.to_csv(csv_name, mode = 'w', index=False)
