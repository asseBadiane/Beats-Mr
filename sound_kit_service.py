import wave
from array import array

class Sound:
    nb_samples = 0
    samples = None

    def __init__(self, filename, displayname):
        self.filename = filename
        self.displayname = displayname
        self.load_sound()
 

    def load_sound(self):
        wave_file = wave.open(self.filename, mode='rb')
        self.nb_samples = wave_file.getnframes()
        frames = wave_file.readframes(self.nb_samples)
        self.samples = array("h", frames)


class Soundkit:
    sounds = ()

    def get_nb_sound(self):
        return  len(self.sounds)
    

    def get_all_samples(self):
        all_samples = []
        for i in range(0, len(self.sounds)): 
            all_samples.append(self.sounds[i].samples)

        return all_samples


class SoundKit1(Soundkit):
    sounds = (
        Sound("sounds/kit1/kick.wav", "KICK"),
        Sound("sounds/kit1/snare.wav", "SNARE"),
        Sound("sounds/kit1/shaker.wav", "SHAKER"),
        Sound("sounds/kit1/clap.wav", "CLAP"),
    )

class SoundKit1All(Soundkit):
    sounds = (
        Sound("sounds/kit1/bass.wav", "BASS"),
        Sound("sounds/kit1/effects.wav", "EFFECTS"),
        Sound("sounds/kit1/kick.wav", "KICK"),
        Sound("sounds/kit1/pluck.wav", "PLUCK"),
        Sound("sounds/kit1/snare.wav", "SNARE"),
        Sound("sounds/kit1/shaker.wav", "SHAKER"),
        Sound("sounds/kit1/clap.wav", "CLAP"),
        Sound("sounds/kit1/kick.wav", "KICK"),
        Sound("sounds/kit1/vocal_chop.wav", "VOCAL_CHOP"),
        
        
    )




class SoundKitService:
    soundkit = SoundKit1All()

    def get_nb_tracks(self):
        return self.soundkit.get_nb_sound()

    def get_sound_index(self, index):
        if index >= len(self.soundkit.sounds):
            return None

        return self.soundkit.sounds[index]

