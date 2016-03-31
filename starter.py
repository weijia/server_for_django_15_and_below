import logging
import os
import threading
import time
import traceback

import psycopg2

from manage import initialize_settings

initialize_settings()

from iconizer import Iconizer
from iconizer.iconizer_client import IconizerClient
from libtool.app_framework import AppConfig

__author__ = 'weijia'

log = logging.getLogger(__name__)

os.environ["POSTGRESQL_ROOT"] = "others/pgsql"
os.environ["UFS_DATABASE"] = "sqlite"


class UfsStarter(object):
    front_end_task = {"postgre_sql": ["scripts\\postgresql.bat"]}
    background_tasks = ({"web_server": ["manage.py", "runserver", "8110"]},
                        {"drop_tagger": ["manage.py", "drop_tagger"]},
                        {"git_pull_all": ["manage.py", "git_pull_all"]},
                        # {"ipynb": ["manage.py", "shell_ipynb"]},
                        # {"ipynb": ["jupyter-notebook.exe", "--config=ipython_config.py"]},
                        # {"clipboard_monitor": ["manage.py", "clipboard_monitor_task"]},
                        # {"web_server": ["cherrypy_server.py", ]}),
                        # {"ipynb": ["jupyter-notebook.exe", "--config=ipython_config.py"]})
                        )
    django_server_folder = "server_for_django_15_and_below"
    log_folder = "logs"
    cleanup_tasks = [{"stop_postgre_sql": ["scripts\\postgresql_stop.bat"]}]

    def __init__(self):
        super(UfsStarter, self).__init__()
        self.app = AppConfig(os.path.realpath(__file__), self.django_server_folder)
        self.log_folder = self.app.get_or_create_app_data_folder(self.log_folder)
        self.iconizer = Iconizer(self.log_folder)
        self.client = IconizerClient()

    def start_ufs_sys(self):
        try:
            threading.Thread(target=self.start_task_starter).start()
            # i.start_name_server()
            # i.add_close_listener(stop_services_and_web_servers)
            # i.add_final_close_listener(stop_postgresql)
            # i.get_gui_launch_manager().taskbar_icon_app["Open Main Page"] = open_main

            # i.execute({"new_ext_svr": [find_callable_in_app_framework("new_ext_svr")]})
            self.iconizer.add_final_close_listener(self.final_cleanup)
            self.iconizer.execute(self.front_end_task)

        except (KeyboardInterrupt, SystemExit):
            raise
            # print "stopping database"

    def start_task_starter(self):
        self.wait_for_database()
        print "executing in remote!!!!!!"
        try:
            self.execute_tasks(self.background_tasks)
        except:
            traceback.print_exc()
            pass

    def execute_tasks(self, tasks):
        for task in tasks:
            self.client.execute_in_remote(task)

    def final_cleanup(self):
        self.execute_tasks(self.cleanup_tasks)

    # noinspection PyMethodMayBeStatic
    def wait_for_database(self):
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


class UfsStarterWithSqlite(UfsStarter):
    front_end_task = {"web_server": ["manage.py", "runserver", "8110"]}
    background_tasks = ({"drop_tagger": ["manage.py", "drop_tagger"]},
                        {"git_pull_all": ["manage.py", "git_pull_all"]},
                        # {"ipynb": ["manage.py", "shell_ipynb"]},
                        # {"ipynb": ["jupyter-notebook.exe", "--config=ipython_config.py"]},
                        # {"clipboard_monitor": ["manage.py", "clipboard_monitor_task"]},
                        # {"web_server": ["cherrypy_server.py", ]}),
                        # {"ipynb": ["jupyter-notebook.exe", "--config=ipython_config.py"]})
                        )
    cleanup_tasks = []

    def wait_for_database(self):
        return


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    UfsStarter().start_ufs_sys()
