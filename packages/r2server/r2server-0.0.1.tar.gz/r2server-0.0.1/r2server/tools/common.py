#!/bin/env python
## common tools file for r2cloud SDK
# @author Lukáš Plevač <lukasplevac@gmail.com>
# @date 30.1.2021

## save binary data to file
# @param self
# @param mixed  bin  - binary data to save
# @param string file - file name 
# @return None
def bin2file(bin, file):
    file = open(file, "wb")
    file.write(bin)
    file.close()

