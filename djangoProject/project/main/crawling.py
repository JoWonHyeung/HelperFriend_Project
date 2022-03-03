from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

def crawling():
    # 1
    query_txt = "AI"
    res = []
    status = []
    # 2
    chrome_path = "c://tmp//chromedriver.exe"

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(chrome_path, options=options)
    driver.get("https://thinkyou.co.kr/index.asp")
    driver.maximize_window()
    time.sleep(3)

    # 3
    a = ActionChains(driver)
    m = driver.find_element_by_xpath('//*[@id="gnb"]/li[1]/a/span')
    a.move_to_element(m).perform()
    time.sleep(0.5)

    # 4
    driver.find_element_by_xpath('//*[@id="gnb"]/li[1]/ul/li[1]').click()

    driver.find_element_by_xpath('//*[@id="searchFrm"]/div/div/div[1]/select').click()
    driver.find_element_by_xpath('//*[@id="searchFrm"]/div/div/div[1]/select/option[2]').click()

    driver.find_element_by_xpath('//*[@id="searchFrm"]/div/div/div[1]/span/input[1]').click()
    elem = driver.find_element_by_name("searchstr")
    elem.send_keys(query_txt)
    elem.send_keys("\n")
    time.sleep(2)

    # driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[1]/a[3]').click() #참석중 클릭
    # time.sleep(1)

    # 5. url수집
    urls = []
    default_dir = "https://thinkyou.co.kr"
    count = 0

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    all = soup.find('div', 'contestArea')

    allTag = all.find_all('div', 'title')
    allStatus = all.find_all('div', 'statNew')

    for i in allTag:
        a_tag = i.find('a')['href']
        urls.append(default_dir + a_tag)

    for i in allStatus:
        status_tag = i.find('p').get_text()
        status.append(status_tag)
    # 6
    urls_image = []

    import sys
    from urllib.parse import quote

    bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    count = 0
    file_no = 1

    for num in range(0,6):
        driver.get(urls[num])  # 사이트 접속

        html1 = driver.page_source
        soup1 = BeautifulSoup(html1, 'html.parser')

        # Title 수집
        title = soup1.find('dl', 'title').find('h1').get_text()

        # 이미지 확대
        driver.find_element_by_xpath('//*[@id="printArea"]/div[1]/div/div[1]/img').click()

        html2 = driver.page_source
        soup2 = BeautifulSoup(html2, 'html.parser')

        # 이미지 수집
        try:
            photo = soup2.find('div', 'galleryImg').find('img')['src']
        except:
            continue
        else:
            full_image = 'https://thinkyou.co.kr/' + quote(photo)
            urls_image.append(full_image)
            file_no += 1
        time.sleep(1)

    res.append(urls_image)
    res.append(urls)
    res.append(status)
    return res