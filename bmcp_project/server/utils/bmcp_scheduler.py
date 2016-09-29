import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from log import Log
log = Log()


def scheduler_listener(event):
    """Custom listener for apscheduler
    Will write the details to log file in case apscheduler job succeeds or error occurs
    :param event: the event executed and related to the apscheduler job
    """
    if event.code == EVENT_JOB_ERROR:
        print('The job crashed :(')
        log.warn("The schedule job crashed because of %s" % repr(event.exception))
    else:
        print('The job executed :)')
        log.debug("The schedule job %s executed and return value is '%s'" % (event.job_id, event.retval))


class BMCPScheduler:
    """An helper class for apscheduler"""

    def __init__(self, app):
        self.app = app
        self.__apscheduler = None

        # NOT instantiate while in flask DEBUG mode or in the main thread
        # It's to avoid APScheduler being instantiated twice
        if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            self.__apscheduler = BackgroundScheduler()

            # add event listener to make logs for the every task
            self.__apscheduler.add_listener(scheduler_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
            log.info("APScheduler loaded")
            self.__apscheduler.start()

    def get_scheduler(self):
        return self.__apscheduler

    def add_interval(self, function, **interval):
        """Add an interval job to APScheduler and executed.
        Job will be executed in interval.
        :Example:
            scheduler.add_interval("get_node_info", minutes=10)
            # user_manager.get_user_by_id(context) will be called every 10 minutes
        """
        if self.__apscheduler:
            self.__apscheduler.add_job(function,
                                       trigger='interval',
                                       max_instances=1,
                                       **interval)
