from geoformat_lib.conf.format_variable import value_to_iterable_value
from geoformat_lib.conversion.geometry_conversion import geometry_to_bbox
from geoformat_lib.geoprocessing.connectors.predicates import bbox_intersects_bbox


def feature_filter_geometry(feature, geometry_type_filter=None, bbox_filter=None, bbox=True):
    """
    Keeps only :
        - a certain type of geometries (beware, this function will not filter geometries inside a GeometryCollection)
        - a geometry that intersect a given bbox.

    :param feature: feature that will be filtered
    :param geometry_type_filter: Geometry(ies) type(s) that we want to keep in feature.
        If type not existing the feature is None.
    :param bbox_filter: if bbox(s) intersects features return feature. If feature not intersecting bbox function return
        None
    :return: geometry part of feature (beware this is not a feature on output but only geometry part)
    """

    if feature:
        geometry_type_filter = value_to_iterable_value(geometry_type_filter, set)
        # TODO remove when bbox will be an object
        if isinstance(bbox_filter, (list, tuple)):
            if isinstance(bbox_filter[0], (int, float)):
                bbox_filter = [bbox_filter]
        bbox_filter = value_to_iterable_value(bbox_filter, tuple)

        geometry = {}

        if 'geometry' in feature:
            if geometry_type_filter:
                if feature['geometry']['type'] in geometry_type_filter:
                    geometry = feature['geometry']
                else:
                    geometry = {}
            else:
                geometry = feature['geometry']

            if bbox_filter and geometry:
                geometry_in_bbox = False
                for bbox in bbox_filter:
                    if 'bbox' in geometry:
                        geometry_bbox = geometry['bbox']
                    else:
                        geometry_bbox = geometry_to_bbox(geometry)

                    if bbox_intersects_bbox(geometry_bbox, bbox):
                        geometry_in_bbox = True
                        break

                if geometry_in_bbox is False:
                    geometry = {}

            # if bbox option is activate we compute it
            if bbox and geometry:
                if 'bbox' not in feature['geometry']:
                    if geometry['type'] == 'GeometryCollection':
                        for geometry_in_collection in geometry['geometries']:
                            geometry_in_collection_bbox = geometry_to_bbox(geometry_in_collection)
                            if geometry_in_collection_bbox:
                                geometry_in_collection['bbox'] = geometry_in_collection_bbox

                    geometry_bbox = geometry_to_bbox(geometry)
                    if geometry_bbox:
                        geometry['bbox'] = geometry_bbox

        return geometry


def feature_filter_attributes(feature, field_name_filter=None):
    """
    Keeps (filter) only the fields specified in the variable field_name_filter

    :param feature: feature that will be filtered
    :param field_name_filter: field name that we want to keep in feature (if present in feature).
    :return: attributes part of feature (beware this is not a feature on output but only attributes part)
    """
    # initialize input
    field_name_filter = value_to_iterable_value(field_name_filter, list)

    if feature:
        # initialize output
        new_feature_attributes = {}

        if field_name_filter:

            # format field_name_filter
            field_name_filter = value_to_iterable_value(field_name_filter)

            if 'attributes' in feature:
                if field_name_filter:
                    for field_name in field_name_filter:
                        if field_name in feature["attributes"]:
                            if new_feature_attributes:
                                new_feature_attributes[field_name] = feature['attributes'][field_name]
                            else:
                                new_feature_attributes = {field_name: feature['attributes'][field_name]}
        else:
            if 'attributes' in feature:
                new_feature_attributes = feature['attributes']

        return new_feature_attributes


def feature_filter(feature, field_name_filter=None, geometry_type_filter=None, bbox_filter=None, bbox=True):
    """
    This function apply filter on "attributes" and/or "geometry"
        Attributes filter
            - field name filter

        Geometry filter
            - geometry type filter
            - bbox filter if feature geometry

    :param feature: feature that we want filter
    :param field_name_filter: field name that we want to keep in feature (if present in feature).
    :param geometry_type_filter: Geometry(ies) type(s) that we want to keep in feature.
        If type not existing the feature is None.
    :param bbox_filter: if bbox(s) intersects features return feature. If feature not intersecting bbox function return
        None
    :return: filtered feature
    """

    # initialize input variable
    # attributes
    attributes_filter = False
    field_name_filter = value_to_iterable_value(field_name_filter, output_iterable_type=list)
    if field_name_filter:
        attributes_filter = True
    # geometry
    geometry_filter = False
    geometry_type_filter = value_to_iterable_value(geometry_type_filter, output_iterable_type=set)
    bbox_filter = value_to_iterable_value(bbox_filter, output_iterable_type=tuple)
    if geometry_type_filter or bbox_filter:
        geometry_filter = True

    # initialize output variable
    new_feature = {}
    # attributes filter
    feature_attributes = feature_filter_attributes(
        feature,
        field_name_filter=field_name_filter
    )
    if feature_attributes:
        new_feature['attributes'] = feature_attributes

    # geometry filter
    feature_geometry = feature_filter_geometry(
        feature,
        geometry_type_filter=geometry_type_filter,
        bbox_filter=bbox_filter,
        bbox=bbox
    )
    if feature_geometry:
        new_feature['geometry'] = feature_geometry

    # check if feature is valid
    if attributes_filter and 'attributes' not in new_feature and 'geometry' not in new_feature:
        new_feature = None
    if new_feature and geometry_filter and 'geometry' not in new_feature:
        new_feature = None

    if new_feature:
        return new_feature
