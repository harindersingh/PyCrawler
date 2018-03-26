import logging
import datetime
import os

def log_crawllink():
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

def main():
    logger = log_crawllink()
    

    """
        Summary line.

        Extended description of function.

        Parameters
        ----------
        arg1 : int
            Description of arg1
        arg2 : str
            Description of arg2

        Returns
        -------
        int
            Description of return value

    """

if __name__ == "__main__":
    # execute only if run as a script
    main()