#!/usr/bin/env python
import os
import sys
from utdirect.utils import setup_extra

# If you use an 'extra' folder with svn externals, uncomment the following lines:
#CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
#setup_extra(os.path.join(CURRENT_DIR, 'extra'))

import settings

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    from django.core.management import execute_from_command_line

    try:  #This should never be on the python path.
        sys.path.remove(os.path.dirname(os.path.abspath(__file__)))
    except:
        pass
    execute_from_command_line(sys.argv)
