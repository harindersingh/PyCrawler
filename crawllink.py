import logging
import datetime
import os
import requests
from bs4 import BeautifulSoup

MAX_DEPTH = 5

def crawllink_log():
    """
        Setup logging for scraplink
        Creates a logfile with scraplink_datetime.txt format with DEBUG 
        level logging

        Returns:
        Logger object which will be used for logging 

    """
    logger = logging.getLogger()
    logfile = "scraplink_" + datetime.datetime.now().strftime("%y-%m-%d-%H-%M") \
            + ".txt"
    logfile = os.path.join("logs", logfile)
    handler = logging.FileHandler(filename=logfile, mode="w")
    formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

def crawl_link_collector(soup, logger):
    """
        Function used to crawl webpages

        Parameters
        ----------
        soup : BeautifulSoup object
            used to perform operations on current webpage contents
        logger : Log object 
            used for logging events

        Returns
        -------
        forward_links[]
            List of web urls to be crawled further
    """
    # Pull all instances of <a> tag within page
    link_lists = soup.find_all('a')
    # Create for loop to filter the links to sections within page
    forward_links = []
    for item in link_lists:
        temp_link = item.get('href')
        if ('http' in temp_link or 'www' in temp_link):
            forward_links.append(item.get('href'))     

    return forward_links

def crawl_spider(seed_url, maxDepth, logger):
    """
        Function used to crawl webpages

        Parameters
        ----------
        url : string
            Base url that will be the seed url
        maxDepth : integer
            Max depth till where the crawler will work and stop thereafter
        logger : Log object used for logging events

        Returns
        -------
        Null
    """
    if maxDepth:
        logger.debug("Base URL = %s and MaxDepth = %d.", seed_url, maxDepth)
    else:
        maxDepth = MAX_DEPTH
        logger.debug("Base URL = %s and MaxDepth = %d.", seed_url, maxDepth)
    page = requests.get(seed_url)
    logger.debug("Response on hitting %s %s ",seed_url, page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')
    forward_links = crawl_link_collector(soup, logger)
    logger.debug("Web urls obtained on hitting ", seed_url)

def main():
    logger = crawllink_log()
    logger.debug("Logger is set up")
    crawl_spider("http://python.org", 1, logger)

if __name__ == "__main__":
    # execute only if run as a script
    main()