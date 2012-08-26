from modargs import args
from oabiblio.updates import *
import oabiblio.reports
import oabiblio.logger
import sys
import os
from oabiblio import INSTALL_DIR

MOD = sys.modules[__name__]
PROG = 'oacensus'
DEFAULT_COMMAND = 'report'

def run():
    args.parse_and_run_command(sys.argv[1:], MOD, default_command=DEFAULT_COMMAND)

def update_command(
        pubmed=False, # whether to update from pubmed
        crossref=False, # whether to update from crossref
        doaj=False, # whether to update from doaj
        years="11,12" # comma separated list of years
        ):
    """
    Downloads the latest source data files from sources.
    """
    log = oabiblio.logger.log("update command")
    log.debug("running update command with parameters:")
    for k, v in locals().iteritems():
        log.debug("%s: '%s'" % (k, v))

    # Do any extra processing of praams.
    years = years.split(",")

    if pubmed:
        log.debug("updating pubmed...")
        update_pubmed(years)

    if crossref:
        log.debug("updating crossref...")
        update_crossref(years)

    if doaj:
        log.debug("updating doaj...")
        # TODO update doaj

def report_command(
    directory='oacensus-report', # Directory (relative to current working dir) in which report files will be written.
    fmt='all' # Format for report. Options are 'csv' or 'html'. The 'all' option generates all formats.
        ):
    """
    Generates reports.
    """
    log = oabiblio.logger.log("report command")
    log.debug("running report command with parameters:")
    for k, v in locals().iteritems():
        log.debug("%s: '%s'" % (k, v))

    if not os.path.exists(directory):
        log.debug("Creating directory '%s' for reports" % directory)
        os.makedirs(directory)

    def do_csv():
        csv_filename = os.path.join(directory, 'ccby.csv')
        oabiblio.reports.ccby_numbers_csv(csv_filename)

    def do_html():
        html_filename = os.path.join(directory, 'index.html')
        oabiblio.reports.ccby_numbers_html(html_filename)

    if fmt == 'csv':
        do_csv()
    elif fmt == 'html':
        do_html()
    elif fmt == 'all':
        do_csv()
        do_html()
    else:
        sys.stderr.write("Invalid report format '%s'" % fmt)
        sys.exit(1)

def help_command(on=False):
    args.help_command(PROG, MOD, DEFAULT_COMMAND, on)

def help_text(on=False):
    return args.help_text(PROG, MOD, DEFAULT_COMMAND, on)
