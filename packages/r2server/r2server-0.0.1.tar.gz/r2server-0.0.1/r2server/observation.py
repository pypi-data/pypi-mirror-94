#!/bin/env python
## Observation file for r2cloud SDK
# @author Lukáš Plevač <lukasplevac@gmail.com>
# @date 9.9.2020

from datetime        import datetime
from .tle            import tle
#from .groundStation  import groundStation

class observation:
    ## init function
    # @param object     self             - instance of class
    # @param dict       dict_observation - dict of obeservation
    # @param api object api              - instance of api for server with observation
    def __init__(self, dict_observation, api):
        self.id                      = int(dict_observation["id"])
        self.satellite               = int(dict_observation["satellite"])
        self.start                   = datetime.fromtimestamp(dict_observation["start"] / 1000)
        self.end                     = datetime.fromtimestamp(dict_observation["end"]   / 1000)
        self.sampleRate              = dict_observation["sampleRate"]
        self.inputSampleRate         = dict_observation["inputSampleRate"]
        self.frequency               = dict_observation["frequency"]
        self.actualFrequency         = dict_observation["actualFrequency"]
        self.bandwidth               = dict_observation["bandwidth"]
        self.tle                     = tle(dict_observation["tle"])
        self.numberOfDecodedPackets  = dict_observation["numberOfDecodedPackets"]
        self.gain                    = dict_observation["gain"]
        self.groundStation           = dict_observation["groundStation"]
        
        if "channelA" in dict_observation:
            self.channelA                = dict_observation["channelA"]
            self.channelB                = dict_observation["channelB"]
        
        if "dataEntity" in dict_observation:
            self.dataEntity              = dict_observation["dataEntity"]
        
        self.haveA = False
        if "aURL" in dict_observation:
            self.aURL                    = dict_observation["aURL"]
            self.haveA = True
        
        self.haveData = False
        if "data" in dict_observation:
            self.dataURL                 = dict_observation["data"]
            self.haveData = True

        self.haveSpect = False
        if "spectogramURL" in dict_observation:
            self.spectrogramURL           = dict_observation["spectogramURL"]
            self.haveSpect = True
        

        self.api                     = api

    ## get data of decoded image (A Layer)
    # @param object     self             - instance of class
    # @return binnary data of JPG image
    def a(self):
        req = self.api.protocol.get(self.aURL.replace(self.api.protocol.addr, ""))
        
        if req.status_code != 200:
            return req.status_code
            
        return req.content

    ## get binary decoded data
    # @param object     self             - instance of class
    # @return binnary data
    def data(self):
        req = self.api.protocol.get(self.dataURL.replace(self.api.protocol.addr, ""))
        
        if req.status_code != 200:
            return req.status_code
            
        return req.content

    ## get data of spectrogram
    # @param object     self             - instance of class
    # @return binnary data of PNG
    def spectrogram(self):
        req = self.api.protocol.get(self.spectrogramURL.replace(self.api.protocol.addr, ""))
        
        if req.status_code != 200:
            return req.status_code
            
        return req.content