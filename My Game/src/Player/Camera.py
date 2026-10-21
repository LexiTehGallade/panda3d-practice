from direct.task import Task

class ThirdPersonCam:
    def __init__(self,player_node,avatar_node):
        self.av = avatar_node
        self.player_node = player_node
        self.cam_node = self.cam_node = self.player_node.attachNewNode("camnode")
        taskMgr.add(self.mouseTask, "MouseResetPos")

    def InitializeCamera(self):
        base.camera.setPos(0, -5, 0)
        self.cam_node.setPos(0,0,1.5)
        base.camera.reparentTo(self.cam_node)
        self.cam_node.setH(180)
        base.camLens.setFov(70)
        return self.cam_node

    # We need to keep the mouse cursor locked to the center of the screen for a mouselook control scheme.
    def mouseTask(self,task):
        self.mw = base.mouseWatcherNode

        if self.mw.hasMouse():
            # get the position, which at center is (0, 0)
            self.x = round(self.mw.getMouseX(),3)
            self.y = round(self.mw.getMouseY(),3)

            # move mouse back to center
            props = base.win.getProperties()
            base.win.movePointer(0,
                                 props.getXSize() // 2,
                                 props.getYSize() // 2)
            # now, x and y can be considered relative movements
            if abs(self.x) > 0.001:
                self.cam_node.setH(self.cam_node,-(self.x*60))
            if abs(self.y) > 0.001:
                self.cam_node.setP(self.cam_node, (self.y*60))
            self.cam_node.setR(0)
            self.av.setH(self.cam_node,180)
            self.av.setP(0)
            self.av.setR(0)
        return Task.cont