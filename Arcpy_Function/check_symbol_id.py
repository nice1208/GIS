import arcpy
import pandas as pd 
aprx = arcpy.mp.ArcGISProject(r"C:\Users\DITZ9027\Desktop\task\Data\Data Validation Plan\display_arcade_symbolcolor\Review symbol ID\20230111 - December Config Map with UN & Non-UN Data.aprx")
m = aprx.listMaps('Merge Map FS')[0]
data1=[]
data2=[]
data3=[]
data4=[]
data5=[]
for lyr in m.listLayers():
    if lyr.supports('symbology')& lyr.supports('name'):
        renderer = lyr.symbology.renderer
        if renderer.type == 'SimpleRenderer':
            data1.append(lyr.name)
            data2.append(lyr.longName)
            data3.append('SimpleRenderer')
            data4.append('SimpleRenderer')
            data5.append('SimpleRenderer')
        elif renderer.type == 'UniqueValueRenderer':
            try:
                items = renderer.groups[0].items
                for i in items:
                    data1.append(lyr.name)
                    data2.append(lyr.longName)
                    data3.append(renderer.fields)
                    data4.append(i.values[0])
                    data5.append(i.label)
            except IndexError:
                data1.append(lyr.name)
                data2.append(lyr.longName)
                data3.append('No Symbol')
                data4.append('No Symbol')
                data5.append('No Symbol')

df = pd.DataFrame({'name':data1,'longName':data2,'fields':data3,'value':data4,'label':data5})   
        
df.to_csv (r'C:\Users\DITZ9027\Desktop\task\Data\Data Validation Plan\display_arcade_symbolcolor\Review symbol ID\symbol_id_list.csv')
