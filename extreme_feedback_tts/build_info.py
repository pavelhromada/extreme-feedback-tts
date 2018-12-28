#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import requests
from .build_status_enum import BuildStatus


class BuildInfo:
    '''Loads the status of defined build.'''

    def __init__( self, base_url, config ):
        self._config            = config
        self._status_changed    = False
        self._status            = BuildStatus.Unavailable
        self._committer         = 'unknown'
        
        branch          = config[ 'branch' ]
        build_id        = config[ 'build_type_id' ]
        branch_locator  = f',branch(name:{branch})' if branch else ''
        builds_locator  = f'locator=buildType(id:{build_id}),count:1,running:any{branch_locator}'
        changes_locator = f'locator=buildType(id:{build_id}),count:1{branch_locator}'

        self._status_url    = f'{base_url}guestAuth/app/rest/builds?{builds_locator}'
        self._committer_url = f'{base_url}guestAuth/app/rest/changes?{changes_locator}'

    def reload( self ):
        self._refresh_build_status()
        self._refresh_last_committer_name()

    def status_has_changed( self ):
        return self._status_changed

    def status( self ):
        return self._status

    def last_commit_by( self ):
        return self._committer

    def build_id( self ):
        return self._config[ 'build_type_id' ]

    def brach( self ):
        return self._config[ 'branch' ]

    def gui_name( self ):
        return self._config[ 'gui_name' ]

    def _refresh_build_status( self ):
        try:
            r = requests.get( self._status_url, headers = { 'Accept': 'application/json' })
            r.raise_for_status()
            success = r.json()[ 'build' ][ 0 ][ 'status' ] == 'SUCCESS'
            running = r.json()[ 'build' ][ 0 ][ 'state' ] == 'running'
            new_status = BuildStatus.Unavailable
            
            if running:
                new_status = BuildStatus.Running
            elif success:
                new_status = BuildStatus.Success
            else:
                new_status = BuildStatus.Failed

            self._status_changed = new_status != self._status
            self._status = new_status
        except requests.exceptions.RequestException:
            self._status_changed = self._status != BuildStatus.Unavailable
            self._status = BuildStatus.Unavailable
            logging.exception( 'Error obtaining build status' )

    def _refresh_last_committer_name( self ):
        try:
            r = requests.get( self._committer_url, headers = { 'Accept': 'application/json' })
            r.raise_for_status()
            self._committer = r.json()[ 'change' ][ 0 ][ 'username' ] # TODO parse user name GIT/SVN
        except requests.exceptions.RequestException:
            self._committer = 'unknown'
            logging.exception( 'Error obtaining last committer name' )