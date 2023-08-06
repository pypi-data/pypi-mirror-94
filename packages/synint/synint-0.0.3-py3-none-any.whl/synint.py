import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import *
from decimal import Decimal

def SynInt(Y,s):
  C = []
  SI = []
  Ix = []
  gradient = []
  lY = len(Y)
  sVal = s
  for i in list(range(0,lY-s)):
    A = Y[i:(i+(s))].mean()
    B = Y[(i+s):(i+2*s)].mean()
    DY = (B-A)
    Indx = i+s
    Ix.append(Indx)
    C.append(DY)
    SI.append(np.sum(C))
  bVal = Y[int(np.floor(.5*s)):int(np.ceil(1.5*s))].mean()
  mVal = 1/s
  trIter = 10000
  j = 0
  Dm_hold = 1
  direction = 1
  reduction = 100
  for i in range(trIter): 
    SIm = SI[0:lY]
    SIm = np.multiply(SIm,mVal)
    SIm = list(map(lambda x: x + bVal, SIm))
    e = np.subtract(Y[(s):(lY)],SIm[0:lY])
    e = np.power(e,2)
    sum_error = np.sum(e)
    Dm = (2/lY)*sum_error
    if np.abs(reduction) < .000001:
      break
    reduction = np.abs(Dm_hold) - np.abs(Dm)
    if reduction < 0:
      direction = -direction
      j = j+i      
    bVal1 = bVal - (bVal*(1/(2*j+2)))*direction
    Dm_hold = Dm
    bVal = bVal1
    gradient.append(Dm)
  SI = np.multiply(SI,mVal) + bVal
  SD = np.multiply(C,mVal)
  return(SI,SD,Ix,sVal,bVal)

def SIproject(SI,SD,Ixn,s):
  bookmark = len(Ixn)
  (SDa,SDDb,IDx,sVala,bValb) = SynInt(SD,s)
  DVmin = 2*SDa.min()
  DVmax = 2*SDa.max()
  reverse = 0
  tail = len(SDa)-2*s
  if tail < 0:
    tail = 0
  vDelta = SDa[tail:len(SDa)-2].mean()
  DV1 = SDa[len(SDa)-1]
  DvM = (DV1-vDelta)/s
  Ixlast = Ixn[len(Ixn)-1]
  SIproj = []
  SDproj = []
  prpoints = []
  sdpoints = []
  for p in list(range(0,ceil(s+1))):
    IxAppend = Ixlast+p
    if p == 0:
      proj = SI[len(SI)-1]
      sdm = DV1
    elif (lastSD <= DVmax and lastSD >= DVmin) and reverse == 0:   
      sdm = p*DvM + DV1
      proj = proj+sdm
    elif reverse == 1:
      sdm = -1 * np.abs(DvM) + lastSD
      proj = proj+sdm
    elif reverse == -1:
      sdm = np.abs(DvM) + lastSD
      proj = proj+sdm   
    SIproj.append(proj)
    SDproj.append(sdm)
    Ixn.append(IxAppend)
    prpoints.append(proj)
    sdpoints.append(sdm)
    lastSD = SDproj[len(SDproj)-1]
    if lastSD > DVmax:
        reverse = 1
    if lastSD < DVmin:
        reverse = -1
        
  SI = np.concatenate((SI, SIproj), axis=0)
  SD = np.concatenate((SD,SDproj), axis = 0)
  IxO = Ixn[0:bookmark]
  return (SI,SD,Ixn,IxO)

def SIforecast(Y_series,FClen,tail_length,spec_index = "auto"):
  Y = np.array(Y_series).reshape(len(Y_series))
  projDatanp = np.empty((0,3), int)
  integrals = list(range(3,(FClen+3),1))
  iter = len(integrals)
  #printout
  maxpcount = len(Y) - spec_index
  pctcomplete = 10
  totalpoints = int(FClen * ((maxpcount*(maxpcount+1))/2))
  print(str(FClen) + "-step forecast with " + str(maxpcount) + " historic data points requested.")
  print("Now forecasting " + str(totalpoints) + " surface points to extrapolate " + str(maxpcount * FClen) + " outcomes:")
  print("Starting job...")
  print(" 0%  -x-")
  for itr in list(range(0,iter)):
    pcstep = (100 * (((itr+1)*maxpcount)/(maxpcount * FClen)))
    if pcstep > pctcomplete:
      print(str(pctcomplete)+"%   V")
      pctcomplete = pctcomplete + 10
    SIlast = []
    castnum = []
    indexP = []
    s = integrals[itr]
    (SI,SD,Ix,sVal,bVal) = SynInt(Y,s)
    maxLength = len(SI)-1
    for step in list(range((spec_index),(maxLength+1),1)):
      stepIndex = step
      if spec_index == 0:
        tail_length = 0      
      (SIa,SDa,Ixna,IxOa) = SIproject(SI[(stepIndex-tail_length):stepIndex],SD[(stepIndex-tail_length):stepIndex],Ix[(stepIndex-tail_length):stepIndex],s)
      SIlast.append(SIa[len(SIa)-1])
      endpoint = np.array(SIlast)
      indexP.append(Ixna[len(Ixna)-1])
      castnum.append(s)
      projDataStep = np.array((indexP, endpoint,castnum)).transpose()
    projDatanp = np.concatenate((projDatanp, projDataStep), axis=0)
  projData = pd.DataFrame(projDatanp)
  print("100% >X<")
  print("Surface complete.")
  return(projData)

def aggProcess(projData,tdata,FClen):
  print("Flattening...")
  shotframe = projData
  indices = projData['index'].unique()
  dimension = list(range(0,len(indices)))

  index_f = []
  cindex = []
  pvals = []
  forecast = []
  upperbound = []
  lowerbound = []
  mprojection = []
  xincr = 1

  for i in dimension:
    stepshots = shotframe.loc[shotframe['index'] == indices[i]]
    maxstep = np.max(stepshots['synInt'])
    minstep = np.min(stepshots['synInt'])
    avgstep = np.mean(stepshots['synInt'])
    countindex = len(stepshots['synInt'])
    try:
      tsval = tdata['sdata'].loc[tdata['index_a'] == indices[i]].values[0]
      pval = len(stepshots['synInt'].loc[stepshots['synInt'] < tsval].values)/countindex
    except:
      xincr = xincr + 1/(10*FClen)
      pval = .5 - (.5 - pval)/(xincr)
    fcast = stepshots['synInt'].quantile(pval)

    index_f.append(indices[i])
    cindex.append(countindex)
    pvals.append(pval)
    forecast.append(fcast)
    upperbound.append(maxstep)
    lowerbound.append(minstep)
    mprojection.append(avgstep)

  DataStep = np.array((index_f,cindex,pvals,forecast,upperbound,lowerbound,mprojection)).transpose()

  aggdata = pd.DataFrame(DataStep)
  aggdata = aggdata.rename(columns={0: "index_f", 1: "cindex", 2: "pval",3:"forecast",4:"upperbound",5:"lowerbound",6:"mprojection"})
  print("Forecast aggregation complete.")
  return aggdata

def generate_forecast(df,FClen,preview = 'false'):
  tdata = df.toPandas()
  tdata['index_a'] = np.arange(tdata.shape[0]) + 1
  Y_series = df.select("sdata").collect()
  tail = (2*FClen)
  start = len(Y_series)-tail - 10
  projData = SIforecast(Y_series,FClen,tail,start)
  projData.columns = ["index","synInt","stepnum"]
  aggdata = aggProcess(projData,tdata,FClen)
  if preview == 'true':
    xrng = len(tdata['index_a'])-2*FClen-10
    plt.style.use('default')
    fig = plt.figure()
    ax2 = fig.add_subplot(111)
    ax2.plot(aggdata['index_f'],aggdata['upperbound'],color = "whitesmoke",linestyle=":", linewidth = 2)
    ax2.plot(aggdata['index_f'],aggdata['lowerbound'],color = "whitesmoke",linestyle=":", linewidth = 2)
    ax2.plot(aggdata['index_f'],aggdata['mprojection'],color = "orange", linewidth = 2)
    ax2.plot(aggdata['index_f'],aggdata['forecast'],color = "black", linewidth = 2)
    ax2.plot(tdata['index_a'][xrng:],tdata['sdata'][xrng:],color = "red", linewidth = 2)
  return (tdata,aggdata)