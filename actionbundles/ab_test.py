from util.toolkit import log, calc_working_seconds
from actionbundles.action_bundle import ActionBundle
import datetime
import ipdb


class ABTest(ActionBundle):
    '''
    classdocs.
    '''

    def __init__(self, parser):
        '''
        Constructor
        '''
        self.parser = parser

        log.info(self.__class__.__name__ + " initialized")

        try:
            st = parser.options.string

            now = datetime.datetime.now()
            then = now + datetime.timedelta(2, 60)

            difference = calc_working_seconds(now, then)

            # print(datetime.timedelta(seconds=difference))

            log.critical(difference)

            # ipdb.set_trace()

        except:
            raise
