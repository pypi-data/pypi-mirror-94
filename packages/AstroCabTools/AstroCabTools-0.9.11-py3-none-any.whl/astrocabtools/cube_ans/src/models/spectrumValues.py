"""
Class that contain current spectrum values transformed
"""

__all__= ['spectrumValues']
class spectrumValues:

    def __init__(self, wValues, fValues):
        self.__wValues = wValues
        self.__fValues = fValues

    @property
    def wValues(self):
        return self.__wValues

    @property
    def fValues(self):
        return self.__fValues

    @wValues.setter
    def wValues(self, wValues):
        self.__wValues = wValues

    @fValues.setter
    def fValues(self, fValues):
        self.__fValues = fValues
