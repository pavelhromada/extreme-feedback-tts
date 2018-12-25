#!/usr/bin/env python3

from enum import Enum

class BuildStatus( Enum ):
    Success = 1
    Failed  = 2
    Running = 3

    @classmethod
    def has_value( cls, value ):
        return any( BuildStatus( value ) == BuildStatus( e.value ) for e in cls )
