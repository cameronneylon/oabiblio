import urllib
import re
from BeautifulSoup import BeautifulSoup
import urllib2
from oabiblio.exceptions import HTTPError

class Journal():
    """A class to represent a specific journal

    The class is used to obtain information on a specific journal
    including licence, publisher, and number of publications.
    """

    def __init__(self, name = None, shortname = None, issn = None, licence = None):
        self.name = name
        self.shortname = shortname
        self.issn = issn
        self.licence = licence
        self.webpage = None
        self.pubs = {}

    def __str__(self):
        return str(self.name) + " ISSN: " +str(self.issn)

    def get_licence_from_doaj(self, option = None):
        query_url = "http://www.doaj.org/doaj?func=findJournals&uiLanguage=en&hybrid=&query="

        if (option == None or option == 'name' or option == 'n'):
            query = self.name

        elif (option == 'shortname' or option == 's'):
            query = self.shortname

        elif (option == 'issn' or option == 'i'):
            query = self.issn

        else:
            return False

        query = urllib.quote_plus(query)
        url = query_url + query
        try:
            response = urllib2.urlopen(url)

        except HTTPError:
            return False

        soup = BeautifulSoup(response.read())

        # Check there is only one result
        results_txt = re.compile("(Found )" + "(\\d)" + "( journals matching your query)")
        page_line = soup.find('p', text = results_txt)
        results = int(results_txt.search(page_line).group(2))

        if results != 1:
            return False

        # Get the licence information
        licence_txt = re.compile("legalcode$")
        licence_info = soup.find('a', href=licence_txt)
        self.licence = licence_info['href']

    def isCCBY(self):
        if self.licence == "http://creativecommons.org/licenses/by/3.0/legalcode":
            return True
        else:
            return False
        
    def isCCBYNC(self):
        if self.licence == "http://creativecommons.org/licenses/by-nc/3.0/legalcode":
            return True
        else:
            return False

