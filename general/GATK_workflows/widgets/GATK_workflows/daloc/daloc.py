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

class OWdaloc(OWBwBWidget):
    name = "daloc"
    description = "localize the GS urls"
    priority = 1
    icon = getIconName(__file__,"cloud-download.png")
    want_main_area = False
    docker_image_name = "varikmp/daloc"
    docker_image_tag = "latest"
    inputs = [("Trigger0",str,"handleInputsTrigger0"),("Trigger1",str,"handleInputsTrigger1"),("Trigger2",str,"handleInputsTrigger2")]
    outputs = [("OutputDir",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    ObjectFilesDir=pset(None)
    DownloadDir=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"daloc")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsTrigger0(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("Trigger0", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsTrigger1(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("Trigger1", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsTrigger2(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("Trigger2", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"OutputDir"):
            outputValue=getattr(self,"OutputDir")
        self.send("OutputDir", outputValue)
