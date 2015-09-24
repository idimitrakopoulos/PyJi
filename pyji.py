#! /usr/bin/env python
import sys
import logging, logging.config
from util.Toolkit import scriptGlobals, generateGUID
from util.ColorFormatter import ColorFormatter
from jira import JIRA

try:

    # Initialize loggers
    logging.ColorFormatter = ColorFormatter
    logging.config.fileConfig(scriptGlobals.logProperties)
    log = logging.getLogger(scriptGlobals.defaultLogger)

    # Generate a unique execution id
    guid = generateGUID()
    log.info("Unique PyJi Execution ID generated: '" + guid + "'")



except (Exception, KeyboardInterrupt):
    log.error(str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]))
    raise



# Salute!
log.info("Bye bye! :-)")