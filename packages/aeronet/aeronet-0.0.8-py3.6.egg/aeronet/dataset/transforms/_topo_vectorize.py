from numpy import unique

from ..vector import Feature, FeatureCollection
from ._vectorize_exact import vectorize_exact
from ._vectorize import _extract_polygons
from ..raster import BandSample, BandCollectionSample
from ._topo_simplify import _topo_simplify


def topo_polygonize(sample, epsilon=0.1, properties=None, labels=None, label_name='class_id'):
    """
    makes polygonization of a multi-valued mask, where each value represents a separate class of the features


    Args:
        sample: BandSample for vectorization. It may contain multiple values, and each unique value will be vectorized
        as a separate set of features. It is intended for a multi-coloured mask, where each value corresponds to the class

        epsilon:
        properties: common properties for all the features
        labels: dict(value:label) , the properties unique for each value.
        If the labels are specified, only the corresponding values (or layers of Collection) are vectorized.
        If labels is None (default) the labels are generated for each value present in the raster
        label_name: the name (key) of the property that will contain class label. If label_name==False, the labels
        are not written to output features
    """
    if isinstance(sample, BandSample):
        raster = sample.numpy()
        values = unique(raster)
        if labels is None:
            rasters = {value: (raster == value) for value in values}
        else:
            rasters = {label: (raster == value) for label, value in labels.items() if value in values}
    elif isinstance(sample, BandCollectionSample):
        if labels is None:
            rasters = {i: band.numpy() for i, band in enumerate(sample)}
        else:
            rasters = {label: sample[value].numpy for label, value in labels.items() if value < sample.count}
    else:
        raise ValueError(f'sample must be BandSample or BandCollectionSample, got {type(sample)} instead')

    if properties is None:
        properties = {}

    features = []
    for raster, label in rasters.items():
        geoms = vectorize_exact(raster, transform=sample.transform)
        # remove all the geometries except for polygons
        polys = _extract_polygons(geoms)
        layer_props = properties
        if label_name:
            # We have an option to disable saving of the layer n`   ame to the
            layer_props[label_name] = label
        features += [Feature(geometry, properties=layer_props, crs=sample.crs)
                     for geometry in polys]

    res = FeatureCollection(features, crs=sample.crs)
    if epsilon > 0:
        res = _topo_simplify(res, epsilon*sample.res)

    return res

