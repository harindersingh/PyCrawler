# Welcome to PyCrawler

ScrapLink is a crawler that starts with a url on the web (ex: http://python.org), fetches the web-page corresponding to that url, and parses all the links on that page into a repository of links. Next, it fetches the contents of any of the url from the repository just created, parses the links from this new content into the repository and continues this process for all links in the repository until stopped or after a given number of links are fetched.

"Structure of Code is Key"

## Commands

* `python .\crawllink.py url maxDepth` - Specify the seed url for crawling and a max number links that should be crawled
* `python .\crawllink.py http://python.org 40` - Sample run

## Project layout

    crawllink.py    # The crawler program
    logs/
        scraplink_datetime.txt  # Log for the last run
    tests/
        # yet to be done
    .gitignore  # mention the files or directories to be ignored by git
    CHANGELOG
    LICENCE
    Makefile
    README.md
    requirements.txt
    setup.py
    TODO 
