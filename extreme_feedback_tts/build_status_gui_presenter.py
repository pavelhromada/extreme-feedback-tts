#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from math import sqrt, ceil
from tkinter import Tk, Canvas, YES, BOTH
from .build_status_presenter import BuildStatusPresenter
from .build_status_panel import StatusPanel


class GuiPresenter( BuildStatusPresenter ):
    '''Displays builds status on the screen.'''

    def __init__( self, config, fullscreen ):
        self._tk = Tk()
        self._tk.title( 'Build status' )
        self._tk.geometry( '800x600+0+0')
        self._tk.attributes( '-fullscreen', fullscreen )
        self._tk.resizable( False, False )
        self._tk[ 'background' ] = '#181818'
        self._tk.protocol( 'WM_DELETE_WINDOW', lambda: None )
        self._tk.update_idletasks()
        self._panels = []

    def update( self, build_infos ):
        logging.debug( 'Updating GUI ...' )
        
        if not self._panels:
            self._create_panels( len( build_infos ), 5 ) # max 5 columns

        for info, panel in zip( build_infos, self._panels ):
            panel.set_status( info.status() )
            panel.set_build_name( info.gui_name() )
            panel.set_last_committer( info.last_commit_by() )
            panel.set_branch_name( info.brach() )

        self._tk.update()

    def _create_panels( self, count, max_columns ):
        scene_width  = self._tk.winfo_width()
        scene_height = self._tk.winfo_height()
        panel_width  = scene_width / count if count < max_columns else scene_width / max_columns
        panel_height = scene_height / ceil( count / max_columns )
        self._panels = [ StatusPanel( self._tk, panel_width, panel_height ) for _ in range( count )]

        for i, panel in enumerate( self._panels ):
            panel.grid( row = i // max_columns, column = i % max_columns )