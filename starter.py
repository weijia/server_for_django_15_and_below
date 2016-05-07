import logging
import os

from iconizer.django_in_iconizer.django_starter import DjangoStarter
from iconizer.django_in_iconizer.postgresql_checker import PostgreSqlChecker
from manage import initialize_settings

initialize_settings()

__author__ = 'weijia'


os.environ["POSTGRESQL_ROOT"] = "others/pgsql"
os.environ["UFS_DATABASE"] = "sqlite"


class UfsStarter(DjangoStarter):
    def get_background_tasks(self):
        return (
            # {"web_server": ["manage_with_conf.py", "runserver", "8110"]},
            self.django_server.get_task_descriptor("runserver", ["8110"]),
            # django_server.get_django_task("drop_tagger"),
            # django_server.get_django_task("process_tasks"),
            # django_server.get_django_task("shell_ipynb"),
            # django_server.get_django_task("clipboard_monitor_task"),
            # {"web_server": ["cherrypy_server.py", ]}),
            # {"ipython_notebook": ["jupyter-notebook.exe", "--config=ipython_config.py"]})
        )


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    UfsStarter().start_iconized_applications()
