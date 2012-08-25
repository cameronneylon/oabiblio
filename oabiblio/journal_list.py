from BeautifulSoup import BeautifulSoup
from oabiblio.journal import Journal
from oabiblio.exceptions import InputError
import csv
import urllib2
import re

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
