from robot import *

Scene = Scene('192.168.1.135')
Scene.reset()

Body = Body('192.168.1.135')

Platform = Platform('192.168.1.135')

Platform.go_time(25, 100)
Platform.go_time(3, 100, 25)
