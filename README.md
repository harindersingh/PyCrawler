# PyCrawler
Crawler using Python 3

ScrapLink is a crawler that starts with a url on the web (ex: http://python.org), fetches the web-page corresponding to that url, and parses all the links on that page into a repository of links. Next, it fetches the contents of any of the url from the repository just created, parses the links from this new content into the repository and continues this process for all links in the repository until stopped or after a given number of links are fetched.

"Structure of Code is Key"

./LICENSE - Lawyering Up <br/>
.setup.py - Package and distribution management. <br/>
./requirements.txt - Development dependencies. <br/>
./tests - Package integration and unit tests. <br/>
./PyCrawlerDocs - Documentation for the project, <br/>
visit ./PyCrawlerDocs/site/index.html after cloning the project<br/>
./logs - Logs for the program execution

 `python .\crawllink.py url maxDepth` - Specify the seed url for crawling and a max number links that should be crawled<br/>
 `python .\crawllink.py http://python.org 40` - Sample run<br/>
 `cat url.csv` - Shows the urls crawler, select any one child link and crawl it using the first command<br/>
 `cat pythonorg.csv` - Shows the list of urls crawled on http://python.org<br/>
