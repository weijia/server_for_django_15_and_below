import logging
import os
import threading
import time
from manage import initialize_settings

initialize_settings()

from iconizer import Iconizer
from iconizer.iconizer_client import IconizerClient
from libtool.app_framework import AppConfig

__author__ = 'weijia'

log = logging.getLogger(__name__)


os.environ["POSTGRESQL_ROOT"] = "others/pgsql"


def start_task_starter():
    time.sleep(10)
    c = IconizerClient()
    print "executing in remote!!!!!!"
    while True:
        time.sleep(1)
        try:
            # c.execute_in_remote({"clipboard_monitor": ["manage.py", "clipboard_monitor_task"]})
            # c.execute_in_remote({"postgre_sql": ["postgresql.bat"]})
            c.execute_in_remote({"web_server": ["manage.py", "runserver", "8110"]})
            c.execute_in_remote({"drop_tagger": ["manage.py", "drop_tagger"]})
            c.execute_in_remote({"git_pull_all": ["manage.py", "git_pull_all"]})
            # c.execute_in_remote({"ipynb": ["manage.py", "shell_ipynb"]})
			c.execute_in_remote({"ipynb": ["jupyter-notebook" "--config=ipython_config.py"]})
            break
        except:
            pass


def stop_postgr_sql():
    c = IconizerClient()
    # c.execute_in_remote({"clipboard_monitor": ["manage.py", "clipboard_monitor_task"]})
    c.execute_in_remote({"stop_postgre_sql": ["postgresql_stop.bat"]})


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

        # i.execute({"new_ext_svr": [find_callable_in_app_framework("new_ext_svr")]})
        # i.execute({"web_server": ["manage.py", "runserver", "8110"]})
        i.add_final_close_listener(stop_postgr_sql)
        i.execute({"postgre_sql": ["postgresql.bat"]})


    except (KeyboardInterrupt, SystemExit):
        raise
        # print "stopping database"


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
