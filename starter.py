import logging
import os
import threading
import time
import traceback

import psycopg2

from iconizer.iconizer_app_root import IconizerAppRoot
from manage import initialize_settings

initialize_settings()

from iconizer import Iconizer
from iconizer.iconizer_client import IconizerClient
from libtool.app_framework import AppConfig

__author__ = 'weijia'

log = logging.getLogger(__name__)

os.environ["POSTGRESQL_ROOT"] = "others/pgsql"
os.environ["UFS_DATABASE"] = "sqlite"


class UfsStarter(IconizerAppRoot):
    front_end_task = {"postgre_sql": ["scripts\\postgresql.bat"]}
    background_tasks = ({"web_server": ["manage.py", "runserver", "8110"]},
                        {"drop_tagger": ["manage.py", "drop_tagger"]},
                        {"git_pull_all": ["manage.py", "git_pull_all"]},
                        {"background_tasks": ["manage.py", "process_tasks"]},
                        # {"ipynb": ["manage.py", "shell_ipynb"]},
                        # {"ipynb": ["jupyter-notebook.exe", "--config=ipython_config.py"]},
                        # {"clipboard_monitor": ["manage.py", "clipboard_monitor_task"]},
                        # {"web_server": ["cherrypy_server.py", ]}),
                        # {"ipynb": ["jupyter-notebook.exe", "--config=ipython_config.py"]})
                        )
    app_root_folder_name = "server_for_django_15_and_below"
    # log_folder = "logs"
    cleanup_tasks = [{"stop_postgre_sql": ["scripts\\postgresql_stop.bat"]}]

    def sync_to_main_thread(self):
        # Define our connection string
        conn_string = "host='localhost' dbname='postgres' user='postgres' password=''"
        conn_string += " port='%d'" % 5432

        # print the connection string we will use to connect
        print "Connecting to database\n	->%s" % (conn_string)

        # Check if postgresql started correctly
        retry_cnt = 0
        while True:
            time.sleep(1)
            try:
                # get a connection, if a connect cannot be made an exception will be raised here
                conn = psycopg2.connect(conn_string)
                break
            except psycopg2.OperationalError:
                retry_cnt += 1
                print "retrying to connect postgresql server"
                if retry_cnt > 20:
                    print "postgresql start failed"
                    raise "Can not start database!!!"


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    UfsStarter().start_iconized_applications()
