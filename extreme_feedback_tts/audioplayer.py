import os
import simpleaudio as sa


class AudioPlayer:
    '''Plays mp3 audio content.'''

    def __init__( self ):
        pass


    def play_all_from_path( self, path ):
        for dirpath, _, files in os.walk( path ):
            for filename in [f for f in files if f.endswith( '.wav' )]:
                self._play( os.path.join( dirpath, filename ))
                print( f'played {filename}' )


    def _play( self, audio_file_path ):
        wave_obj = sa.WaveObject.from_wave_file( audio_file_path )
        play_obj = wave_obj.play()
        play_obj.wait_done()
