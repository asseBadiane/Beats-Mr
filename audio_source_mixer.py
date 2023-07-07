from audiostream.sources.thread import ThreadSource
from array import array
from audio_source_track import AudioSourceTrack

class AudioSourceMixer(ThreadSource):
    buf = None

    def __init__(self, output_stream, all_wav_samples, bpm, sample_rate, nb_steps, on_current_step_changed, min_bpm, *args, **kwargs):
        ThreadSource.__init__(self, output_stream, *args, **kwargs)
      
        self.tracks = []
        for i in range(0, len(all_wav_samples)):
            track = AudioSourceTrack(output_stream, all_wav_samples[i], bpm, sample_rate, min_bpm)
            track.set_steps((0, ) * nb_steps)
            self.tracks.append(track)

        self.buf = None
        self.silence = array('h', b"\x00\x00" * self.tracks[0].buffer_nb_samples)

        self.nb_steps = nb_steps
        self.current_sample_index = 0
        self.current_steps_index = 0
        self.sample_rate = sample_rate
        self.on_current_step_changed = on_current_step_changed
        self.is_playing = False
        self.min_bpm = min_bpm
        self.bpm = bpm


    def set_steps(self, index, steps):
        if index >= len(self.tracks):
            return
        
        if not len(steps) == self.nb_steps:
            self.tracks[index].set_steps(steps)

    
    def set_bpm(self, bpm):
        if bpm < self.min_bpm:
            return
        self.bpm = bpm

    def audio_play(self):
        self.is_playing = True

    def audio_stop(self):
        self.is_playing = False

        
    def get_bytes(self, *args, **kwargs):

        for i in range(0, len(self.tracks)):
            self.tracks[i].set_bpm(self.bpm)

        steps_nb_samples = self.tracks[0].steps_nb_samples
        # if self.buf is None or not len(self.buf) == steps_nb_samples:
        #     self.buf = array('h', b"\x00\x00" * steps_nb_samples)    

        if not self.is_playing:
            # for i in range(0, steps_nb_samples):
                # self.buf[i] = 0
            return self.silence[0:steps_nb_samples].tobytes()

        tracks_buffers = []
        for i in range(0, len(self.tracks)):
            track = self.tracks[i]
            track_buffer = track.get_bytes_array()    
            tracks_buffers.append(track_buffer)    

        # for i in range(0, steps_nb_samples):
        #     self.buf[i] = 0
        #     for j in range(0, len(tracks_buffers)):
        #         self.buf[i] += tracks_buffers[j][i]

        s  = map(sum, zip(*tracks_buffers))
        self.buf = array('h', s)


        if self.on_current_step_changed is not None:
            # Décalage de deux steps pour synchroniser l'affichage
            # step courant e le son attendu (à causes des buffers audios)
            step_index_for_display = self.current_steps_index - 2
            if step_index_for_display < 0:
                step_index_for_display += self.nb_steps
            self.on_current_step_changed(step_index_for_display)
        
        self.current_steps_index += 1
        if self.current_steps_index >= self.nb_steps:
            self.current_steps_index = 0
            
        return self.buf[0:steps_nb_samples].tobytes()