from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import requests
import scrapy
import re
import urllib.request

class PageParser:
    m_driver: webdriver.Chrome

    BASE_URL = 'https://www.google.com/search?q='
    BASE_SEARCH_OPTIONS = '&asearch=jb_list&cs=1&async=_id:VoQFxe,_pms:hts,_fmt:pc&rciv=jb&nfpr=0&start='

    CLOSING_STYLE="</style>".encode('UTF-8')

    m_url = 'https://www.google.com/search?q=software+engineer+in+LA&sclient=gws-wiz-serp&ibp=htl;jobs&sa=X'
    def __init__(self, _jobs : list):
        m_driver = webdriver.Chrome()
        
        m_driver.get(self.m_url)
        
        title = m_driver.find_element(By.TAG_NAME, 'title').text
        if title == 'Avant d\'accéder à la recherche Google':
            self.parseConsent(self.m_url)
        
        for job in _jobs:
            # replace spaces by "+" to build proper url
            customUrl = self.BASE_URL + job.replace(' ', '+') 
            self.parse(customUrl)
        

    def parseConsent(self, _url: str):
        """
        parseConsent 
            Sometimes google could ask for accepting consent.
            This function allows to accepts all the cookies

        :param _url: url of the page we want to access
        :type _url: str
        """
        self.m_driver.get(_url)
        
        WebDriverWait(self.m_driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@value="Tout accepter"]'))).click()

    def parse(self, _url: str):        
        urlWithArgs = _url + self.BASE_SEARCH_OPTIONS

        
        for i in range(0, 3):
            scrolledUrl = urlWithArgs + str(i * 10)
            
            result = requests.get(scrolledUrl)
                     
            startingHTMLIndex = result.content.find(self.CLOSING_STYLE) + len(self.CLOSING_STYLE)
            decodedData  = result.content[startingHTMLIndex:].decode("unicode_escape")
            ind = decodedData.find("[[[")
            completeData = decodedData[ind:]


            urls = re.findall('(?P<url>https?://[^\s]+),', completeData)


            for encodedUrl in urls:
                # convert escaped unicode character
                cleanedUrl = bytes(encodedUrl[:-1], "utf-8").decode("unicode_escape")
                print(cleanedUrl)
                
                self.parseOffer(cleanedUrl)
                break
            break
            
        self.m_driver.close()
        
    def parseOffer(self, _url: str):
        with urllib.request.urlopen(_url) as f:
            data = f.read().decode('utf-8')

        soup : BeautifulSoup = BeautifulSoup(data)

        pass