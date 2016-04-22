import logging
import os
import threading
import time
import traceback
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
    front_end_task = {"postgre_sql": ["postgresql.bat"]}
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
    django_server_folder = "server_for_django_15_and_below"
    log_folder = "logs"
    cleanup_tasks = [{"stop_postgre_sql": ["postgresql_stop.bat"]}]

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
        time.sleep(10)
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


class UfsStarterWithSqlite(UfsStarter):
    front_end_task = {"web_server": ["manage.py", "runserver", "8110"]}
    background_tasks = ({"drop_tagger": ["manage.py", "drop_tagger"]},
                        {"git_pull_all": ["manage.py", "git_pull_all"]},
                        {"background_tasks": ["manage.py", "process_tasks"]},
                        )
    cleanup_tasks = []


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    UfsStarter().start_ufs_sys()
