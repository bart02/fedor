from robot import *

Scene = Scene('192.168.0.108')
Scene.reset()

Body = Body('192.168.0.108')

Platform = Platform('192.168.0.108')

Platform.go_time(25, 100)
Platform.go_time(3, 100, 25)
