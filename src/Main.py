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
if __name__ == "__main__":
    main()