from modargs import args
import sys

from oabiblio.updates import *

MOD = sys.modules[__name__]
PROG = 'oacensus'
DEFAULT_COMMAND = 'report'

def run():
    args.parse_and_run_command(sys.argv[1:], MOD, default_command=DEFAULT_COMMAND)

def update_command(
        years="11,12" # comma separated list of years
        ):
    """
    Downloads the latest source data files from sources.
    """
    years = years.split(",")
    crossref(years)

def report_command():
    """
    Generates the report.
    """
    print "this is the report command!"

def help_command(on=False):
    args.help_command(PROG, MOD, DEFAULT_COMMAND, on)

def help_text(on=False):
    return args.help_text(PROG, MOD, DEFAULT_COMMAND, on)
