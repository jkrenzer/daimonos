
import configargparse 
import logging
import getpass

def _getLogLevel(userLevel):
    if isinstance(userLevel, int):
        numericLevel = userLevel
    else:
        numericLevel = getattr(logging, userLevel.upper(), None)
    if not isinstance(numericLevel, int):
        numericLevel = logging.INFO
    return numericLevel

def _getActionsByDest(argp):
    destDict = {}
    for action in argp._actions:
        destDict.update({action.dest: action})
    return destDict

def askMissingArgs(required, args, argp):
    missing = _getMissingArgs(required, args)
    actions = _getActionsByDest(argp)
    newArgs = []
    for arg in missing:
        if arg in actions.keys():
            action = actions[arg]
            val = input("Enter a value for {arg} ({help}) [{default}]:".format(arg=arg,help=action.help, default=action.default))
            newArgs.append("{} {}".format(action.option_strings[0], val))
    argp.parse_args(newArgs, namespace=args)

def _getMissingArgs(requiredArgs, namespace):
    missing = set()
    for arg in set(requiredArgs):
        val = getattr(namespace, arg, None)
        if val is None:
            missing.add(arg)
    return missing

def main():
    
    # Set program informations
    prog = "daimonos"
    description = "Daimonos is an extensible XMPP-Bot written in Python3."
    epilog = ""
    
    # Instanciating a config- and argument-parser
    argp = configargparse.ArgParser(default_config_files=['/etc/daimonos.conf', '~/.daimonos.conf'],prog=prog,description=description,epilog=epilog)
    
    # Setup the commandline and config-file arguments
    argp.add('-c', '--config', is_config_file=True, help='Configuration file')

    # Options governing the daemon and locking
    argp.add('-s', '--singleQuery', help='Execute single Query and then exit. The query must be given as would be in a message to the bot.',
                    dest='singleQuery')
    argp.add('-f', '--lockFileName', help='set name of lock-file which is used by deamon',
                    dest='lockFileName', default='daimonos.lock')
    argp.add('-F', '--lockFilePath', help='set path of lock-file which is used by deamon',
                    dest='lockFilePath', default='/var/lock/')

    # Logging options.
    argp.add('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    argp.add('-l', '--logFile', help='set a filepath to log to. Filelogging is deactivated if empty.',
                     dest="logFile", default=None)
    argp.add('-d', '--logLevel', help='set the loglevel of the logfile',
                    dest='logLevel', default=logging.INFO)
    argp.add('-v', '--verbosity', help='set the loglevel of the console',
                    dest='verbosity', default=logging.INFO)

    # JID and password options.
    argp.add("-j", "--jid", dest="jid", help="JID to use")
    argp.add("-p", "--password", dest="password", help="password to use")
    
    # Parsing commandline
    args = argp.parse_args()
    
    import pprint as pp
    
    pp.pprint(argp.__dict__)
    pp.pprint(args)
    
    # Comparing given and required arguments
    neededArgs = ('jid', 'password')
    missingArgs = _getMissingArgs(neededArgs, args)

    # Setup logging.
    logger = logging.getLogger(__name__)
    logger.setLevel(-1)
    
    # Create and add handlers
    
    logStdErrHandler = logging.StreamHandler()
    logStdErrHandler.setFormatter(logging.Formatter('%(levelname)s:%(name)s: %(message)s'))
    logStdErrHandler.setLevel(_getLogLevel(args.verbosity))
    logger.addHandler(logStdErrHandler)
    
    if args.logFile is not None:    
        logFileHandler = logging.FileHandler(args.logFile)
        logFileHandler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logFileHandler.setLevel(_getLogLevel(args.logLevel))
        logger.addHandler(logFileHandler)
    
    # Start logging
        logger.debug('Logging configured. There are %s handlers configured.' % len(logger.handlers))
    # Log configuration options
    for line in argp.format_values().split('\n'):
        logger.debug(line)
    
    if len(missingArgs) > 0: 
        logger.debug('There are %s required arguments missing: %s' % (len(missingArgs)," ".join(missingArgs)))
    
    # Ask needed values if not given
    askMissingArgs(neededArgs, args, argp)
    logger.debug('# Begin Config Values ')
    for key, val in args.__dict__.items():
        logger.debug("{}: {}".format(key, val))
    logger.debug('# End Config Values')

#TODO do something with our values
