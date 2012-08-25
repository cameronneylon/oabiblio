from modargs import args
from oabiblio.updates import *
import oabiblio.reports
import sys

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
    # Do any extra processing of praams.
    years = years.split(",")

    if pubmed:
        print "Running pubmed"
        update_pubmed()

    if crossref:
        # TODO update crossref
        update_crossref(years)

    if doaj:
        # TODO update doaj
        pass

    print "updating is complete!"

def report_command():
    """
    Generates the report.
    """
    print oabiblio.reports.ccby_numbers_html()

def help_command(on=False):
    args.help_command(PROG, MOD, DEFAULT_COMMAND, on)

def help_text(on=False):
    return args.help_text(PROG, MOD, DEFAULT_COMMAND, on)
