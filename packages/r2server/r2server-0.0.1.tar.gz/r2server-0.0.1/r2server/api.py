#!/bin/env python
## api file for r2cloud SDK
# @author Lukáš Plevač <lukasplevac@gmail.com>
# @date 9.9.2020

from .protocol           import protocol
from .observation        import observation
#from .baseTle            import baseTle

class api:
    ## init function
    # @param object   self     - instance of class
    # @param string   addr     - address of r2cloud server
    # @param string   version  - version of r2cloud api (default: v1)
    # @param mixed    verify   - verify ssl cert of server (default: False) more read from httpx.get parameter verify
    def __init__(self, addr = 'https://r2server.ru/', version = 'v1', verify = True):
        self.protocol = protocol(addr, version, verify)            

    
    ## get Observation list from server of satellite
    # @param object   self      - instance of class
    # @paran str/int  sat       - satellite name / naradid
    # @return list of observationSummary obj when ok else return code
    def observation(self, sat):

        norad = sat

        req = self.protocol.apiGet("observation", params = {
            "satellite": norad
        })

        if req.status_code != 200:
            return req.status_code
        
        res = []
        for observation_entry in req.json():
            res.append(
                observation(observation_entry, self)
            )

        return res