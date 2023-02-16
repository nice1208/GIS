# export the in-out range report
import arcpy
import pandas as pd 
aprx = arcpy.mp.ArcGISProject('CURRENT')
data1=[]
data2=[]
data3=[]
data4=[]
for m in aprx.listMaps():
    for lyr in m.listLayers():
        if lyr.supports('name'):
            data1.append(lyr.name)
            data2.append(lyr.longName)
            data3.append(lyr.maxThreshold)
            data4.append(lyr.minThreshold)
            
df = pd.DataFrame({'name':data1,'longName':data2,'maxThreshold': data3,'minThreshold':data4})   
    
df.head()
df.to_csv (r'C:\Users\DITZ9027\Desktop\export_dataframe.csv')
del aprx
