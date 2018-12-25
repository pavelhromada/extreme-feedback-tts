import requests
from .build_status_enum import BuildStatus


class BuildInfo:
    '''Loads the status of defined build.'''

    def __init__( self, base_url, config ):
        self._config    = config
        self._status    = BuildStatus.Success
        self._committer = 'unknown'
        
        branch   = config[ 'branch' ]
        build_id = config[ 'build_type_id' ]
        branch_locator  = f',branch(name:{branch})' if branch else ''
        builds_locator  = f'locator=buildType(id:{build_id}),count:1,running:any{branch_locator}'
        changes_locator = f'locator=buildType(id:{build_id}),count:1{branch_locator}'

        self._status_url = f'{base_url}guestAuth/app/rest/builds?{builds_locator}'
        self._committer_url = f'{base_url}guestAuth/app/rest/changes?{changes_locator}'


    def reload( self ):
        r = requests.get( self._status_url, headers = { 'Accept': 'application/json' })
        success = r.json()[ 'build' ][ 0 ][ 'status' ] == 'SUCCESS'
        running = r.json()[ 'build' ][ 0 ][ 'state' ] == 'running'
        
        if running:
            self._status = BuildStatus.Running
        elif success:
            self._status = BuildStatus.Success
        else:
            self._status = BuildStatus.Failed

        r = requests.get( self._committer_url, headers = { 'Accept': 'application/json' })
        self._committer = r.json()[ 'change' ][ 0 ][ 'username' ] # TODO parse user name GIT/SVN


    def status( self ):
        return self._status


    def last_commit_by( self ):
        return self._committer


    def brach( self ):
        return self._config[ 'branch' ]

    
    def gui_name( self ):
        return self._config[ 'gui_name' ]
