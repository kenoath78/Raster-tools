from osgeo import gdal, osr
import os

def check_raster(raster):
    raster.replace("\\","/")
    # Check if path and file exist
    if os.path.exists(raster) is False:
        raise Exception('No such file or directory: \'' + raster +'\'')
    ds = gdal.Open(raster, gdal.GA_ReadOnly)
    # Check if file is valid
    if ds == None:
        raise Exception('Unable to read the data file or incorrect file type: \'' + raster +'\'')
    else:
        print("Valid raster: {0}".format(raster))
    # Check projection validity
    Projection  = osr.SpatialReference()
    Projection.ImportFromWkt(ds.GetProjectionRef())
    Projcs = Projection.GetAttrValue('PROJCS', 0)
    Projcs_unit = Projection.GetAttrValue('UNIT', 0)
    epsg = int(Projection.GetAttrValue('AUTHORITY', 1))
    if Projcs == None:
        if epsg == None:
            print("File name: {0}\nInvalid Projection and EPSG")
        else:
            print("Invalid Projection\nEPSG: {0}".format(epsg))
    else:
        print("Projection: {0}\nProjection units: {1}\nEPSG: {2}".format(Projcs, Projcs_unit, epsg))
    # Check number of bands
    bands= ds.RasterCount
    print("Number of bands: {0}\n".format(bands))
    ds=None

def compile_df_fields(df,csv_dictionary):
    csv_dict=pd.read_csv(csv_dictionary)
    dict_df=dict(zip(csv_dict.FIELDNAME, csv_dict[csv_dict.columns[1:]].values.tolist()))
    for fieldname_,fieldlist in zip(list(dict_df.keys()),list(dict_df.values())):
        fieldlist=[field for field in fieldlist if str(field)!='nan']
        fieldname_=str('c'+fieldname_)
        df[fieldname_]=pd.NA
        for field in fieldlist:
            df.loc[df[fieldname_].isna(), fieldname_]=df[field]
    column_list=[col for col in df.columns.values.tolist() if str(col).startswith('c')]
    df=df[column_list]
    df=df.rename(columns=lambda column: column.lstrip('c'))
    return df
