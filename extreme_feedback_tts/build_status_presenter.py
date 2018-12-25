from abc import ABC, abstractmethod

class BuildStatusPresenter( ABC ):
    '''Interface class representing general presenter of build status.'''

    @abstractmethod
    def update( self, build_statuses ):
        pass