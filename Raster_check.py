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
    # Check for valid projection
    Projection  = osr.SpatialReference()
    Projection.ImportFromWkt(ds.GetProjectionRef())
    Projcs = Projection.GetAttrValue('PROJCS', 0)
    Projcs_unit = Projection.GetAttrValue('UNIT', 0)
    epsg = int(Projection.GetAttrValue('AUTHORITY', 1))
    bands = ds.RasterCount
    ds = None
    if Projcs == None:
        if epsg == None:
            print("File name: {0}\nInvalid Projection and EPSG")
        else:
            print("Invalid Projection\nEPSG: {0}".format(epsg))
    else:
        print("Projection: {0}\nProjection units: {1}\nEPSG: {2}".format(Projcs, Projcs_unit, epsg))
    print("Number of bands: {0}\n".format(bands))
