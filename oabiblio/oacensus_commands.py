from modargs import args
import sys

MOD = sys.modules[__name__]
PROG = 'oacensus'
DEFAULT_COMMAND = 'report'

def run():
    args.parse_and_run_command(sys.argv[1:], MOD, default_command=DEFAULT_COMMAND)

def update_command(
        foo='bar' # This is a command line argument
        ):
    """
    Downloads the latest source data files from sources.
    """
    print "this is the update command! foo is %s" % foo

def report_command():
    """
    Generates the report.
    """
    print "this is the report command!"

def help_command(on=False):
    args.help_command(PROG, MOD, DEFAULT_COMMAND, on)

def help_text(on=False):
    return args.help_text(PROG, MOD, DEFAULT_COMMAND, on)
