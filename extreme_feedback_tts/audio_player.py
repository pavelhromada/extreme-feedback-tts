#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import logging
import simpleaudio as sa


class AudioPlayer:
    '''Plays mp3 audio content.'''

    def __init__( self ):
        self._playlist = []

    def clear_playlist( self ):
        self._playlist.clear()

    def add_to_playlist( self, audio_paths ):
        self._playlist.append( audio_paths )

    def play_playlist( self ):
        for item in self._playlist:
            if item.__class__.__name__ in ( 'list', 'tuple' ):
                for sub_item in item:
                    self._play( sub_item )
                    time.sleep( 0.15 ) # 150ms pause between sub-items
            else:
                self._play( item )

            time.sleep( 1 ) # 1s pause between items

    def play_all_from_path( self, path ):
        for dirpath, _, files in os.walk( path ):
            for filename in [f for f in files if f.endswith( '.wav' )]:
                self._play( os.path.join( dirpath, filename ))
                logging.debug( f'Playback of {filename} stopped' )

    def _play( self, audio_file_path ):
        wave_obj = sa.WaveObject.from_wave_file( audio_file_path )
        play_obj = wave_obj.play()
        play_obj.wait_done()
