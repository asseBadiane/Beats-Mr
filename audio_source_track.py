from audiostream.sources.thread import ThreadSource
from array import array

class AudioSourceTrack(ThreadSource):
    steps = ()
    steps_nb_samples = 0

    def __init__(self, output_stream, wav_samples, bpm, sample_rate, *args, **kwargs):
        ThreadSource.__init__(self, output_stream, *args, **kwargs)
      
        self.wav_samples = wav_samples

        self.nb_wav_samples = len(wav_samples)
        
        self.current_steps_index = 0
        self.bpm = bpm
        self.sample_rate = sample_rate
        
        self.compute_steps_nb_samples_and_alloc_buffer()

    def set_steps(self, steps):
        if not len(steps) == self.steps:
            self.current_steps_index = 0
        self.steps = steps

    
    def set_bpm(self, bpm):
        # bpm (beats per minute)
        self.bpm = bpm
        self.compute_steps_nb_samples_and_alloc_buffer()
        
    
    def compute_steps_nb_samples_and_alloc_buffer(self):
        if not self.bpm == 0:
            n = int(self.sample_rate * 15 / self.bpm) 
            if self.steps_nb_samples != n:
                self.steps_nb_samples = n
                self.buf = array('h', b"\x00\x00" * self.steps_nb_samples)


    
    def get_bytes(self, *args, **kwargs):

        for i in range(0, self.steps_nb_samples):
            if len(self.steps) > 0:
                if self.steps[self.current_steps_index] == 1:
                    # lancer mon son 
                    self.buf[i] = self.wav_samples[i]
                else:
                    self.buf[i] = 0
            else:
                self.buf[i] = 0
        
        self.current_steps_index += 1
        if self.current_steps_index >= len(self.steps):
            self.current_steps_index = 0
            
        return self.buf.tobytes()