import logging
import datetime
import os
import sys
import requests
import csv
from bs4 import BeautifulSoup

url_mapper = {}

def crawl_store_links(url, child_links, logger):
    """
        Function used to crawl webpages

        Parameters
        ----------
        url : string
            Base url that will be the seed url
        child_links : list 
            Child links of base url in a list
        logger : Log object used for logging events

        Returns
        -------
        Stores a list of urls in the given webpage 
        in a csv file
    """
    url_file = url.strip('http:')
    url_file = url_file.strip('~!@#$%^&*()/\\,}{;:.')
    url_file = url_file + ".csv"
    with open(url_file, 'w') as f:
        csvfile = csv.writer(f)
        try:
            csvfile.writerow(['Parent Link', ' ChildLink'])
            for item in child_links:
                csvfile.writerow([url, " " + item])
        except csv.Error as e:
            logger.error('file %s, line %d: %s' % (url_file, csvfile.line_num, e))

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
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        logger.debug(page.raise_for_status())
        return soup
    except requests.exceptions.HTTPError as err:
        logger.error(err)
    except requests.exceptions.ConnectionError as err:
        logger.error("Error Connecting:", err)
    except requests.exceptions.Timeout as err:
        logger.err("Timeout Error:", err)
    except requests.exceptions.RequestException as err:
        logger.error("Invalid request", err)
    
def crawllink_log():
    """
        Setup logging for scraplink
        Creates a logfile with scraplink_datetime.txt format with DEBUG 
        level logging

        Returns:
        Logger object which will be used for logging 

    """
    logger = logging.getLogger()
    logfile = "crawllink_" + datetime.datetime.now().strftime("%y-%m-%d-%H-%M") \
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
        maxDepth : Integer
            max number of links that need to be crawled
        logger : Log object 
            used for logging events

        Returns
        -------
        forward_links[]
            List of web urls to be crawled further
        maxDepth
            return updated maxDepth variable
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
                return forward_links, maxDepth  
    return forward_links, maxDepth

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
    logger.debug("Base URL = %s and MaxDepth = %d.", seed_url, maxDepth)
    soup = crawl_visit_url(seed_url, logger)
    forward_links, maxDepth = crawl_link_collector(soup, maxDepth, logger)
    logger.debug("Web urls obtained on hitting %s, %d more can be crawled", 
        seed_url, maxDepth)
    crawl_store_links(seed_url, forward_links, logger)

def main():
    logger = crawllink_log()
    logger.debug("Logger is set up")
    crawl_spider(str(sys.argv[1]), int(sys.argv[2]), logger)

if __name__ == "__main__":
    main()