import logging
import os
import threading
import time
import sys
from manage import initialize_settings

initialize_settings()
log = logging.getLogger(__name__)
from iconizer import Iconizer
from iconizer.iconizer_client import IconizerClient

__author__ = 'weijia'


def start_task_starter():
    time.sleep(10)
    c = IconizerClient()
    print "executing in remote!!!!!!"
    c.execute_in_remote({"task_starter": ["manage.py", "clipboard_monitor_task"]})


def main():

    i = Iconizer()
    threading.Thread(target=start_task_starter).start()
    i.execute({"django_server": ["manage.py", "runserver", "8088"]})
    # Iconizer().execute({"test_app_id_for_later_killing": ["manage.py", "clipboard_monitor_task"]})
    # Iconizer().execute({"test_app_id_for_later_killing": ["manage.py", "process_tasks"]})
    # Iconizer().execute({"test_app_id_for_later_killing": ["manage.py", "syncdb"]})
    # threading.Thread.

    # i.execute({"task_starter": ["manage.py", "start_task"]})

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
