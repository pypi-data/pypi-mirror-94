from selenium import webdriver
from selenium.webdriver.common.keys import Keys       # Keyboard inputs
from selenium.webdriver import ActionChains
import time
import pandas as pd


def search_arxiv(query, max_page=10):
    driver = webdriver.Chrome(r'..\chrome_drivers\chromedriver')
    data = []
    try:
        driver.maximize_window()
        driver.get('https://arxiv.org/')

        # Searching Arxiv
        elem = driver.find_element_by_name('query')
        # Clearing any initial words
        elem.clear()
        elem.send_keys(query)
        elem.send_keys(Keys.RETURN)

        # Checking whether in condensed matter
        # assert "Condensed Matter" in driver.title
        # To open a link in a new tab
        page_at = 1
        while True:
            finds = driver.find_elements_by_class_name('arxiv-result')
            for link in finds:
                try:
                    # ActionChains(driver).move_to_element(link).key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
                    title = link.find_element_by_class_name('title').text
                    link_val = link.find_element_by_link_text('pdf').get_attribute('href')
                    author = link.find_element_by_class_name('authors').text
                    #print('Title:', title)
                    #print('Link:', link_val)
                    #print('Authors:', author)
                    citations = link.find_elements_by_class_name('is-size-7')
                    for citation in citations:
                        if 'Submitted' in citation.text:
                            citation_val = citation.text
                            data.append([title, link_val, author, citation_val])
                            #print('Citation:', citation_val)
                    #print('----------------------------------------------------------------')
                except Exception as ex:
                    print(ex)
                    # main-container > div.content > ol > li:nth-child(49) > p:nth-child(5)
            # find.click()
                # actions.key_down(Keys.CONTROL).click(find).key_up(Keys.CONTROL).perform()# Clearing any initial words
            if driver.find_element_by_link_text('Next'):
                driver.find_element_by_link_text('Next').click()
            else:
                break
            page_at = page_at + 1
            if page_at >= max_page:
                break
    except Exception as ex:
        print(ex)
    finally:
        driver.quit()
        string = query.replace(" ", "")
        df = pd.DataFrame(data, columns=['Title', 'Link', 'Authors', 'Citations'])
        file_path = r'..\data\\'
        file_path = file_path + string + '_arxiv.csv'
        df.to_csv(file_path, index=False, header=True)
    return True


def search_prl(query, max_page=10):
    driver = webdriver.Chrome(r'..\chrome_drivers\chromedriver')
    data = []
    try:
        driver.maximize_window()
        driver.get('https://journals.aps.org/prl/')

        # Searching Arxiv
        elem = driver.find_element_by_name('q')
        elem.clear()
        elem.send_keys(query)
        elem.send_keys(Keys.RETURN)

        # Checking whether in condensed matter
        # assert "Condensed Matter" in driver.title
        # To open a link in a new tab
        page_at = 1
        while True:
            finds = driver.find_elements_by_class_name('article-result')
            for link in finds:
                try:
                    # ActionChains(driver).move_to_element(link).key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
                    title = link.find_element_by_class_name('title')
                    title_val = title.text
                    link_val = title.find_element_by_tag_name('a').get_attribute('href')
                    author = link.find_element_by_class_name('authors').text
                    citation = link.find_element_by_class_name('citation').text
                    data.append([title_val, link_val, author, citation])
                    #print('-----------------PRL------------------------')
                    #print('Title:', title_val)
                    #print('Link:', link_val)
                    #print('Author:', author)
                    #print('Citation:', citation)
                    #print('--------------------------------------------------------------')
                except Exception as ex:
                    print(ex)
            # Earlier there was an error as the data wasn't loaded so use sleep and action
            if page_at == 1:
                driver.find_element_by_link_text('I Agree').click()
            #actions = ActionChains(driver)
            #actions.move_to_element(element).click(element).perform()
            #time.sleep(10)
            # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            element = driver.find_element_by_xpath('//*[@id="search-main"]/div[2]/div/ul/li[last()]/button')
            if page_at > max_page:
                break
            else:
                element.click()
                time.sleep(10)
                page_at = page_at + 1
    except Exception as ex:
        print(ex)
    finally:
        driver.quit()
        df = pd.DataFrame(data, columns=['Title', 'Link', 'Authors', 'Citations'])
        file_path = r'..\data\\'
        string = query.replace(" ", "")
        file_path = file_path + string + '_prl.csv'
        df.to_csv(file_path, index=False, header=True)
    return True


def search_gs(query, max_page=10):
    driver = webdriver.Chrome(r'..\chrome_drivers\chromedriver')
    data = []
    try:
        driver.maximize_window()
        driver.get('https://scholar.google.com/')

        # Searching Arxiv
        elem = driver.find_element_by_name('q')
        elem.clear()
        elem.send_keys(query)
        elem.send_keys(Keys.RETURN)

        # Checking whether in condensed matter
        # assert "Condensed Matter" in driver.title
        # To open a link in a new tab
        page_at = 1
        element = driver.find_element_by_link_text('Next')
        while element:
            datus = driver.find_elements_by_css_selector('div.gs_r.gs_or.gs_scl')
            for data_val in datus:
                try:
                # ActionChains(driver).move_to_element(link).key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
                    # title = link.find_element_by_class_name('gs_rt')
                    title = data_val.find_element_by_class_name('gs_rt')
                    auth = data_val.find_element_by_class_name('gs_a')
                    #print('-------------------GS-------------------------')
                    #print('Title:', title.text)
                    #print('Link:', title.find_element_by_tag_name('a').get_attribute('href'))
                    #print('Author:', auth.text)
                    data.append([title.text, title.find_element_by_tag_name('a').get_attribute('href'), auth.text])
                    # print('Author:', link.find_element_by_class_name('gs_a').text)
                    # print('Citation:', link.find_element_by_class_name('citation').text)
                    #print('--------------------------------------------------------------')
                except Exception as ex:
                    print(ex)
            # Earlier there was an error as the data wasn't loaded so use sleep and action

            # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            element.click()
            time.sleep(10)
            element = driver.find_element_by_link_text('Next')
            page_at = page_at + 1
            # time.sleep(3)
            if page_at > max_page:
                break
    except Exception as ex:
        print(ex)
    finally:
        driver.quit()
        df = pd.DataFrame(data, columns=['Title', 'Link', 'Authors'])
        file_path = r'..\data\\'
        string = query.replace(" ", "")
        file_path = file_path + string + '_gs.csv'
        df.to_csv(file_path, index=False, header=True)
    return True
