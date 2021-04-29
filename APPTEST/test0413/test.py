from kivy.app import App
from kivy.uix.camera import Camera

class MyApp(App):

    def build(self):
        cam=Camera(index=0,resolution=(640,480), size=(500,500))
        return cam

if __name__ == '__main__':
    MyApp().run()