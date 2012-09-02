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
        request_url = "http://www.doaj.org/doaj?func=licensedJournals&p=%s&uiLanguage=en" % str(i)
        LOG.debug("Requesting page: %s" % request_url)
        
        try:
            response = urllib2.urlopen(request_url)
        except urllib2.HTTPError, e:
            if e.code == "404":
                LOG.error("DOAJ page %s failed with HTTP Error code %s"
                      % request_url, e.code)
            
        LOG.debug("Responding URL: %s" % response.geturl())
        filename = "doaj_cc_licenced_journals_page_%s.html" % str(i)
        filepath = os.path.join("data/raw/doaj/", filename)
        with open(filepath, 'w') as f:
            LOG.debug("opening file %s to write doaj page" % filepath)
            f.write(response.read())

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
            LOG.debug("Downloading Crossref deposition records from %s"
                      % query_url)

            try:
                response = urllib2.urlopen(query_url)
                LOG.debug("Responding URL: %s" % response.geturl())
                filename = "crossref_depositrecords_%s.html" % quarterstring
                filepath = os.path.join("data/raw/crossref/", filename)
                with open(filepath, 'w') as f:
                    LOG.debug("opening file %s to write crossref page" % filepath)
                    f.write(response.read())

            except urllib2.HTTPError, e:
                LOG.error("Crossref record %s failed with HTTP Error code %s"
                              % request_url, e.code)



            

        

        
