import numpy
import os
from fepydas.datatypes.Dataset import Spectrum, PLE, SpectrumSeries
from fepydas.constructors.datareaders.Generic import ASCII
from fepydas.datatypes.Data import Data1D, Data2D, Data3D, DataType
import fepydas.datatypes as datatypes

def Automatic(filename):
  file = open(filename)
  done = False
  headers = {}
  while not done:
    line = file.readline().strip().split(" = ")
    #print(line)
    if line[0]=="HEADER":
      done = True
    else:
      headers[line[0]] = line[1:]
  
  names = file.readline().strip().split("\t")
  units = file.readline().strip().split("\t")
  length = len(headers)+3
  file.close()
  data = ASCII(filename, skip_header=length).T
  axis = Data1D(data[0,:],DataType(names[0],units[0]))
  if headers["Measurement Type"][0] == "Series":
    #2D
    values = Data2D(data[2:,:],datatypes.COUNTS)
    if headers["Measurement Type"][1] == "PLE Xe Arc Lamp":
      dtype = DataType("Excitation Wavelength","nm")
    else:
      dtype = datatypes.NUMBER
    keys = Data1D(numpy.array(names[2:2+values.values.shape[0]]).astype(numpy.float),dtype)
    
    if headers["Measurement Type"][1] == "PLE Xe Arc Lamp":
      return PLE(axis,keys,values,None,None)
    else:
      return SpectrumSeries(axis,keys,values)
  elif headers["Measurement Type"][0] == "PLE Response":
    values = Data1D(data[1,:],DataType(names[1],units[1]))
    return Spectrum(axis, values)
  else:
    #1D
    values = Data1D(data[2,:],datatypes.COUNTS)
    return Spectrum(axis, values)
