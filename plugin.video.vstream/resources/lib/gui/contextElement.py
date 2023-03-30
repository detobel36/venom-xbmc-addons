from resources.lib.handler.outputParameterHandler import OutputParameterHandler


class ContextElement:

    def __init__(self):
        self.__sTitle = ''
        self.__oOutputParameterHandler = OutputParameterHandler()

    def setFunction(self, sFunctionName):
        self.__sFunctionName = sFunctionName

    def getFunction(self):
        return self.__sFunctionName

    def setFile(self, sFile):
        self.__sFile = sFile

    def getFile(self):
        return self.__sFile

    def setTitle(self, title):
        self.__sTitle = title

    def getTitle(self):
        return self.__sTitle

    def setSiteName(self, sSiteName):
        self.__sSiteName = sSiteName

    def getSiteName(self):
        return self.__sSiteName

    def setOutputParameterHandler(self, output_parameter_handler):
        self.__oOutputParameterHandler = output_parameter_handler

    def getOutputParameterHandler(self):
        return self.__oOutputParameterHandler
