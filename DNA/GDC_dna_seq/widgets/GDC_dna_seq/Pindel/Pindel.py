import os
import glob
import sys
import functools
import jsonpickle
from collections import OrderedDict
from Orange.widgets import widget, gui, settings
import Orange.data
from Orange.data.io import FileFormat
from DockerClient import DockerClient
from BwBase import OWBwBWidget, ConnectionDict, BwbGuiElements, getIconName, getJsonName
from PyQt5 import QtWidgets, QtGui

class OWPindel(OWBwBWidget):
    name = "Pindel"
    description = "Minimum Python3 container with pip"
    priority = 10
    icon = getIconName(__file__,"pindel.png")
    want_main_area = False
    docker_image_name = "biodepot/pindel"
    docker_image_tag = "test"
    inputs = [("inputfiles",str,"handleInputsinputfiles"),("Trigger",str,"handleInputsTrigger")]
    outputs = [("outputfiles",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    inputfiles=pset([])
    configuration=pset(None)
    filetags=pset([])
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"Pindel")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsinputfiles(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("inputfiles", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("Trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputfiles"):
            outputValue=getattr(self,"outputfiles")
        self.send("outputfiles", outputValue)
