#!/usr/bin/env python3

import sys
import argparse
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


if __name__ == "__main__":
    args = parse_arguments()
    if not args[ 'config' ]:
        print( 'Config JSON file not provided. Exit.' )
        exit( 1 )

    app = ExtremeFeedbackApp( args[ 'config' ],
                              args[ 'gui' ],
                              args[ 'fullscreen' ])
    app.run()
