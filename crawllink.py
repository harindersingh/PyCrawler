import logging
import datetime
import os
import sys
import requests
from bs4 import BeautifulSoup

MAX_DEPTH = 40
url_mapper = {}

def crawl_valid_url(url):
    pass

def crawl_visit_url(url, logger):
    """
        Visits a webpage

        Parameters
        ----------
        url : String
            visit the url provided
        logger : Log object 
            used for logging events

        Returns
        -------
        forward_links[]
            BeautifulSoup object for the full webpage of requested url
    """
    page = requests.get(url)
    if page.status_code == 200:
        #OK
        logger.debug("Response on hitting %s : %s The request is OK", url, page.status_code)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup
    elif page.status_code == 400:
        #Bad Request
        logger.debug("Response on hitting %s : %s \
            The request cannot be fulfilled due to bad syntax", url, page.status_code)
    elif page.status_code == 401:
        #Unauthorized
        logger.debug("Response on hitting %s : %s \
            The request was a legal request, but the server is refusing to respond to it. \
            For use when authentication is possible but has failed or not yet been provided", 
            url, page.status_code)
    elif page.status_code == 403:
        #Forbidden
        logger.debug("Response on hitting %s : %s The request was a legal request, \
            but the server is refusing to respond to it", url, page.status_code)
    elif page.status_code == 404:
        #Not Found
        logger.debug("Response on hitting %s : %s \
            The requested page could not be found but may be available again in the future",
            url, page.status_code)
    else:
        logger.error("Requested could not be processed, please check url %s", url)

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

def crawl_link_collector(soup, maxDepth, logger):
    """
        Takes a webpage, crawls it to find other web urls 
        which have not been visited yet and queues them 
        to visit next

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
    # Create for loop to filter the links within page
    forward_links = []
    for item in link_lists:
        temp_link = item.get('href')
        if 'http' in temp_link or 'www' in temp_link and maxDepth >= 0:
            #crawl a url only once
            if temp_link in url_mapper:
                url_mapper[temp_link] += 1
                logger.debug("%s already queued or visited", temp_link)
            else:
                maxDepth -= 1
                logger.debug("Visited %s, %d more links can be crawled", temp_link, maxDepth)
                url_mapper[temp_link] = 1
                forward_links.append(item.get('href'))   
            if maxDepth == 0:
                return forward_links  
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
    soup = crawl_visit_url(seed_url, logger)
    forward_links = crawl_link_collector(soup, maxDepth, logger)
    logger.debug("Web urls obtained on hitting %s, %d more can be crawled", 
        seed_url, maxDepth)

def main():
    logger = crawllink_log()
    logger.debug("Logger is set up")
    #crawl_spider("http://python.org", 1, logger)
    crawl_spider(str(sys.argv[1]), int(sys.argv[2]), logger)

if __name__ == "__main__":
    main()