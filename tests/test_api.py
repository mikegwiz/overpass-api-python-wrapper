# Copyright 2015-2018 Martijn van Exel.
# This file is part of the overpass-api-python-wrapper project
# which is licensed under Apache 2.0.
# See LICENSE.txt for the full license text.

import overpass
import geojson
import pickle
import os


def test_initialize_api():
    api = overpass.API()
    assert isinstance(api, overpass.API)
    assert api.debug is False


def test_geojson():
    api = overpass.API(debug=True)

    map_query = overpass.MapQuery(37.86517, -122.31851, 37.86687, -122.31635)
    osm_geo = api.get(map_query)
    assert len(osm_geo["features"]) > 1

    osm_geo = api.get("node(area:3602758138)[amenity=cafe]")
    assert len(osm_geo["features"]) > 1


def test_geojson_extended():

    class API(overpass.API):
        def _get_from_overpass(self, query):
            return pickle.load(open(os.path.join(os.path.dirname(__file__), "example.response"), "rb"))

    # The commented code should only be executed once when major changes to the Overpass API and/or to this wrapper are
    # introduced. One than has to manually verify that the date in the  example.response file from the Overpass API
    # matches the data in the example.json file generated by this wrapper.
    #
    # The reason for this approach is the following: It is not safe to make calls to the actual API in this test as the
    # API might momentarily be unavailable and the underlying data can also change at any moment. The commented code is
    # needed to create the example.response and example.json files. The example.response file is subsequently used to
    # fake the _get_from_overpass method during the tests and the example.json file is the reference that we are
    # asserting against.
    #
    # api = overpass.API()
    # osm_geo = api.get("rel(6518385);out body geom;way(10322303);out body geom;node(4927326183);", verbosity='body geom')
    # pickle.dump(api._get_from_overpass("[out:json];rel(6518385);out body geom;way(10322303);out body geom;node(4927326183);out body geom;"),
    #             open(os.path.join(os.path.dirname(__file__), "example.response"), "wb"),
    #             protocol=2)
    # geojson.dump(osm_geo, open(os.path.join(os.path.dirname(__file__), "example.json"), "w"))

    api = API()
    osm_geo = api.get("rel(6518385);out body geom;way(10322303);out body geom;node(4927326183);", verbosity='body geom')
    ref_geo = geojson.load(open(os.path.join(os.path.dirname(__file__), "example.json"), "r"))
    assert osm_geo==ref_geo
