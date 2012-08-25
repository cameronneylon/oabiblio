from oabiblio.journal_list import *
import csv

def ccby_numbers():
    ccby = JournalList()
    ccby.load_from_csv('ccby_journals.csv')
    ccby_journal_names = [journal.name for journal in ccby.journal_list]

    ccbync = JournalList()
    ccbync.load_from_csv('ccbync_journals.csv')
    ccbync_journal_names = [journal.name for journal in ccbync.journal_list]

    ccbyncsa = JournalList()
    ccbyncsa.load_from_csv('ccbyncsa_journals.csv')
    ccbyncsa_journal_names = [journal.name for journal in ccbyncsa.journal_list]

    data = []

    for quarter in ['Q106', 'Q206', 'Q306', 'Q406',
                    'Q107', 'Q207', 'Q307', 'Q407',
                    'Q108', 'Q208', 'Q308', 'Q408',
                    'Q109', 'Q209',
                    'Q110', 'Q210', 'Q310', 'Q410',
                    'Q111', 'Q211', 'Q311', 'Q411',
                    'Q112', 'Q212']:

        dep_records = []
        with open((quarter+'.csv'), 'rU') as f:
            reader = csv.DictReader(f)
            for journal in reader:
                dep_records.append(journal)

        ccby_accumulator = 0
        ccbync_accumulator = 0
        ccbyncsa_accumulator = 0
        plos_accumulator = 0
        total_accumulator = 0

        for journal in dep_records:
            if journal['name'] in ccby_journal_names:
                # print journal['name'], journal['cy']
                ccby_accumulator += (int(journal['cy'])) # + int(journal['by']))

            if journal['name'] in ccbync_journal_names:
                # print journal['name'], journal['cy']
                ccbync_accumulator += (int(journal['cy'])) #+ int(journal['by']))

            if journal['name'] in ccbyncsa_journal_names:
                # print journal['name'], journal['cy']
                ccbyncsa_accumulator += (int(journal['cy'])) #+ int(journal['by']))

            if 'PLoS' in journal['name']:
                # print journal['name'], journal['cy']
                plos_accumulator += (int(journal['cy'])) #+ int(journal['by']))

            if journal['type'] == 'J':
                total_accumulator += (int(journal['cy'])) #+ int(journal['by']))

        print quarter, str(total_accumulator), str(plos_accumulator), str(ccbync_accumulator), str(ccbyncsa_accumulator)
        data.append({'quarter' : quarter,
                     'total_deposits' : total_accumulator,
                     'ccby_deposits'  : ccby_accumulator,
                     'ccbync_deposits' : ccbync_accumulator,
                     'ccbyncsa_deposits' : ccbyncsa_accumulator,
                     'plos' : plos_accumulator})

    with open('crossref_cydeps_by_license.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames = ['quarter', 'total_deposits', 'ccby_deposits',
                                                 'ccbync_deposits', 'ccbyncsa_deposits', 'plos'])
        writer.writeheader()
        for row in data:
            writer.writerow(row)
