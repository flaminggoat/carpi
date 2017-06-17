from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.audio import SoundLoader
import fnmatch
import os
from tinytag import TinyTag

music_screen = None

class MusicFileBar(BoxLayout):
    title = StringProperty("")
    path = StringProperty("")
    def play(self):
        global music_screen
        music_screen.play(self.path, self.title)
        
class MusicFileView(RecycleView):
    def __init__(self, **kwargs):
        super(MusicFileView, self).__init__(**kwargs)
        self.music_files = []
        for root, dirnames, filenames in os.walk('/home/pi/Music'):
            for filename in filenames:
                if filename.lower().endswith(('.mp3','.m4a','.flac')):
                    path = os.path.join(root,filename)
                    tag = TinyTag.get(path, image=True)
                    #print(tag.get_image())
                    if tag.title is None:
                        tag.title = filename
                    if tag.artist is None:
                        tag.artist = 'None'
                    self.music_files.append({'title': tag.title, 'path': path, 'artist': tag.artist})
        self.files = self.music_files
    def filter(self, text):
        self.files = []
        print('filter ' + text)
        if(text is None) or text == '':
            print('no filter')
            self.data = self.music_files
            return
        text = text.lower()
        for music_file in self.music_files:
            if (text in music_file['title'].lower()) or (text in music_file['artist'].lower()):
                print(music_file['title'] + ' ' + music_file['artist'])
                self.files.append(music_file)
        self.data = self.files

class MusicScreen(Screen):
    def __init__(self, **kwargs):
        super(MusicScreen, self).__init__(**kwargs)
        global music_screen
        music_screen = self
        self.audio = None
        self.audio_path = None
        self.audio_title = None
        self.audio_pos = 0
    def update(self, dt):
        pass
    def play(self, path=None, title=None):
        if path is None:
            path = self.audio_path
            title = self.audio_title
        if self.audio:
            self.audio.stop()
            self.audio.unload()
        if path:
            self.audio = SoundLoader.load(path)
        if self.audio:
            self.audio_path = path
            self.audio_title = title
            self.audio.play()
            self.ids.now_playing_label.text = title
            self.ids.play_button.text = 'Pause'
            self.audio.bind(on_stop=self.on_stop)
    def on_stop(self, obj):
        #changes the play/pause button text to play
        self.ids.play_button.text = "Play"
    def play_pause(self):
        if self.audio:
            if self.audio.state == 'play':
                #store the audio position so it can resume from the correct place
                self.audio_pos = self.audio.get_pos()
                self.audio.stop()
                self.ids.play_button.text = 'Play'
            else:
                self.audio.play()
                #seek to the position that the audio was paused at
                self.audio.seek(self.audio_pos)
                self.ids.play_button.text = 'Pause'
