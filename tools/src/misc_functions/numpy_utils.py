import numpy as np

def multiDims(arr,newlist):
  if isinstance(arr,np.ndarray):
    if arr.ndim > 2:
      for nextarr in arr:
        newlist.append([])
        multiDims(nextarr,newlist[-1])
    elif arr.ndim == 2:
      for nextarr in arr:
        if nextarr.dtype.kind in ('U','O','S'):
          newlist.append(list(map(bytes,nextarr)))
        else:
          newlist.append(list(nextarr))
    else:
      if arr.dtype.kind in ('O','U','S'):
        newlist = list(map(bytes,arr)))
      else:
        newlist = list(arr)
    return newlist
  else:
    return arr
