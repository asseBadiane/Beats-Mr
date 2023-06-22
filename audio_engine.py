from audiostream import get_output
from audio_source_one_shot import AudioSourceOneShot


class AudioEngine:
    CHANNELS = 1
    SAMPLES_RATE = 44100
    BUFFER_SIZE = 1024

    def __init__(self):
        self.output_stream = get_output(channels=self.CHANNELS,
                                    rate=self.SAMPLES_RATE, 
                                    buffersize=self.BUFFER_SIZE)
        

        self.audio_source_one_shot = AudioSourceOneShot(self.output_stream)
        self.audio_source_one_shot.start()

        
    
    def play_sound(self, wav_samples):
       self.audio_source_one_shot.set_wav_samples(wav_samples)