#Find the count of multi-part features in the layer
import arcpy

aprx = arcpy.mp.ArcGISProject('CURRENT')
multiparts = []
nonetype = []
row_count = 0
for m in aprx.listMaps():
    for lyr in m.listLayers():
        if lyr.longName == "Map\Map Network\Structure\Structure Boundary\Building":
            fc_name = lyr
            for row in arcpy.da.SearchCursor(fc_name, ["OID@", "SHAPE@"]):
                row_count += 1
                if row[1] is None:
                    print("{0} has issue with NoneType".format(row[0]))
                    nonetype.append(row[0])
                elif row[1].isMultipart is True:
                    multiparts.append(row[0])

            print("Nonetypes (Zero length typically):")
            print(nonetype)
            
            print("Multi-part OID:")
            print(multiparts)
            print("There are {0} multi-part feature(s) in {1} with {2} features".format(len(multiparts), fc_name, row_count))
