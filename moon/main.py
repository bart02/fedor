from robot import *

nikita = '192.168.0.108'
artem = '192.168.1.135'

fedor = Robot(nikita)
plat = Robot(nikita, platform=True)

fedor.reset()
plat.platform.go_time(25, 100)
plat.platform.go_time(11, 100, 25)
plat.platform.go_time(9, 100)

fedor.body.click_button()
fedor.body.index()

# workn't
plat.platform.go_time(10, -100, -25)
sleep(1)
plat.platform.go_time(15, 100)
plat.platform.go_time(10, 100, -25)
