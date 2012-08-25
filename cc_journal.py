from oabiblio import *

cc_journals = JournalsWithCCLicence()
cc_journals.populate()
cc_journals.write_journal_list("cc_journals.csv")

ccby_journals = cc_journals.filter_by_licence("http://creativecommons.org/licenses/by/3.0/legalcode")

ccby_jlist = JournalList(ccby_journals)
for journal in ccby_jlist.journal_list:
    print journal, journal.licence

ccby_jlist.write_journal_list("ccby_journals.csv")

ccbync_journals = JournalList(cc_journals.filter_by_licence("http://creativecommons.org/licenses/by-nc/3.0/legalcode"))
ccbync_journals.write_journal_list("ccbync_journals.csv")

ccbyncsa_journals = JournalList(cc_journals.filter_by_licence("http://creativecommons.org/licenses/by-nc-sa/3.0/legalcode"))
ccbyncsa_journals.write_journal_list("ccbyncsa_journals.csv")
