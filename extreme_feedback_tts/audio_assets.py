#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from enum import Enum
from gtts import gTTS
from pydub import AudioSegment


class Message( Enum ):
    StatusAllUnavailable    = 1
    StatusAllOk             = 2
    StatusAllOkLongTime     = 3
    StatusAllNokLongTime    = 4
    StatusUnavailable       = 5
    StatusOkAgain           = 6
    StatusNok               = 7
    StatusRunning           = 8
    YouBrokeBuild           = 9
    YouCommitted            = 10

    @classmethod
    def from_string( cls, value ):
        if value == 'status_all_unavailable':
            return Message.StatusAllUnavailable
        elif value == 'status_all_ok':
            return Message.StatusAllOk
        elif value == 'status_all_ok_long_time':
            return Message.StatusAllOkLongTime
        elif value == 'status_all_nok_long_time':
            return Message.StatusAllNokLongTime
        elif value == 'status_unavailable':
            return Message.StatusUnavailable
        elif value == 'status_ok_again':
            return Message.StatusOkAgain
        elif value == 'status_nok':
            return Message.StatusNok
        elif value == 'status_running':
            return Message.StatusRunning
        elif value == 'you_broke_build':
            return Message.YouBrokeBuild
        elif value == 'you_committed':
            return Message.YouCommitted
        else:
            raise RuntimeWarning( 'Not valid audio message requested' )


class AudioAssets:
    '''Downloads audio texts in form of wav files, which will be used in particular situations.'''

    def __init__( self, out_dir, lang, replace_if_exists = False ):
        self._out_dir           = out_dir
        self._lang              = lang
        self._replace_if_exists = replace_if_exists
        self._user_names_audio  = {}
        self._builds_audio      = {}
        self._messages_audio    = {}

    def download_users_names( self, users ):
        base_path = os.path.join( self._out_dir, 'users' )
        os.makedirs( base_path, exist_ok = True )
        logging.debug( f'Creating user names audio files in {base_path}' )
        
        def replace_special_chars( old_string, to_replace_chars, new_string ):
            for c in to_replace_chars:
                old_string = old_string.replace( c, new_string )
            return  old_string
            
        for user in users:
            user_name = user[ 'team_city_name' ].replace( ' ', '' )
            name = replace_special_chars( user_name, '<>:"/\\|?*', '_' )
            path = self._download_audio( user[ 'tts_name' ], base_path, name )
            self._user_names_audio[ user[ 'team_city_name' ]] = path
        
        logging.debug( 'Audio files of users created' )
    
    def download_builds_names( self, builds ):
        base_path = os.path.join( self._out_dir, 'builds' )
        os.makedirs( base_path, exist_ok = True )
        logging.debug( f'Creating build names audio files in {base_path}' )

        for build in builds:
            path = self._download_audio( build[ 'tts_name' ], base_path, build[ 'build_type_id' ])
            self._builds_audio[ build[ 'build_type_id' ]] = path
        
        logging.debug( 'Audio files of build names created' )

    def download_messages( self, messages ):
        base_path = os.path.join( self._out_dir, 'messages' )
        os.makedirs( base_path, exist_ok = True )
        logging.debug( f'Creating custom messages audio files in {base_path}' )
        
        for id, text in messages.items():
            path = self._download_audio( text, base_path, id )
            self._messages_audio[ Message.from_string( id )] = path
        
        logging.debug( 'Audio files of custom messages created' )

    def user_path( self, user ):
        path = self._user_names_audio[ user ] if user in self._user_names_audio else None
        if not path:
            logging.warning( f'No audio for user {user}' )
        return path
        
    def build_path( self, build_id ):
        path = self._builds_audio[ build_id ] if build_id in self._builds_audio else None
        if not path:
            logging.warning( f'No audio for build name {build_id}' )
        return path

    def message_path( self, message ):
        path = self._messages_audio[ message ] if message in self._messages_audio else None
        if not path:
            logging.warning( f'No audio for message {message}' )
        return path

    def _download_audio( self, text, path, file_name ):
        '''Converts text via Google text-to-speech and saves it as wav file.
        Returns path to saved wav file.
        '''

        mp3 = os.path.join( path, f'{file_name}.mp3' )
        wav = os.path.join( path, f'{file_name}.wav' )

        if not self._replace_if_exists and os.path.isfile( wav ):
            cropped = '...' + os.sep + os.sep.join( wav.split( os.sep )[-4:] )
            logging.debug( f'Audio file already exists "{cropped}"' )
            return wav

        # create and download mp3 TTS audio file
        tts = gTTS( text, lang = self._lang )
        tts.save( mp3 )
   
        # convert mp3 to wav
        audio = AudioSegment.from_mp3( mp3 )
        audio.export( wav, format = 'wav' )
        os.remove( mp3 )
        
        return wav
