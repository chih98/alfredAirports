# -*- coding: utf-8 -*-

import sys

from workflow import Workflow3
from workflow.background import is_running, run_in_background

import os


def string_from_count(c):
    """Returns a fancy string to show in the workflow from the count item"""

    blue = "\\U0001F535\\U0000FE0F"
    white = "\\U000026AA\\U0000FE0F"
    black = "\\U000026AB\\U0000FE0F"

    ret = black + black + black + black + black + white + black + black + black + black + black

    mod = 2 * (5 - (c % 5))

    return ret.decode('unicode_escape')[mod:][0:10]


def main(wf):
    # Check if first time
    try:
        count = int(os.environ['count'])
        first_time = False
    except:
        count = 0
        first_time = True

    if first_time:

        wf.rerun = 0.5
        wf.store_data('download_percent', '0%')
        wf.add_item('Starting background process')
        # run_in_background('bg', ['/usr/bin/python', wf.workflowfile('src/bg_downloader.py'),
        #                          'http://ourairports.com/data/airports.csv'])
        run_in_background('bg', ['/usr/bin/python', wf.workflowfile('src/bg_downloader.py')])

    else:

        if is_running('bg'):
            """Update status"""
            pct = wf.stored_data('download_percent')
            progress = wf.stored_data('download_progress')
            file = wf.stored_data('download_file')

            wf.rerun = 0.5

            title = "Downloading {} [{}]".format(file,progress)
            subtitle = string_from_count(count) + " " + pct
            wf.add_item(title,subtitle=subtitle)

            count += 1
        else:
            """Last case"""
            wf.add_item("File download complete",  icon="images/Checkmark.png")

    wf.setvar('count', count)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))