from oabiblio.journal_list import *
import csv
import jinja2
import oabiblio.html_reporting
import os

import oabiblio.logger
LOG = oabiblio.logger.log(__name__)

def ccby_numbers():
    """
    Generates aggregate numbers for cc-by.
    """
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
        quarter_csv_file = os.path.join("data", "%s.csv" % quarter)
        with open(quarter_csv_file, 'rU') as f:
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

        #print quarter, str(total_accumulator), str(plos_accumulator), str(ccbync_accumulator), str(ccbyncsa_accumulator)
        data.append({'quarter' : quarter,
                     'total_deposits' : total_accumulator,
                     'ccby_deposits'  : ccby_accumulator,
                     'ccbync_deposits' : ccbync_accumulator,
                     'ccbyncsa_deposits' : ccbyncsa_accumulator,
                     'plos' : plos_accumulator})
    return data

def ccby_numbers_csv(filename):
    data = ccby_numbers()
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, fieldnames = ['quarter', 'total_deposits', 'ccby_deposits',
            'ccbync_deposits', 'ccbyncsa_deposits', 'plos'])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def ccby_numbers_md(parent_dir):
    data = ccby_numbers()
    svg_filename = os.path.join(parent_dir, 'chart.svg')
    graph_svg(data, 'title of graph', svg_filename)
    return oabiblio.html_reporting.generate("ccby.md", {'data' : data })

def ccby_numbers_html(filename):
    parent_dir = os.path.dirname(filename)
    md = ccby_numbers_md(parent_dir)
    with open(filename, "wb") as f:
        f.write(oabiblio.html_reporting.convert_markdown(md))

import pygal
def graph_svg(data, title, filename):
    # rearrange the data
    quarters = [row['quarter'] for row in data]
    total_deposits = [row['total_deposits'] for row in data]
    ccby = [row['ccby_deposits'] for row in data]
    ccbync = [row['ccbync_deposits'] for row in data]
    ccbyncsa = [row['ccbyncsa_deposits'] for row in data]
    plos = [row['plos'] for row in data]

    # make the graph
    line_chart = pygal.StackedLine(fill=True)
    line_chart.title = title
    line_chart.x_labels = quarters
    line_chart.add('CCBY', ccby)
    line_chart.add('CCBYNC', ccbync)
    line_chart.add('CCBYNCSA', ccbyncsa)
    line_chart.add('PLOS', plos)
    return line_chart.render_to_file(filename)
