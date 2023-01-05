import arcpy
import sys
import pandas as pd
import datetime
from multiprocessing import Pool

# Usage
# "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" C:\Users\DITZ9027\Desktop\Python code\vscode\Test.py C:\Users\DITZ9027\Desktop\Python code\vscode\TO_RPA\validate_graphic_sample_check_16_12_2022.xlsx 5

def export_PDF_self(x_coordinate, y_coordinate, x2_coordinate, y2_coordinate, zoom_level, layer_config_file_path, map_type, layers, check_id, fid, geometry):
    start_time = datetime.datetime.now()
    if  x2_coordinate == -99999.0:
        print('Start Exporting (' + str(x_coordinate) + ', ' + str(y_coordinate) + ') Zoom ' + str(zoom_level) + ' ' + str(start_time) + '...')
    else:
        print('Start Exporting (' + str(x_coordinate) + ', ' + str(y_coordinate) + ') to (' + str(x2_coordinate) + ', ' + str(y2_coordinate) + ') Zoom ' + str(zoom_level) + ' ' + str(start_time) + '...')

    if map_type == 'Map':
        arcpy.env.referenceScale = "100"
        aprx = arcpy.mp.ArcGISProject(r'C:\Users\DITZ9027\Desktop\Python code\vscode\exportToPDFmap.aprx')
        m = aprx.listMaps("Merge Map FS11")[0]
    elif map_type == 'Schematics':
        arcpy.env.referenceScale = "30"
        aprx = arcpy.mp.ArcGISProject(r'C:\Users\DITZ9027\Desktop\Python code\vscode\exportToPDFsch.aprx')
        m = aprx.listMaps("Merge Map FS11")[0]
    # On/Off Layers
    if layer_config_file_path:
        df1 = pd.read_csv(layer_config_file_path)
        for m in aprx.listMaps("Merge Map FS11"):
            for lyr in m.listLayers():
                temp_df = df1
                if len(temp_df.loc[(temp_df['name'].isin(layers)) & (temp_df['longName'] == lyr.longName)].index) > 0:
                    lyr.visible = True
    aprxLayout = aprx.listLayouts("Layout")[0]
    mf = aprxLayout.listElements("mapframe_element", "Map Frame")[0]
    new_Extent = mf.camera.getExtent()
    #x_coordinate = 835368.59
    #y_coordinate = 815220.63
    if  x2_coordinate == -99999.0:
        new_Extent.XMin = x_coordinate - 84.2824387085
        new_Extent.YMin = y_coordinate - 58.99461726475
        new_Extent.XMax = x_coordinate + 84.2824387085
        new_Extent.YMax = y_coordinate + 58.99461726475
    else:
        new_Extent.XMin = x_coordinate
        new_Extent.YMin = y_coordinate
        new_Extent.XMax = x2_coordinate
        new_Extent.YMax = y2_coordinate
    mf.camera.setExtent(new_Extent)
    mf.camera.scale = zoom_level
    m.defaultCamera = mf.camera
    date_time_now = datetime.datetime.now()
    check_id_for_file_name = ''
    if len(check_id) == 1:
        check_id_for_file_name = f'000{check_id}'
    elif len(check_id) == 2:
        check_id_for_file_name = f'00{check_id}'
    elif len(check_id) == 3:
        check_id_for_file_name = f'0{check_id}'
    elif len(check_id) == 4:
        check_id_for_file_name = check_id
    aprxLayout.exportToPDF(rf'C:\Users\DITZ9027\Desktop\Python code\vscode\2023_01_03_fid1\{check_id_for_file_name}-{fid}-{map_type}-{geometry}-{str(date_time_now.year) + str(date_time_now.month) + str(date_time_now.day) + str(date_time_now.hour) + str(date_time_now.minute) + str(date_time_now.second)}-ArcGISPro.pdf', 300, "BEST", True, "NONE", True, "LAYERS_AND_ATTRIBUTES")
    if  x2_coordinate == -99999.0:
        print('Finish Exporting (' + str(x_coordinate) + ', ' + str(y_coordinate) + ') Zoom ' + str(zoom_level) + ' ' + str(date_time_now) + '.')
        print('Duration for (' + str(x_coordinate) + ', ' + str(y_coordinate) + ') Zoom ' + str(zoom_level) + ' ' + str((date_time_now - start_time).total_seconds()) + '.')
    else:
        print('Finish Exporting (' + str(x_coordinate) + ', ' + str(y_coordinate) + ') to (' + str(x2_coordinate) + ', ' + str(y2_coordinate) + ') Zoom ' + str(zoom_level) + ' ' + str(date_time_now) + '.')
        print('Duration for (' + str(x_coordinate) + ', ' + str(y_coordinate) + ') to (' + str(x2_coordinate) + ', ' + str(y2_coordinate) + ') Zoom ' + str(zoom_level) + ' ' + str((date_time_now - start_time).total_seconds()) + '.')
# r'C:\RPA_DEV\P000-NHGISHealthCheck\PDF\2022-12-07\Exported_PDF_' + str(x_coordinate) + r'_' + str(y_coordinate) + r'_' + str(zoom_level) + r'_' + str(date_time_now.year) + str(date_time_now.month) + str(date_time_now.day) + str(date_time_now.hour) + str(date_time_now.minute) + str(date_time_now.second) + r'.pdf'
# aprxLayout.exportToPDF(r'C:\RPA_DEV\P000-NHGISHealthCheck\PDF\2022-12-07\Exported_PDF_' + str(x_coordinate) + r'_' + str(y_coordinate) + r'_' + str(x2_coordinate) + r'_' + str(y2_coordinate) + r'_' + str(zoom_level) + r'_' + str(date_time_now.year) + str(date_time_now.month) + str(date_time_now.day) + str(date_time_now.hour) + str(date_time_now.minute) + str(date_time_now.second) + r'.pdf', 300, "BEST", True, "NONE", True, "LAYERS_AND_ATTRIBUTES")

if __name__ == "__main__":
    df = pd.read_excel(r"C:\Users\DITZ9027\Desktop\Python code\vscode\TO_RPA\validate_graphic_sample_check_23_12_2022.xlsx", sheet_name='feature_sample')
    pool = Pool(processes=5)
    for index, row in df.iterrows():
        if not (pd.isna(row['X1']) or pd.isna(row['Y1']) or pd.isna(row['Zoom level '])  or pd.isna(row['DOMAIN'])):
            layer_list = [row['Layer1'], row['Layer2'], row['Layer3'], row['Layer4'], row['Layer5'], row['Layer6'], row['Layer7'], row['Layer8'], row['Layer9']]
            if not (pd.isna(row['X2']) or pd.isna(row['Y2'])):
                pool.apply_async(export_PDF_self, args=(row['X1'], row['Y1'], row['X2'], row['Y2'], int(str(row['Zoom level ']).split('.', 1)[0]), r'C:\Users\DITZ9027\Desktop\Python code\vscode\layerlist_16_12_2022.csv', row['DOMAIN'], layer_list, str(row['Check ID']).split('.', 1)[0], str(row['FID']).split('.', 1)[0], row['Geometry']))
            else:
                pool.apply_async(export_PDF_self, args=(row['X1'], row['Y1'], -99999.0, -99999.0, int(str(row['Zoom level ']).split('.', 1)[0]), r'C:\Users\DITZ9027\Desktop\Python code\vscode\layerlist_16_12_2022.csv', row['DOMAIN'], layer_list, str(row['Check ID']).split('.', 1)[0], str(row['FID']).split('.', 1)[0], row['Geometry']))
    pool.close()
    pool.join()
