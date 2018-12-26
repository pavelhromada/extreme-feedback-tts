#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import logging
from extreme_feedback_tts import ExtremeFeedbackApp

def parse_arguments():
    ap = argparse.ArgumentParser()

    ap.add_argument( '-c', '--config',
                     required = True,
                     help = 'path to config file JSON' )
    ap.add_argument( '-g', '--gui',
                     required = False,
                     help = 'show also GUI',
                     action = 'store_true',
                     default = False )
    ap.add_argument( '-f', '--fullscreen',
                     required = False,
                     help = 'show GUI in fullscreen mode (if GUI is requested)',
                     action = 'store_true',
                     default = False )
    
    return vars( ap.parse_args() )


def configure_logging():
    # logging.basicConfig( level = logging.DEBUG )
    # logging.basicConfig( format = '%(message)s' )
    pass


if __name__ == "__main__":
    configure_logging()
    args = parse_arguments()

    if not args[ 'config' ]:
        logging.warning( 'Config JSON file not provided. Exit.' )
        exit( 1 )

    app = ExtremeFeedbackApp( args[ 'config' ],
                              args[ 'gui' ],
                              args[ 'fullscreen' ])
    app.run()
