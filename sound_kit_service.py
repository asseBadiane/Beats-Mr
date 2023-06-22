

class Sound:
    def __init__(self, filename, displayname):
        self.filename = filename
        self.displayname = displayname

class Soundkit:
    sounds = ()

    def get_nb_sound(self):
        return  len(self.sounds)

class SoundKit1(Soundkit):
    sounds = (
        Sound("sounds/kit1/kick.wav", "KICK"),
        Sound("sounds/kit1/snare.wav", "SNARE"),
        Sound("sounds/kit1/shaker.wav", "SHAKER"),
        Sound("sounds/kit1/clap.wav", "CLAP"),
    )

class SoundKitService:
    soundkit = SoundKit1()

    def get_nb_tracks(self):
        return self.soundkit.get_nb_sound()

    def get_sound_index(self, index):
        if index >= len(self.soundkit.sounds):
            return None

        return self.soundkit.sounds[index]

