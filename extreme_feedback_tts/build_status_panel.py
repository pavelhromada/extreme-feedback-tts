#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import Canvas, NW
from .build_status_enum import BuildStatus
from math import sqrt, ceil


class StatusPanel( Canvas ):
    def __init__( self, master, width, height ):
        super().__init__( master, height = height, width = width,
                          border = 0, background = '#181818', highlightthickness = 0 )
        self._status             = BuildStatus.Success
        self._build_name         = 'AppCore win32'
        self._last_commiter      = 'Pavel Hromada'
        self._branch_name        = 'master'
        self._width              = width
        self._height             = height
        self._padding            = 10
        self._indicator_object   = None
        self._commiter_object    = None
        self._build_name_object  = None
        self._branch_name_object = None

        self._draw_scene()

    def set_status( self, status ):
        if not BuildStatus.has_value( status ):
            return
        self._status = BuildStatus( status )
        if self._indicator_object:
            self.itemconfig( self._indicator_object, fill = self._indicator_color() )

    def set_build_name( self, name ):
        self._build_name = name
        self.itemconfig( self._build_name_object, text = name )

    def set_last_commiter( self, name ):
        self._last_commiter = name
        self.itemconfig( self._commiter_object, text = 'Last commit: ' + name )

    def set_branch_name( self, name ):
        self._build_name = name
        self.itemconfig( self._branch_name_object, text = 'Branch: ' + name )

    def _draw_scene( self ):
        corner_length = int( min( self._width, self._height ) * 0.15 )
        bg_points = [ self._padding, self._padding + corner_length,
                      self._padding + corner_length, self._padding,
                      self._width - self._padding, self._padding,
                      self._width - self._padding, self._height - corner_length - self._padding,
                      self._width - corner_length - self._padding, self._height - self._padding,
                      self._padding, self._height - self._padding ]
        self.create_polygon( bg_points, fill = '#121212' )
        
        in_padding = 2 * self._padding
        in_height = self._height // 2
        corner_offset = int( sqrt( 2 * self._padding ))
        in_points = [ in_padding, self._padding + corner_length + corner_offset,
                      self._padding + corner_length + corner_offset, in_padding,
                      self._width - in_padding, in_padding,
                      self._width - in_padding, in_height - corner_length + corner_offset + 1,
                      self._width - self._padding - corner_length - corner_offset, in_height,
                      in_padding, in_height ]
        self._indicator_object = self.create_polygon( in_points, fill = self._indicator_color() )

        self._build_name_object = self.create_text( self._width / 2,
                                                    self._height * 0.6,
                                                    fill = '#cdcdcd',
                                                    width = self._width - 2 * in_padding,
                                                    text = self._build_name )
        self._branch_name_object = self.create_text( in_padding,
                                                     self._height * 0.75,
                                                     fill = '#777',
                                                     anchor = NW,
                                                     width = self._width - 2 * in_padding,
                                                     text = 'Last commit: ' + self._last_commiter )
        self._commiter_object = self.create_text( in_padding,
                                                  self._height * 0.8,
                                                  fill = '#777',
                                                  anchor = NW,
                                                  width = self._width - 2 * in_padding,
                                                  text = 'Branch: ' + self._branch_name )

    def _indicator_color( self ):
        if self._status == BuildStatus.Success:
            return '#4e9525'#'#729d39'
        elif self._status == BuildStatus.Failed:
            return '#ce2525'#'#8f1d14'
        elif self._status == BuildStatus.Running:
            return '#f89d13'
        else:
            return '#3e3838'
