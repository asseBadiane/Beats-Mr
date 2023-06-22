from audiostream import get_output



class AudioEngine:
    CHANNELS = 1
    SAMPLES_RATE = 44100
    BUFFER_SIZE = 1024

    def __init__(self):
        self.output_stream = get_output(channels=self.CHANNELS,
                                    rate=self.SAMPLES_RATE, 
                                    buffersize=self.BUFFER_SIZE)
        

        
    
