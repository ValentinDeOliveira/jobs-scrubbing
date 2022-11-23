from scrapy.crawler import CrawlerProcess
from jobs_parser.jobs_parser.spiders.JobParser import JobsParser
from custom_parser.PageParser import PageParser

import re

def main():
    jobs = [
        'software engineer in LA'
    ]
    
    pageParser : PageParser = PageParser(jobs)
    """
    f = open("res3.txt", "r+")
    res = f.read()
    #res = bytes(f.read(), "utf-8").decode("unicode_escape")
    urls = re.findall('(?P<url>https?://[^\s]+),', res)

    print(type(res))

    cleanedUrls : list = list()
    for url in urls:
        cleanedUrl = bytes(url[:-1], "utf-8").decode("unicode_escape")
        cleanedUrls.append(cleanedUrl)
        
    print(res)
    """
    """
    f = open("tmp.txt", "rb+")        
    res = f.read()

    ind = res.find('[[['.encode('UTF-8'))
    completeData = res[ind:]
    
    urls = re.findall("https://.*\",{1}",completeData.decode("UTF-8"))
    for encodedUrl in urls:
        # remove useless '\'
        cleanedUrl = re.sub('\\\(?![u])', '', encodedUrl[:-2])
        # convert escaped unicode character
        url = bytes(cleanedUrl, "utf-8").decode("unicode_escape")
    """
if __name__ == "__main__":
    main()