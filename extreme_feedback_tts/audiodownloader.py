#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from gtts import gTTS
from pydub import AudioSegment


class AudioDownloader:
    '''Downloads audio texts in for of mp3 files, which will be used in particular situations.'''

    def __init__( self, out_dir, lang, replace_if_exists = False ):
        self._out_dir           = out_dir
        self._lang              = lang
        self._replace_if_exists = replace_if_exists


    def download_users_names( self, users ):
        base_path = os.path.join( self._out_dir, 'users' )
        os.makedirs( base_path, exist_ok = True )
        logging.debug( f'Creating user names audio files in {base_path}' )
        
        for user in users:
            user_name = user[ 'team_city_name' ].replace( ' ', '' )
            self._download_audio( user[ 'tts_name' ], base_path, user_name )
        
        logging.debug( 'Audio files of users created' )

    
    def download_builds_names( self, builds ):
        base_path = os.path.join( self._out_dir, 'builds' )
        os.makedirs( base_path, exist_ok = True )
        logging.debug( f'Creating build names audio files in {base_path}' )

        for build in builds:
            self._download_audio( build[ 'tts_name' ], base_path, build[ 'build_type_id' ] )
        
        logging.debug( 'Audio files of build names created' )


    def download_messages( self, messages ):
        base_path = os.path.join( self._out_dir, 'messages' )
        os.makedirs( base_path, exist_ok = True )
        logging.debug( f'Creating custom messages audio files in {base_path}' )

        for id, text in messages.items():
            self._download_audio( text, base_path, id )
        
        logging.debug( 'Audio files of custom messages created' )


    def _download_audio( self, text, path, file_name ):
        mp3 = os.path.join( path, f'{file_name}.mp3' )
        wav = os.path.join( path, f'{file_name}.wav' )

        if not self._replace_if_exists and os.path.isfile( wav ):
            cropped = '...' + os.sep + os.sep.join( wav.split( os.sep )[-4:] )
            logging.debug( f'Audio file already exists "{cropped}"' )
            return None

        # create and download mp3 TTS audio file
        tts = gTTS( text, lang = self._lang )
        tts.save( mp3 )

        # convert mp3 to wav
        audio = AudioSegment.from_mp3( mp3 )
        audio.export( wav, format = 'wav' )
        
        os.remove( mp3 )
