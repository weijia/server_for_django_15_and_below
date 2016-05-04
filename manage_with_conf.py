#!/usr/bin/env python
import sys

from ufs_tools.libtool import include_all_direct_sub_folders_in_sibling


def initialize_settings():
    include_all_direct_sub_folders_in_sibling(__file__, "server_base_packages")
    from djangoautoconf.django_dev_server_auto_conf import DjangoDevServerAutoConf
    c = DjangoDevServerAutoConf()
    c.configure("local/local_postgresql_settings")


if __name__ == "__main__":
    initialize_settings()

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
