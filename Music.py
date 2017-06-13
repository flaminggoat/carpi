from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview import RecycleView

class MusicFileView(RecycleView):
    def __init__(self, **kwargs):
        super(MusicFileView, self).__init__(**kwargs)
        self.data = [{'text': str(x)} for x in range(100)]
        print(self.data)


class MusicScreen(Screen):
    def update(self, dt):
        pass

