import logging
import os
import threading
import time
import sys
from manage import initialize_settings

initialize_settings()

from iconizer import Iconizer
from iconizer.iconizer_client import IconizerClient
from libtool.app_framework import AppConfig

__author__ = 'weijia'

log = logging.getLogger(__name__)


def start_task_starter():
    time.sleep(10)
    c = IconizerClient()
    print "executing in remote!!!!!!"
    while True:
        time.sleep(1)
        try:
            c.execute_in_remote({"task_starter": ["manage.py", "clipboard_monitor_task"]})
            break
        except:
            pass


def main():
    try:
        app = AppConfig(os.path.realpath(__file__), "server_for_django_15_and_below")
        log_folder = app.get_or_create_app_data_folder("logs")
        threading.Thread(target=start_task_starter).start()
        i = Iconizer(log_folder)
        # i.start_name_server()
        # i.add_close_listener(stop_services_and_web_servers)
        # i.add_final_close_listener(stop_postgresql)
        # i.get_gui_launch_manager().taskbar_icon_app["Open Main Page"] = open_main
        # add_path_to_python_path_env(root_path)

        # i.execute({"new_ext_svr": [find_callable_in_app_framework("new_ext_svr")]})
        i.execute({"web_server": ["manage.py", "runserver", "8110"]})

    except (KeyboardInterrupt, SystemExit):
        raise
        # print "stopping database"


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
