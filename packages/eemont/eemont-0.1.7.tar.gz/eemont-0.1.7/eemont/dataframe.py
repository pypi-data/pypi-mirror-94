import ee
import pandas as pd
import warnings

def _extend_pdDataFrame():
    """Decorator. Extends the pd.DataFrame class."""
    return lambda f: (setattr(pd.core.frame.DataFrame,f.__name__,f) or f)

@_extend_pdDataFrame()
def toEEFeatureCollection(self,latitude = None,longitude = None):
    '''Converts a pd.DataFrame object into an ee.FeatureCollection object. If lat/lon coordinates are available, the Data Frame can be converted into a Feature Collection
    with an associated geometry.
    
    Parameters
    ----------    
    self : pd.DataFrame [this]
        Data Frame to convert into a Feature Collection.
    latitude : string
        Name of a latitude column, if available. Coupled with a longitude column, an ee.Geometry.Point is created and associated to each Feature.
    longitude : string
        Name of a longitude column, if available. Coupled with a latitude column, an ee.Geometry.Point is created and associated to each Feature.
        
    Returns
    -------    
    ee.FeatureCollection
        Data Frame converted into a Feature Collection.
    '''
    def getFeature(r):
        properties = r.to_dict()
        if latitude != None and longitude == None:
            warnings.warn("longitude missing, Feature Collection with no geometries generated!",Warning)
            return ee.Feature(None,properties)
        elif latitude == None and longitude != None:
            warnings.warn("latitude missing, Feature Collection with no geometries generated!",Warning)
            return ee.Feature(None,properties)
        elif latitude != None and longitude != None:
            point = ee.Geometry.Point([r[longitude],r[latitude]])
            return ee.Feature(point,properties)
        else:
            return ee.Feature(None,properties)

    dataFrame = self.copy()
    dataFrame['feature'] = dataFrame.apply(getFeature,axis = 1)    
    featureCollection = ee.FeatureCollection(dataFrame['feature'].tolist())

    return featureCollection