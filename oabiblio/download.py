from oabiblio.journal_list import *
from oabiblio.parser import *
import urllib2
import urllib
import os.path

import oabiblio.logger
LOG = oabiblio.logger.log(__name__)

def download_doaj(numpages):
    """
    Download pages from DOAJ that contain CC-licence journals
    """
    LOG.debug("starting download of %s pages from DOAJ for cc-licenced journals"
                  % str(numpages))

    if not os.path.exists("data/raw/doaj/"):
        LOG.debug("Creating directory data/raw/doaj")
        os.makedirs("data/raw/doaj")

    i=1
    while i < numpages:
        query_url = "http://www.doaj.org/doaj?func=licensedJournals&p=%s&uiLanguage=en" % str(i)
        filename = "doaj_cc_licenced_journals_page_%s.html" % str(i)
        filepath = os.path.join("data/raw/doaj/", filename)
        LOG.debug("Requesting DOAJ page: %s" % query_url)
        
        try:
            LOG.debug("writing file to: %s" % filepath)
            file, headers = urllib.urlretrieve(query_url, filepath)
            LOG.debug("wrote page to file: %s" % file)

        except IOError:
            LOG.error("DOAJ record %s failed with IOError"
                            % query_url)
            
        i+=1


def download_crossref(deprecorddates):
    """
    Download Crossref deposition records for the specified dates
    """
              
    if not os.path.exists("data/raw/crossref/"):
        LOG.debug("Creating directory data/raw/crossref")
        os.makedirs("data/raw/crossref")
        
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    if deprecorddates == 0:
        years = range(6,15)
        LOG.debug("Starting download of Crossref deposition records")

    else:
        LOG.debug("Starting download of Crossref deposition records for %s"
                  % str(deprecorddates))
        times = deprecorddates.split('-')
        if times[0][0] == 'Q':
            raise NotImplementedError
        else:
            years = range(int(times[0]), (int(times[1]) + 1))

    for year in years:
        yearstring = "%02d" % year
        for quarter in quarters:
            quarterstring = quarter+yearstring
            query_url = "http://www.crossref.org/06members/%squarterly_deposits.html" % quarterstring
            filename = "crossref_depositrecords_%s.html" % quarterstring
            filepath = os.path.join("data/raw/crossref/", filename)
            LOG.debug("Downloading Crossref deposition records from %s"
                      % query_url)

            try:
                LOG.debug("writing file to: %s" % filepath)
                file, headers = urllib.urlretrieve(query_url, filepath)
                LOG.debug("wrote page to file: %s" % file)

            except IOError:
                LOG.error("Crossref record %s failed with IOError"
                              % query_url)



            

        

        
