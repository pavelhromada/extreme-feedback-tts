#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from .audio_assets import AudioAssets, Message
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
        self._assets            = AudioAssets( config.assets_dir(), config.tts_lang() )

        logging.debug( 'Audio presenter: Downloading audio files ...' )

        self._assets.download_users_names( config.users() )
        self._assets.download_builds_names( config.builds() )
        self._assets.download_messages( config.tts_messages() )

    def update( self, build_statuses ):
        logging.debug( 'Updating audio status ...' )

        self._player.clear_playlist()

        all_ok          = all( info.status() == BuildStatus.Success for info in build_statuses )
        all_unavailable = all( info.status() == BuildStatus.Unavailable for info in build_statuses )

        if all_ok:
            self._all_nok_counter = 0

            if self._is_first_update or self._all_ok_counter == 0:
                self._all_ok_counter = 1
                message = self._assets.message_path( Message.StatusAllOk )
                self._player.add_to_playlist( message )
            elif self._all_ok_counter == 5:
                self._all_ok_counter = 1
                message = self._assets.message_path( Message.StatusAllOkLongTime )
                self._player.add_to_playlist( message )
            else:
                self._all_ok_counter += 1
        elif all_unavailable:
            self._all_ok_counter = 0
            self._all_nok_counter = 0
            message = self._assets.message_path( Message.StatusAllUnavailable )
            self._player.add_to_playlist( message )
        else:
            self._all_nok_counter += 1
            if self._all_nok_counter == 5:
                message = self._assets.message_path( Message.StatusAllNokLongTime )
                self._player.add_to_playlist( message )
                self._all_nok_counter = 0

            for info in build_statuses:
                self._process_build_status( info )

        self._is_first_update = False
        self._player.play_playlist()

    def _process_build_status( self, info ):
        if not info.status_has_changed():
            return

        build_name_path = self._assets.build_path( info.build_id() )
        items = []

        if info.status() == BuildStatus.Success:
            items = [ 
                build_name_path,
                self._assets.message_path( Message.StatusOkAgain )
            ]
        elif info.status() == BuildStatus.Failed:
            items = [
                build_name_path,
                self._assets.message_path( Message.StatusNok ),
                self._assets.user_path( info.last_commit_by() ),
                self._assets.message_path( Message.YouBrokeBuild )
            ]
        elif info.status() == BuildStatus.Running:
            items = [
                build_name_path,
                self._assets.message_path( Message.StatusRunning ),
                self._assets.user_path( info.last_commit_by() ),
                self._assets.message_path( Message.YouCommitted )
            ]
        else:
            items = [ 
                self._assets.message_path( Message.StatusUnavailable ),
                build_name_path
            ]
            
        self._player.add_to_playlist( items )