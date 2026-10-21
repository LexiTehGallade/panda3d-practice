from direct.gui.DirectGui import *
from panda3d.core import LVector3f as LVec
from direct.showbase import DirectObject
from direct.showbase.ShowBase import ShowBase


class UI:
    def __init__(self):
        self.elements = {}
        self.create_UI()

    def create_UI(self):
        self.elements["Exit"] = DirectButton(parent=base.a2dTopRight)
        self.elements["Exit"].setScale(0.8)
        self.elements["Exit"].setPos(-0.12,0,-0.12)