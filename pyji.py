#! /usr/bin/env python
import sys

import util.opt_parser as parser
from util.toolkit import log, generate_guid, ab_path_to_class, ab_subclass_path_from_action, start_busy_indicator, \
    stop_busy_indicator

bi = None

try:

    # Begin the Busy indicator
    bi = start_busy_indicator("")

    # Print execution command
    log.debug("Executed command '" + " ".join(sys.argv) + "'")

    # Generate a unique execution id
    guid = generate_guid()
    log.info("Unique PyJi execution ID generated: '" + guid + "'")

    # Instantiate specified ActionBundle class (from string)
    ab = ab_path_to_class(ab_subclass_path_from_action(parser.action), parser)

except (Exception, KeyboardInterrupt):
    # Show error
    log.error(str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]))
    raise

finally:
    # End the busy indicator
    stop_busy_indicator(bi)

    # Salute!
    log.info("Bye bye! :-)")
