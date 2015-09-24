#! /usr/bin/env python
import sys

import util.OptParser as parser
from util.Toolkit import log, generateGUID, abPathToClass, abSubclassPathFromAction

try:

    # Print execution command
    log.debug("Executed command '" + " ".join(sys.argv) + "'")

    # Generate a unique execution id
    guid = generateGUID()
    log.info("Unique PyJi execution ID generated: '" + guid + "'")

    # Instantiate specified ActionBundle class (from string)
    ab = abPathToClass(abSubclassPathFromAction(parser.action), parser)

except (Exception, KeyboardInterrupt):
    log.error(str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]))
    raise



# Salute!
log.info("Bye bye! :-)")