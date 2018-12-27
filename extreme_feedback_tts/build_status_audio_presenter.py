#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from .audio_downloader import AudioDownloader
from .audio_player import AudioPlayer
from .build_status_enum import BuildStatus
from .build_status_presenter import BuildStatusPresenter


class AudioPresenter( BuildStatusPresenter ):
    '''Presents builds status as audio output.'''

    def __init__( self, config ):
        self._config            = config
        self._is_first_update   = True
        self._all_ok_counter    = 0
        self._all_nok_counter   = 0
        self._player            = AudioPlayer()
        self._audio             = AudioDownloader( config.assets_dir(), config.tts_lang() )

        logging.debug( 'Audio presenter: Downloading audio files ...' )

        self._audio.download_users_names( config.users() )
        self._audio.download_builds_names( config.builds() )
        self._audio.download_messages( config.tts_messages() )

    def update( self, build_statuses ):
        logging.debug( 'Updating audio status ...' )

        self._player.clear_playlist()

        all_ok          = all( info.status() == BuildStatus.Success for info in build_statuses )
        all_unavailable = all( info.status() == BuildStatus.Unavailable for info in build_statuses )

        if all_ok:
            self._all_nok_counter = 0

            if self._is_first_update or self._all_ok_counter == 0:
                self._all_ok_counter = 1
                self._player.add_to_playlist( self._audio.filepath_of_status_all_ok() )
                # play status_all_ok
            elif self._all_ok_counter == 5:
                self._all_ok_counter = 1
                self._player.add_to_playlist( self._audio.filepath_of_status_all_ok_long_time() )
                # play status_all_ok_long_time
            else:
                self._all_ok_counter += 1
        elif all_unavailable:
            self._all_ok_counter = 0
            self._all_nok_counter = 0
            self._player.add_to_playlist( self._audio.filepath_of_status_all_unavailable() )
            # play status_all_unavailable
        else:
            self._all_nok_counter += 1
            if self._all_nok_counter == 5:
                self._player.add_to_playlist( self._audio.filepath_of_status_all_nok_long_time() )
                self._all_nok_counter = 0
                # play status_all_nok_long_time

            for info in build_statuses:
                self._process_build_status( info )

        self._is_first_update = False
        self._player.play_playlist()

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