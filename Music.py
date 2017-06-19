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
    def play(self, play_next=False):
        global music_screen
        f = {}
        f['path'] = self.path
        f['title'] = self.title
        f['artist'] = self.artist
        if play_next:
            music_screen.play_next(f)
            return
        music_screen.play_now(f)
        
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
        self.audio_list = []
        self.audio_pos = 0
    def update(self, dt):
        pass
    def play_now(self, audio_file):
        self.audio_list.insert(0, audio_file)
        self.play()
    def play_next(self, audio_file):
        self.audio_list.insert(0, audio_file)
    def play(self, obj=None):
        if len(self.audio_list) <= 0:
            #end of song queue reached
            if self.audio.state != 'play':
                self.ids.play_button.text = 'Play'
            return
        f = self.audio_list.pop(0)
        if self.audio:
            self.audio.unbind(on_stop=self.play)
            self.audio.stop()
            self.audio.unload()
            self.audio = None
        if f['path']:
            audio = SoundLoader.load(f['path'])
            if audio:
                #if the audio file loaded successfully
                audio.play()
                self.ids.now_playing_label.text = f['title']
                self.ids.now_playing_artist.text = f['artist']
                self.ids.play_button.text = 'Pause'
                audio.bind(on_stop=self.play)
                self.audio = audio
                return
        #The audio file failed to load, try playing next file
        self.play()
    #def on_stop(self, obj):
    #    if len(self.audio_list) > 0:
    #        play(self.audio_list)
    #    else:
    #        #changes the play/pause button text to play
    #        self.ids.play_button.text = "Play"
    def play_pause(self):
        if self.audio:
            if self.audio.state == 'play':
                #store the audio position so it can resume from the correct place
                self.audio_pos = self.audio.get_pos()
                #avoid playing the next song when playback stops
                self.audio.unbind(on_stop=self.play)
                self.audio.stop()
                self.ids.play_button.text = 'Play'
            else:
                #rebind on stop event
                self.audio.bind(on_stop=self.play)
                self.audio.play()
                #seek to the position that the audio was paused at
                self.audio.seek(self.audio_pos)
                self.ids.play_button.text = 'Pause'
        else:
            self.play()
