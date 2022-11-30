from custom_parser.PageParser import PageParser

import re

def main():
    jobs = [
        'software engineer in LA'
    ]
    
    pageParser : PageParser = PageParser(jobs)
    

    """
    f = open("res.txt", "r+")
    res = bytes(f.read().replace(' ','').replace('\n',''), "utf-8").decode("unicode_escape")
    res = bytes(res, "utf-8").decode("unicode_escape")
    urls = re.findall("\"https?:\/\/[a-zA-Z0-9+%\-?=\\\/#_?&;.]*\"", res)

    cleanedUrls : list = list()
    for url in urls:
        cleanedUrl = bytes(url[1:-1], "utf-8").decode("unicode_escape")
        cleanedUrls.append(cleanedUrl)
    """  
if __name__ == "__main__":
    main()