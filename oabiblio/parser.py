from BeautifulSoup import BeautifulSoup
from oabiblio.exceptions import InputError
import csv
import urllib2

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


class PubMedParser():
    """Fetches the number of articles for a given journal for a given year from PubMed"""

    def __init__(self, journal_file, years):
        self.journal_file = journal_file
        self.years = years
        self.data = []

    def fetch_all_data(self):
        """Reads the infile and fetches article count for each article contained therein"""

        with open(self.journal_file, 'rU') as jf:
            reader = csv.DictReader(jf)

            for row in reader:
                datum = {'name': row['name']}
                for year in self.years:
                    #Convert two-digit years to four-digit years
                    if year.__len__() == 2:
                        year = "20" + year

                    year_header = "Year-" + year
                    datum[year_header] = self.fetch_journal_data(row['issn'], year)

    def fetch_journal_data(self, issn, year):
        """Fetches the number of articles for a specific journal and year"""
        fixed_issn = issn[:4] + "-" + issn[:-4]
        query = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%(issn)s[Journal]+AND+%(year)s[pdat]" % {'issn' : fixed_issn, 'year': year}
        print query

    def write_file(self, filename=None):
        """Takes our populated data and writes it to a csv file"""

        # If an output filename isn't supplied, create one from the infile name
        if filename is None:
            filename = self.journal_file.split(".")[0] + "_article_counts.csv"

