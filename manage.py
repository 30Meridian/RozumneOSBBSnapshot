#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "system.settings")

    basedir = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(os.path.join(basedir, "modules"))
    sys.path.append(os.path.join(basedir, "applications"))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)