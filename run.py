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
    ap.add_argument( '-d', '--debug',
                     required = False,
                     help = 'enable debug logs',
                     action = 'store_true',
                     default = False )
    
    return vars( ap.parse_args() )

def configure_logging( enable_logs ):
    if enable_logs:
        logging.basicConfig( level = logging.DEBUG )
    else:
        logging.disable( sys.maxsize )


if __name__ == "__main__":
    args = parse_arguments()
    configure_logging( args[ 'debug' ])

    try:
        app = ExtremeFeedbackApp( args[ 'config' ],
                                  args[ 'gui' ],
                                  args[ 'fullscreen' ])
        app.run()
    except Exception:
        logging.exception( 'Application exited prematurely' )
