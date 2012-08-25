# oabiblio: A python library for obtaining data on levels of
# open access adoption
#
# Public Domain Waiver:
# To the extent possible under law, Cameron Neylon has waived all 
# copyright and related or neighboring rights to lablogpost.py
# This work is published from United Kingdom.
#
# See http://creativecommons.org/publicdomain/zero/1.0/
#
# Dependencies: The application requires a range of modules from the
# Python 2.7 standard library including urllib, urllib2, re and csv.
# Python is Copyright 2001-2012 Python Software Foundation
# and used here under the PSF Licence for Python 2.7.2
#
# This code additionally depends on the BeautifulSoupt parsing library.
# Development was done using version 3 of this library but it should
# work with version 4.
#
# Data Sources: The library uses sources such as PubMed and CrossRef
# alongside the Directory of Open Access Journals to obtain data on
# publications and licensing.
#

import urllib2
import urllib
from BeautifulSoup import BeautifulSoup
import re
import csv

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

class JournalList():

    """Abstract class for lists of journals, by publisher or by other criteria"""

    
    def __init__(self, journal_list = None):
        self.journal_list = []
        if not journal_list:
            pass
        elif isinstance(journal_list, list) and isinstance(journal_list[0], Journal):
            self.journal_list.extend(journal_list)

        else:
            raise InputError

    def add_journal(self, journal):
        assert isinstance(journal, Journal)

        self.journal_list.append(journal)

    def load_from_csv(self, filename, verbose = False):

        with open(filename, 'rU') as f:
            reader = csv.DictReader(f)
            for journal in reader:
                j = Journal(**journal)
                self.add_journal(j)

    def write_journal_list(self, filename, verbose = False):

        with open(filename, 'w') as f:
            writer = csv.DictWriter(f, fieldnames = ['name', 'issn', 'licence'])
            writer.writeheader()
            for journal in self.journal_list:
                if verbose:
                    print journal.name
                writer.writerow({'name' : journal.name,
                                 'issn' : journal.issn,
                                 'licence': journal.licence})

    def filter_by_licence(self, licence):

        def is_licence(licence, journal):
            if journal.licence == licence: return True
            else: return False

        filtered_list = [journal for journal in self.journal_list if is_licence(licence, journal)]
        return filtered_list


class Publisher(JournalList):
    """Class to hold lists of journals by a single publisher."""

    pass

class JournalsWithCCLicence(JournalList):

    def __init__(self):
        JournalList.__init__(self)

    def populate(self, test = False):

        try:
            i=1
            while i < 25:
                request_url = "http://www.doaj.org/doaj?func=licensedJournals&p=%s&uiLanguage=en" % str(i)
                response = urllib2.urlopen(request_url)
                soup = BeautifulSoup(response.read())

                p_tags = soup.findAll('p', attrs = {'class' : 'text'})
                journals_list = p_tags[1]
                links = journals_list.findAll('a')
                new_tag =links[0]
                while new_tag:
                    new_journal, next_tag = self.process_journal(new_tag)
                    new_tag = next_tag
                    self.add_journal(new_journal)
                    
                if test == True:
                    i=25
                i+=1

        except urllib2.HTTPError:
            return False                
                


    def process_journal(self, tag, verbose = False):
        """Process a DOAJ journal record from within the list page"""

        journal = Journal(tag.string)
        issn_tag = tag.findNext('b').nextSibling
        issn = issn_tag.lstrip(": ").strip()
        journal.issn = issn
        licence_tag = tag.findNext('a', href=(re.compile("legalcode$")))
        journal.licence = licence_tag['href']

        if verbose:
            print "\n\nJournal:", journal.name
            print "ISSN:", issn
            print "Licence:", journal.licence

        next_tag = licence_tag.findNext('br').findNext('br').findNext('a')
        if next_tag.get('class', None) == 'page':
            next_tag = False

        return journal, next_tag

        

        
       
class CrossRefDepRecordParser():
    """Parses a single instance of quarterly CrossRef deposition records"""

    def __init__(self, quarter = None, test = False):
        self.quarter = quarter
        self.journal_list = []
        self.test = test

    def get_and_parse_dep_record(self):
        if not self.quarter:
            raise InputError

        response = self.get_record()
        parsed_response = self.parse_response(response)
        publishers = self.get_publishers(parsed_response)

        for publisher in publishers:
            journals = self.parse_journals(publisher)
            for journal in journals:
                self.journal_list.append(journal)

        

    def get_record(self):
        if self.test:
            response = open("Q311quarterly_deposits.html", 'r')
            return response
        query_url = "http://www.crossref.org/06members/%squarterly_deposits.html" % self.quarter
        print "Query:", query_url
        response = urllib2.urlopen(query_url)
        return response

    def parse_response(self, response):
        parsed_response = BeautifulSoup(response.read())
        return parsed_response

    def get_publishers(self, parsed_response):
        """Returns a list of the div elements containing journal list.

        The core element of each journal list for each publisher is a div containing the
        list of journals and the deposition numbers. The actual publisher name is in a <td>
        tag a few elements up in the heirachy.
        """
        
        publishers = parsed_response.findAll('div')
        #print len(publishers), publishers[1]
        return publishers

    def parse_journals(self, publisher):
        td_elements = publisher.findAll('td')
        num_journals = (len(td_elements) - 12)/6
        journals = []

        if num_journals > 0:
            for journal in range(1,num_journals+1):
                journals.append({'type' : str(td_elements[journal*6 + 1].string),
                                 'name' : str(td_elements[journal*6 + 2].string),
                                 'cy'   : int(td_elements[journal*6 + 3].string),
                                 'by'   : int(td_elements[journal*6 + 4].string),
                                 'ud'   : int(td_elements[journal*6 + 5].string)})

        return journals

    def write_journal_list(self, filename):

        with open(filename, 'w') as f:
            writer = csv.DictWriter(f, fieldnames = ['name', 'type', 'cy', 'by', 'ud'])
            writer.writeheader()
            for row in self.journal_list:
                writer.writerow(row)

    def get_publisher_name(self, publisher):
        pub_td_element = publisher.parent.parent.previous
        print pub_td_element
        name = pub_td_element.find('A')
        print name
        return name
        


        
