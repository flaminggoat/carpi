from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
import fnmatch
import os
from eyed3.id3 import Tag

class MusicFileBar(BoxLayout):
    title = StringProperty("")
    path = StringProperty("")
    pass

class MusicFileView(RecycleView):
    def __init__(self, **kwargs):
        super(MusicFileView, self).__init__(**kwargs)
        self.files = []
        tag = Tag()
        for root, dirnames, filenames in os.walk('/home/pi/Music/Random'):
            for filename in fnmatch.filter(filenames, '*.mp3*'):
                path = os.path.join(root,filename)
                tag.parse(path)
                self.files.append({'title': tag.title, 'path': path}) 

class MusicScreen(Screen):
    def __init__(self, **kwargs):
        super(MusicScreen, self).__init__(**kwargs)
        print('fetching music')
        self.music_list_data = []
        for root, dirnames, filenames in os.walk('/home/pi/Music/Random'):
            for filename in fnmatch.filter(filenames, '*.mp3*'):
                self.music_list_data.append({'text': filename})
        #print(str(self.ids))
        #self.root.ids.music_list.data = data

    def update(self, dt):
        pass

