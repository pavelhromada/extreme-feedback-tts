#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from .audio_downloader import AudioDownloader
from .audio_player import AudioPlayer
from .build_status_enum import BuildStatus
from .build_status_presenter import BuildStatusPresenter


class AudioPresenter( BuildStatusPresenter ):
    '''Presents builds status via audio output.'''

    def __init__( self, config ):
        self._config            = config
        self._is_first_update   = True
        self._all_ok_counter    = 0
        self._all_nok_counter   = 0
        self._player            = AudioPlayer()

        logging.debug( 'Audio presenter: Downloading audio files ...' )

        audio = AudioDownloader( config.assets_dir(), config.tts_lang() )
        audio.download_users_names( config.users() )
        audio.download_builds_names( config.builds() )
        audio.download_messages( config.tts_messages() )

    def update( self, build_statuses ):
        logging.debug( 'Updating audio status ...' )

        self._player.clear_playlist()

        all_ok          = all( info.status() == BuildStatus.Success for info in build_statuses )
        all_unavailable = all( info.status() == BuildStatus.Unavailable for info in build_statuses )

        if all_ok:
            if self._is_first_update:
                self._all_ok_counter = 1
                # play status_all_ok
            elif self._all_ok_counter == 0:
                self._all_ok_counter = 1
                # play status_all_ok
            elif self._all_ok_counter == 5:
                self._all_ok_counter = 1
                # play status_all_ok_long_time
            else:
                self._all_ok_counter += 1
        elif all_unavailable:
            self._all_ok_counter = 0
            # play status_all_unavailable
        else:
            self._all_nok_counter += 1
            if self._all_nok_counter == 5:
                pass # play status_all_nok_long_time

            for info in build_statuses:
                self._process_build_status( info )

        self._is_first_update = False
            
        # player = AudioPlayer()
        # player.play_all_from_path( self._config.assets_dir() )

    def _process_build_status( self, info ):
        if not info.status_has_changed():
            return

        if info.status() == BuildStatus.Success:
            pass # play build name + status_ok_again
        elif info.status() == BuildStatus.Failed:
            pass # play build name + status_nok + committer name + you_broke_build
        elif info.status() == BuildStatus.Running:
            pass # play build name + status_sunning + committer name + you_committed
        else:
            pass # play status_unavailable + build name