#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class BuildStatusPresenter( ABC ):
    '''Interface class representing general presenter of build status.'''

    @abstractmethod
    def update( self, build_statuses ):
        pass