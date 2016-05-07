import logging

from iconizer.django_in_iconizer.django_starter import DjangoStarter


class UfsStarterWithSqlite(DjangoStarter):
    django_main_script_name = "manage.py"

    def get_frontend_task_descriptor(self):
        return self.django_server.get_task_descriptor("runserver", ["8110"])

    def get_background_tasks(self):
        return [
            # self.django_server.get_task_descriptor("drop_tagger"),
            # self.django_server.get_task_descriptor("git_pull_all"),
        ]

    def get_cleanup_task_descriptors(self):
        return []


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    UfsStarterWithSqlite().start_iconized_applications()
