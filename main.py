from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight
from panda3d.core import Vec4
from panda3d.core import DirectionalLight
from direct.task import Task
from math import pi, sin, cos


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.timeClock = 0
        self.rgbRange = 0
        self.old_time = 0
        self.setBackgroundColor(0, 0, 0)
        self.sunlight = DirectionalLight('sun')
        self.sunlight.setColor((self.rgbRange, self.rgbRange, self.rgbRange, 1))
        self.sunlight_np = self.render.attachNewNode(self.sunlight)
        self.sunlight_np.setHpr(0, -60, 0) 
        self.render.setLight(self.sunlight_np)
        
        # Включаем освещение
        self.render.setLight(self.sunlight_np)

        mySound = self.loader.loadSfx("backSound.mp3")
        
        self.scene = self.loader.loadModel("hand_painted_forest/1/scene.gltf") 
        
        '''ainLight = DirectionalLight("main light") # направленный свет
        self.mainLightNodePath = self.render.attachNewNode(mainLight)
        self.mainLightNodePath.setHpr(-100, -100, -500)
        self.render.setLight(self.mainLightNodePath)'''

        self.ambientLight = AmbientLight("ambient light") # общий свет (освещение всего)
        self.ambientLight.setColor(Vec4(0.5, 0.5, 0.5, 1)) # тут можно регулировать
        self.ambientLightNodePath = self.render.attachNewNode(self.ambientLight)
        self.render.setLight(self.ambientLightNodePath)
        
        self.scene.reparentTo(self.render)
        #self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(0, 10, -30)
        self.scene.setH(90)

        self.render.setShaderAuto() # панда автоматически обрабатывает шейдеры
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask") # подключение обработчика события вращение камеры
        mySound.setVolume(0.5)
        mySound.setLoop(True)
        mySound.play()
        self.set_night_lighting()


    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        if  task.time - self.old_time >= 1:
            self.timeClock += 1
            self.old_time = task.time
            self.set_day_lighting(self.timeClock/100, self.timeClock/100, self.timeClock/100)
            if 0.5+self.timeClock/100 >= 1:
                self.ambientLight.setColor(Vec4(1, 1, 1, 1))
            else:
                self.ambientLight.setColor(Vec4(0.5+self.timeClock/100, 0.5+self.timeClock/100, 0.5+self.timeClock/100, 1))
            print(self.timeClock/100)
        return Task.cont
    
    def set_day_lighting(self, r, g, b):
        # Яркий белый свет
        self.sunlight.setColor((r, g, b, 1))
        self.sunlight_np.setHpr(0, -60, 0)  # Солнце высоко
        self.setBackgroundColor(r, g, b)
    
    def set_night_lighting(self):
        self.sunlight.setColor((0.2, 0.2, 0.5, 1))
        self.sunlight_np.setHpr(180, -30, 0)  # Луна в другом положении
        #self.setBackgroundColor(0.05, 0.05, 0.2)


app = MyApp()
app.run()


