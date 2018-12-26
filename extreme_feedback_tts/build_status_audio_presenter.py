#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from .build_status_presenter import BuildStatusPresenter
from .audiodownloader import AudioDownloader
from .audioplayer import AudioPlayer


class AudioPresenter( BuildStatusPresenter ):
    '''Presents builds status via audio output.'''

    def __init__( self, config ):
        self._config = config

        logging.debug( 'Audio presenter: Downloading audio files ...' )

        audio = AudioDownloader( config.assets_dir(), config.tts_lang() )
        audio.download_users_names( config.users() )
        audio.download_builds_names( config.builds() )
        audio.download_messages( config.tts_messages() )

    def update( self, build_statuses ):
        logging.debug( 'Updating audio status ...' )

        # player = AudioPlayer()
        # player.play_all_from_path( self._config.assets_dir() )

        # TODO implement audio composition logic