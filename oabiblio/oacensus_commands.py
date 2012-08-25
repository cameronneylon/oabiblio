from modargs import args
import sys

from oabiblio.updates import *

MOD = sys.modules[__name__]
PROG = 'oacensus'
DEFAULT_COMMAND = 'report'

def run():
    args.parse_and_run_command(sys.argv[1:], MOD, default_command=DEFAULT_COMMAND)

def update_command(
        pubmed=True, # whether to update from pubmed
        crossref=True, # whether to update from crossref
        doaj=True, # whether to update from doaj
        years="11,12" # comma separated list of years
        ):
    """
    Downloads the latest source data files from sources.
    """
    # Do any extra processing of praams.
    years = years.split(",")

    if pubmed:
        # TODO update pubmed

    if crossref:
        # TODO update crossref
        crossref(years)

    if doaj:
        # TODO update doaj

    print "updating is complete!"

def report_command():
    """
    Generates the report.
    """
    print "this is the report command!"

def help_command(on=False):
    args.help_command(PROG, MOD, DEFAULT_COMMAND, on)

def help_text(on=False):
    return args.help_text(PROG, MOD, DEFAULT_COMMAND, on)
