from audiostream.sources.thread import ThreadSource
from array import array
from audio_source_track import AudioSourceTrack

class AudioSourceMixer(ThreadSource):
    buf = None

    def __init__(self, output_stream, all_wav_samples, bpm, sample_rate, nb_steps, *args, **kwargs):
        ThreadSource.__init__(self, output_stream, *args, **kwargs)
      
        self.tracks = []
        for i in range(0, len(all_wav_samples)):
            track = AudioSourceTrack(output_stream, all_wav_samples[i], bpm, sample_rate)
            track.set_steps((0, ) * nb_steps)
            self.tracks.append(track)

        self.nb_steps = nb_steps
        self.current_sample_index = 0
        self.current_steps_index = 0
        self.sample_rate = sample_rate


    def set_steps(self, index, steps):
        if index >= len(self.tracks):
            return
        
        if not len(steps) == self.nb_steps:
            self.tracks[index].set_steps(steps)

    
    def set_bpm(self, bpm):
        for i in range(0, len(self.tracks)):
            self.tracks[i].set_bpm(bpm)

        
    def get_bytes(self, *args, **kwargs):

        steps_nb_samples = self.tracks[0].steps_nb_samples
        if self.buf is None or not len(self.buf) == steps_nb_samples:
            self.buf = array('h', b"\x00\x00" * steps_nb_samples)    

        tracks_buffers = []
        for i in range(0, len(self.tracks)):
            track = self.tracks[i]
            track_buffer = track.get_bytes_array()    
            tracks_buffers.append(track_buffer)    

        for i in range(0, steps_nb_samples):
            self.buf[i] = 0
            for j in range(0, len(tracks_buffers)):
                self.buf[i] += tracks_buffers[j][i]
        
        self.current_steps_index += 1
        if self.current_steps_index >= self.nb_steps:
            self.current_steps_index = 0
            
        return self.buf.tobytes()