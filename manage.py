#!/usr/bin/env python
import logging
import os
import sys
import re


my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(my_path, "server_base_packages/libtool"))
from libtool import include_all, include_file_sibling_folder
from libtool import get_folder
include_all(__file__, "server_base_packages")
include_all(__file__, "external_apps")
include_file_sibling_folder(__file__, "local")
#include_file_sibling_folder(__file__, "extra_settings/keys")
#include_file_sibling_folder(__file__, "server_base_packages/django-bootstrap3/demo/")
from djangoautoconf.auto_conf_signals import ServerSignalTrigger


def initialize_settings():
    from djangoautoconf import DjangoAutoConf
    #Added keys folder to path so DjangoAutoConf can find keys in it
    c = DjangoAutoConf()
    c.set_default_settings("default_django_15_and_below.settings")
    root_folder = get_folder(__file__)
    c.set_root_dir(root_folder)
    c.set_local_key_folder(os.path.join(root_folder, "local/local_keys"))
    local_setting_dir = os.path.join(root_folder, "local/local_settings")
    c.add_extra_settings_from_folder(local_setting_dir)
    c.configure()

    """
    server_signal_handler_dir = os.path.join(root_folder, "extra_settings/server_signal_handlers")
    for module_name in c.enum_modules(server_signal_handler_dir):
        __import__("extra_settings.server_signal_handlers.%s" % module_name)
    """

if __name__ == "__main__":
    #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "default_django_15_and_below.settings")
    #logging.basicConfig(level=logging.DEBUG)

    initialize_settings()
    from django.core.management import execute_from_command_line
    #Need to put the import here after Django settings are configured
    #import django_cron
    #django_cron.start_cron_when_run_server()
    trigger = ServerSignalTrigger()
    trigger.trigger_server_start_if_needed()
    execute_from_command_line(sys.argv)
    trigger.trigger_server_stop_if_needed()
    #print "execute return"
    #django_cron.stop()
    #print "Process exiting"
