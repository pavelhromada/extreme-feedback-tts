import os
import time
from .configuration import Configuration
from .buildinfo import BuildInfo
from .build_status_audio_presenter import AudioPresenter
from .build_status_gui_presenter import GuiPresenter

class ExtremeFeedbackApp:
    '''Entry point to extreme feedback application.'''

    def __init__( self, config_file_path, show_gui, fullscreen ):
        self._config_path   = config_file_path
        self._show_gui      = show_gui
        self._fullscreen    = fullscreen
        self._builds_info   = []
        self._presenters    = []


    def run( self ):
        try:
            self._run_internal()
        except KeyboardInterrupt:
            print( '\nApplication exit.' )


    def _run_internal( self ):
        if not self._config_path:
            print( 'No config path provided. Exit.' )
            return

        print( f'Loading config [{self._config_path}] ...' )
        config = Configuration( self._config_path )

        if self._show_gui:
            self._presenters.append( GuiPresenter( config, self._fullscreen ))

        self._presenters.append( AudioPresenter( config ))

        for build_config in config.builds():
            self._builds_info.append( BuildInfo( config.build_server_url(), build_config ))

        print( 'Starting application loop ...' )

        while True:
            for build in self._builds_info:
                build.reload()

            for presenter in self._presenters:
                presenter.update( self._builds_info )

            time.sleep( 20 ) # 20s is refresh period
