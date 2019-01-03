#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json


class Configuration:
    '''Loads the JSON configuration for application.'''

    def __init__( self, file_path ):
        data = self._load_config_file( file_path )

        filename, _ = os.path.splitext( os.path.basename( file_path ))
        assets = os.path.dirname( os.path.abspath( __file__ ))
        assets = os.path.join( assets, '..', 'assets', filename )

        self._assets_dir        = os.path.normpath( assets )
        self._users             = data[ 'users'            ]
        self._tts_messages      = data[ 'tts_messages'     ]
        self._builds            = data[ 'builds'           ]
        self._tts_lang          = data[ 'tts_lang'         ]
        self._build_server_url  = data[ 'build_server_url' ]

    def assets_dir( self ):
        return self._assets_dir

    def users( self ):
        return self._users

    def tts_messages( self ):
        return self._tts_messages

    def builds( self ):
        return self._builds

    def tts_lang( self ):
        return self._tts_lang

    def build_server_url( self ):
        return self._build_server_url

    def _load_config_file( self, file_path ):
            with open( file_path, encoding = 'utf-8' ) as json_file:
                return json.load( json_file )