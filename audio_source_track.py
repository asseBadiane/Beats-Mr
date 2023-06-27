from audiostream.sources.thread import ThreadSource
from array import array

class AudioSourceTrack(ThreadSource):
    steps = ()
    steps_nb_samples = 0

    def __init__(self, output_stream, wav_samples, bpm, sample_rate, min_bpm, *args, **kwargs):
        ThreadSource.__init__(self, output_stream, *args, **kwargs)
      
        self.wav_samples = wav_samples
        self.nb_wav_samples = len(wav_samples)
        self.current_sample_index = 0
        
        self.current_steps_index = 0 # le pas au courant
        self.bpm = bpm # beats per minute
        self.sample_rate = sample_rate
        
        # self.compute_steps_nb_samples_and_alloc_buffer()
        self.last_sound_sample_start_index = 0 # l'index de début des samples du son
        self.min_bpm = min_bpm

        self.steps_nb_samples = self.compute_steps_nb_samples(bpm)
        self.buffer_nb_samples = self.compute_steps_nb_samples(min_bpm)
        self.buf = array('h', b"\x00\x00" * self.buffer_nb_samples)

        if not self.bpm == 0:
            n = int(self.sample_rate * 15 / self.bpm) 
            if self.steps_nb_samples != n:
                self.steps_nb_samples = n
                self.buf = array('h', b"\x00\x00" * self.steps_nb_samples)

    def set_steps(self, steps):
        if not len(steps) == len(self.steps):
            self.current_steps_index = 0
        self.steps = steps

    
    def set_bpm(self, bpm):
        # bpm (beats per minute)
        self.bpm = bpm
        self.steps_nb_samples =  self.compute_steps_nb_samples(bpm)
        
    
    def compute_steps_nb_samples(self, bpm_value):

        if not self.bpm == 0:
            n = int(self.sample_rate * 15 / bpm_value)
            return n
        return 0


    def no_steps_activated(self):
        if len(self.steps) ==  0:
                return True
        
        for i in range(0, len(self.steps)):
            if self.steps[i] == 1:
                return False
            
            return True 
    
    def get_bytes_array(self):

        for i in range(0, self.steps_nb_samples):
            if len(self.steps) > 0 and not self.no_steps_activated():
                if self.steps[self.current_steps_index] == 1 and i < self.nb_wav_samples:
            
                    self.buf[i] = self.wav_samples[i]
                    if i == 0:
                        self.last_sound_sample_start_index = self.current_sample_index
                else:
                    index =  self.current_sample_index - self.last_sound_sample_start_index
                    if index < self.nb_wav_samples:
                        self.buf[i] = self.wav_samples[index]
                    else:
                        self.buf[i] = 0
            else :
                self.buf[i] = 0
            
            self.current_sample_index += 1
            
            
        self.current_steps_index += 1
        if self.current_steps_index >= len(self.steps):
            self.current_steps_index = 0
            
        return self.buf[0:self.steps_nb_samples]
    

    def get_bytes(self, *args, **kwargs):
        return self.get_bytes_array().tobytes()