class ObjectWorld:
    def __init__(self):
        self.world = {}

    def CreateWorld(self):
        self.world["Ground"] = loader.loadModel("../resources/Models/worldplane.bam")
        self.world["Ground"].reparentTo(render)
        self.world["Ground"].setTwoSided(True)
        self.world["Ground"].setScale(15)
        self.world["Skybox"] = loader.loadModel("../resources/Models/Skybox.egg")
        self.world["Skybox"].setTwoSided(True)
        self.world["Skybox"].setColor(0.8, 0.8, 1, 1)



        return self.world

