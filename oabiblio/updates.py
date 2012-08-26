from oabiblio.journal_list import *
from oabiblio.parser import *

import oabiblio.logger
LOG = oabiblio.logger.log(__name__)

def update_crossref(years=['12']):
    quarters=['Q1', 'Q2', 'Q3', 'Q4']
    for year in years:
        for quarter in quarters:
            LOG.debug("updating crossref for %s of %s" % (quarter, year))
            crossrefrecord = CrossRefDepRecordParser(quarter+year)
            crossrefrecord.get_and_parse_dep_record()
            crossrefrecord.write_journal_list(quarter+year+'.csv')

def update_pubmed(years=['12']):
    parser = PubMedParser("ccby_journals.csv", years)
    parser.fetch_all_data()

def cc_journal():
    cc_journals = JournalsWithCCLicence()
    cc_journals.populate()
    cc_journals.write_journal_list("cc_journals.csv")

    ccby_journals = cc_journals.filter_by_licence("http://creativecommons.org/licenses/by/3.0/legalcode")

    ccby_jlist = JournalList(ccby_journals)

    for journal in ccby_jlist.journal_list:
        LOG.debug("%s, %s" % (journal, journal.licence))

    ccby_jlist.write_journal_list("ccby_journals.csv")

    ccbync_journals = JournalList(cc_journals.filter_by_licence("http://creativecommons.org/licenses/by-nc/3.0/legalcode"))
    ccbync_journals.write_journal_list("ccbync_journals.csv")

    ccbyncsa_journals = JournalList(cc_journals.filter_by_licence("http://creativecommons.org/licenses/by-nc-sa/3.0/legalcode"))
    ccbyncsa_journals.write_journal_list("ccbyncsa_journals.csv")
