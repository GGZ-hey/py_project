from numpy import *
import urllib
import json


def loadDataSet(filename):
    dataMat=[]
    fr=open('test.txt')
    for line in fr.readlines():
        curLine=line.strip().split('\t')
        fltLine=list(map(float,curLine))
        dataMat.append(fltLine)
    return dataMat

def distEclud(vecA,vecB):
    return sqrt(sum(power(vecA-vecB,2)))

def randCent(dataSet,k):
    n=shape(dataSet)[1]
    centroids=mat(zeros((k,n)))
    for i in range(n):
        minX=min(dataSet[:,i])
        rangee=float(max(dataSet[:,i])-minX)
        centroids[:,i]=minX+rangee*random.rand(k,1)
    return centroids


def kMeans(dataSet,k,distMeans=distEclud,createCent=randCent):
    m=shape(dataSet)[0]
    centroids=createCent(dataSet,k)
    AssessVect=mat(zeros((m,2)))
    clusterChanged=True
    while clusterChanged:
        clusterChanged=False
        for i in range(m):
            MinDist=Inf;MinIndex=-1
            for j in range(k):
                Edist=distMeans(dataSet[i,:],centroids[j,:])
                if Edist<MinDist:
                    MinDist=Edist;MinIndex=j
            if AssessVect[i,0]!=MinIndex:
                clusterChanged=True
            AssessVect[i,:]=MinIndex,MinDist**2
        print(centroids)
        for cent in range(k):
            Same=dataSet[nonzero(AssessVect[:,0].A==cent)[0],:]#同一类元素
            centroids[cent,:]=mean(Same,axis=0)
    return centroids,AssessVect



def biKmeans(dataSet,k,distMeans=distEclud):
    m=shape(dataSet)[0]
    AssessVect=mat(zeros((m,2)))
    centroid0=mean(dataSet,axis=0)
    centroids=[centroid0]
    for i in range(m):
        AssessVect[i,1]=distMeans(centroid0,dataSet[i,:])
    while(len(centroids)<k):
        Min_SSE=Inf
        for i in range(len(centroids)):
            PresentICluster=dataSet[nonzero(AssessVect[:,0].A==i)[0],:]
            if(PresentICluster.any()):
                PresentCentroids,PresentAsseV=kMeans(PresentICluster,2,distMeans)
            else:continue
            SSE=sum(PresentAsseV[:,1])
            SSE_Not=sum(AssessVect[nonzero(AssessVect[:,0].A!=i)[0],1])
            if(SSE+SSE_Not<Min_SSE):
                best_centroids=PresentCentroids
                bestCluster=i
                Assess_copy=PresentAsseV.copy()
                Min_SSE=SSE+SSE_Not
        Assess_copy[nonzero(Assess_copy[:,0].A==1)[0],0]=len(centroids)#顺序不能错
        Assess_copy[nonzero(Assess_copy[:,0].A==0)[0],0]=bestCluster #顺序！！
        centroids[bestCluster]=best_centroids[0,:].tolist()[0]
        centroids.append(best_centroids[1,:].tolist()[0])
        AssessVect[nonzero(AssessVect[:,0].A==bestCluster)[0],:]=Assess_copy
    return mat(centroids),AssessVect

def geoGrab(stAddress,city):
    apiStem='http://where.yahooapis.com/geocode?'
    params={}
    params['flags']='J'
    params['appid']='aaa0VN6k'
    params['location']='%s %s'
    url_params=urllib.urlencode(params)
