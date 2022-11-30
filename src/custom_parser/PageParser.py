from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import requests
import scrapy
import re
import urllib.request
from selenium.webdriver.remote.webelement import WebElement
from pyvirtualdisplay import display

class PageParser:
    m_driver: webdriver.Chrome

    BASE_URL = 'https://www.google.com/search?q='
    BASE_SEARCH_OPTIONS = '&asearch=jb_list&cs=1&async=_id:VoQFxe,_pms:hts,_fmt:pc&rciv=jb&nfpr=0&start='
    OFFER_SEARCH_OPTION = 'sclient=gws-wiz-serp&ibp=htl;jobs&sa=X#htivrt=jobs&fpstate=tldetail&htidocid='
    CLOSING_STYLE="</style>".encode('UTF-8')

    m_url = 'https://www.google.com/search?q=software+engineer+in+LA&sclient=gws-wiz-serp&ibp=htl;jobs&sa=X'
    def __init__(self, _jobs : list):
        #m_display = display.Display(visible=0, size=(800, 800))  
        #m_display.start()

        self.m_driver = webdriver.Chrome()
        
        self.m_driver.get(self.m_url)
        
        WebDriverWait(self.m_driver, timeout=10).until(lambda d: d.title != "")
                
        title = self.m_driver.title
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
        
        WebDriverWait(self.m_driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@jscontroller="soHxf"]'))).click()

    URL_ID="htidocid="
    N_OFFERS_BLOCK=3

    def parse(self, _url: str):   
        # append the options needed for the search
        urlWithArgs = _url + self.BASE_SEARCH_OPTIONS

        # get all the offers from 0 to 10*N_OFFERS_BLOCK
        for i in range(0,self.N_OFFERS_BLOCK):
            # add the index of offer block
            scrolledUrl = urlWithArgs + str(i * 10)
            # get the data from the url
            result = requests.get(scrolledUrl)
            
            # A lot of crap to remove, we will get the data after the </style>
            startingHTMLIndex = result.content.find(self.CLOSING_STYLE) + len(self.CLOSING_STYLE)
            decodedData  = result.content[startingHTMLIndex:].decode("unicode_escape")
            # interesting data is at the end of the file and start by [[[
            # we will find the index of those [[[ 
            ind = decodedData.find("[[[")

            # remove spaces and \n, decode unicode characters
            completeData = bytes(decodedData[ind:].replace(' ','').replace('\n',''), "utf-8").decode("unicode_escape")
            # data is encoded twice with unicode, meaning that we need to decode data again
            completeData = bytes(decodedData, "utf-8").decode("unicode_escape")

            """
                completeData contains JSON with a lot of unreadable data.
                From this JSON we will get all the google's link.
                Those link are link to a single offer
            """

            # get all the google links from the JSON
            urls = re.findall("\"https:\/\/www.google.com[a-zA-Z0-9+%\-?=\\\/#_?&;.]*\"", completeData)

            """
                Foreach url:
                    need to decode unicode characters from the URL
                    get a particular id from this url
                    append the parsed id to a different url that will redirect to a single offer
            """
            for encodedUrl in urls:
                # convert escaped unicode character
                cleanedUrl = bytes(encodedUrl[1:-1], "utf-8").decode("unicode_escape")
                
                
                urlIdPos=cleanedUrl.rfind(self.urlId)
                urlId = cleanedUrl[urlIdPos + len(self.URL_ID):len(cleanedUrl)]
                
                finalUrl= _url + self.OFFER_SEARCH_OPTION + urlId
                
                self.parseOffer(finalUrl)
            break
            
        self.m_driver.close()
        
    
    RIGHT_CONTAINER = "jolnDe" 
    OFFER_DESCRIPTION = "WbZuDe" 
        
    def parseOffer(self, _url: str):
        self.m_driver.get(_url)

        #container : WebElement = WebDriverWait(self.m_driver, timeout=10).until(lambda d: d.find_element(By.CLASS_NAME, self.RIGHT_CONTAINER))    
        #descriptionContainer : WebElement= container.find_element(By.XPATH, './/span[@class=\"' + self.OFFER_DESCRIPTION + '\"]')
        
        # get container that holds the detailed description of the offer
        descriptionContainer : WebElement= WebDriverWait(self.m_driver, timeout=10).until(lambda d: d.find_element(By.XPATH, './/span[@class=\"' + self.OFFER_DESCRIPTION + '\"]'))
        
        fullDescription = descriptionContainer.get_attribute('innerHTML')        
        
        f = open("resultOffer.txt", "a")
        f.write(fullDescription)
        f.write("\n-------------------------------------------------------------------------\n")
        f.close()
