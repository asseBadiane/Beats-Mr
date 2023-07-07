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
        self.silence = array('h', b"\x00\x00" * self.buffer_nb_samples)

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

        result_buf = None

        # 1 Aucun pas d'activé silence
        if self.no_steps_activated():
            result_buf = self.silence[0:self.steps_nb_samples]
        elif self.steps[self.current_steps_index] == 1 :
            # 2 step activé et le son a plus de sample que 1 step
            # self.last_sound_sample_start_index = self.current_sample_index
            if self.nb_wav_samples  >= self.steps_nb_samples:
                result_buf = self.wav_samples[0:self.steps_nb_samples]
            else:
                # 3 step activé et le son a moins de sample que 1 step
                silences_nb_samples = self.steps_nb_samples - self.nb_wav_samples
                result_buf = self.wav_samples[0:self.nb_wav_samples]
                result_buf.extend(self.silence[0:silences_nb_samples])
        else :
            #  4 le step n'est pas activé, mais on doit jouer la suite du son
            index =  self.current_sample_index - self.last_sound_sample_start_index
            # 4.1 Ce qu'il nous reste à jouer est plus long qu'un step
            if index >= self.nb_wav_samples:
            # le step n'est pas activé, mais on a fini de jouer le son --> Silence
                result_buf = self.silence[0:self.steps_nb_samples]
            elif self.nb_wav_samples - index >= self.steps_nb_samples:
                result_buf = self.wav_samples[index:self.steps_nb_samples + index]
            else:
                # 4.2 Ce qu'il nous reste à jouer est plus petit qu'un step
                silence_nb_samples = self.steps_nb_samples - (self.nb_wav_samples - index)
                result_buf = self.wav_samples[index:self.nb_wav_samples]
                result_buf.extend(self.silence[0:silence_nb_samples])


        # for i in range(0, self.steps_nb_samples):
        #     if len(self.steps) > 0 and not self.no_steps_activated():
        #         if self.steps[self.current_steps_index] == 1 and i < self.nb_wav_samples:
            
        #             self.buf[i] = self.wav_samples[i]
        #             if i == 0:
        #                 self.last_sound_sample_start_index = self.current_sample_index
        #         else:
        #             index =  self.current_sample_index - self.last_sound_sample_start_index
        #             if index < self.nb_wav_samples:
        #                 self.buf[i] = self.wav_samples[index]
        #             else:
        #                 self.buf[i] = 0
        #     else :
        #         self.buf[i] = 0
            
        self.current_sample_index += self.steps_nb_samples
            
            
        self.current_steps_index += 1
        if self.current_steps_index >= len(self.steps):
            self.current_steps_index = 0

        if result_buf is None:
            print("result_buf is None")
        elif not len(result_buf) == self.steps_nb_samples:
            print("result_buf len is not steps_nb_samples")
            
        return result_buf
    

    def get_bytes(self, *args, **kwargs):
        return self.get_bytes_array().tobytes()