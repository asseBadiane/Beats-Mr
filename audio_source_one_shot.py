from audiostream.sources.thread import ThreadSource
from array import array

class AudioSourceOneShot(ThreadSource):


    def __init__(self, output_stream, *args, **kwargs):
        ThreadSource.__init__(self, output_stream, *args, **kwargs)
        self.chunk_nb_samples = 32
        self.buf = array('h', b"\x00\x00" * self.chunk_nb_samples)


    
    def get_bytes(self, *args, **kwargs):
        return self.buf.tobytes()