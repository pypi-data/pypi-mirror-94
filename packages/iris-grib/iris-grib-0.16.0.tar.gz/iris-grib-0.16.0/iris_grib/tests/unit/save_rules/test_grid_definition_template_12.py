# Copyright iris-grib contributors
#
# This file is part of iris-grib and is released under the LGPL license.
# See COPYING and COPYING.LESSER in the root of the repository for full
# licensing details.
"""
Unit tests for :meth:`iris_grib._save_rules.grid_definition_template_12`.

"""

# Import iris_grib.tests first so that some things can be initialised before
# importing anything else.
import iris_grib.tests as tests

import numpy as np

import iris.coords
from iris.coord_systems import GeogCS, TransverseMercator
from iris.exceptions import TranslationError

from iris_grib._save_rules import grid_definition_template_12
from iris_grib.tests.unit.save_rules import GdtTestMixin


class FakeGribError(Exception):
    pass


class Test(tests.IrisGribTest, GdtTestMixin):
    def setUp(self):
        self.default_ellipsoid = GeogCS(semi_major_axis=6377563.396,
                                        semi_minor_axis=6356256.909)
        self.test_cube = self._make_test_cube()

        GdtTestMixin.setUp(self)

    def _make_test_cube(self, cs=None, x_points=None, y_points=None):
        # Create a cube with given properties, or minimal defaults.
        if cs is None:
            cs = self._default_coord_system()
        if x_points is None:
            x_points = self._default_x_points()
        if y_points is None:
            y_points = self._default_y_points()

        x_coord = iris.coords.DimCoord(x_points, 'projection_x_coordinate',
                                       units='m', coord_system=cs)
        y_coord = iris.coords.DimCoord(y_points, 'projection_y_coordinate',
                                       units='m', coord_system=cs)
        test_cube = iris.cube.Cube(np.zeros((len(y_points), len(x_points))))
        test_cube.add_dim_coord(y_coord, 0)
        test_cube.add_dim_coord(x_coord, 1)
        return test_cube

    def _default_coord_system(self):
        # This defines an OSGB coord system.
        cs = TransverseMercator(latitude_of_projection_origin=49.0,
                                longitude_of_central_meridian=-2.0,
                                false_easting=400000.0,
                                false_northing=-100000.0,
                                scale_factor_at_central_meridian=0.9996012717,
                                ellipsoid=self.default_ellipsoid)
        return cs

    def test__template_number(self):
        grid_definition_template_12(self.test_cube, self.mock_grib)
        self._check_key('gridDefinitionTemplateNumber', 12)

    def test__shape_of_earth(self):
        grid_definition_template_12(self.test_cube, self.mock_grib)
        self._check_key('shapeOfTheEarth', 7)
        self._check_key('scaleFactorOfEarthMajorAxis', 0)
        self._check_key('scaledValueOfEarthMajorAxis', 6377563.396)
        self._check_key('scaleFactorOfEarthMinorAxis', 0)
        self._check_key('scaledValueOfEarthMinorAxis', 6356256.909)

    def test__grid_shape(self):
        test_cube = self._make_test_cube(x_points=np.arange(13),
                                         y_points=np.arange(6))
        grid_definition_template_12(test_cube, self.mock_grib)
        self._check_key('Ni', 13)
        self._check_key('Nj', 6)

    def test__grid_points_exact(self):
        test_cube = self._make_test_cube(x_points=[1, 3, 5, 7],
                                         y_points=[4, 9])
        grid_definition_template_12(test_cube, self.mock_grib)
        self._check_key("X1", 100)
        self._check_key("X2", 700)
        self._check_key("Y1", 400)
        self._check_key("Y2", 900)
        self._check_key("Di", 200)
        self._check_key("Dj", 500)

    def test__grid_points_approx(self):
        test_cube = self._make_test_cube(x_points=[1.001, 3.003, 5.005, 7.007],
                                         y_points=[4, 9])
        grid_definition_template_12(test_cube, self.mock_grib)
        self._check_key("X1", 100)
        self._check_key("X2", 701)
        self._check_key("Y1", 400)
        self._check_key("Y2", 900)
        self._check_key("Di", 200)
        self._check_key("Dj", 500)

    def test__negative_grid_points_gribapi_broken(self):
        self.mock_gribapi.GribInternalError = FakeGribError

        # Force the test to run the signed int --> unsigned int workaround.
        def set(grib, key, value):
            if key in ["X1", "X2", "Y1", "Y2"] and value < 0:
                raise self.mock_gribapi.GribInternalError()
            grib.keys[key] = value
        self.mock_gribapi.grib_set = set

        test_cube = self._make_test_cube(x_points=[-1, 1, 3, 5, 7],
                                         y_points=[-4, 9])
        grid_definition_template_12(test_cube, self.mock_grib)
        self._check_key("X1", 0x80000064)
        self._check_key("X2", 700)
        self._check_key("Y1", 0x80000190)
        self._check_key("Y2", 900)

    def test__negative_grid_points_gribapi_fixed(self):
        test_cube = self._make_test_cube(x_points=[-1, 1, 3, 5, 7],
                                         y_points=[-4, 9])
        grid_definition_template_12(test_cube, self.mock_grib)
        self._check_key("X1", -100)
        self._check_key("X2", 700)
        self._check_key("Y1", -400)
        self._check_key("Y2", 900)

    def test__template_specifics(self):
        grid_definition_template_12(self.test_cube, self.mock_grib)
        self._check_key("latitudeOfReferencePoint", 49000000.0)
        self._check_key("longitudeOfReferencePoint", -2000000.0)
        self._check_key("XR", 40000000.0)
        self._check_key("YR", -10000000.0)

    def test__scale_factor_gribapi_broken(self):
        # GRIBAPI expects a signed int for scaleFactorAtReferencePoint
        # but it should accept a float, so work around this.
        # See https://software.ecmwf.int/issues/browse/SUP-1100

        def get_native_type(grib, key):
            assert key == "scaleFactorAtReferencePoint"
            return int
        self.mock_gribapi.grib_get_native_type = get_native_type
        grid_definition_template_12(self.test_cube, self.mock_grib)
        self._check_key("scaleFactorAtReferencePoint", 1065346526)

    def test__scale_factor_gribapi_fixed(self):

        def get_native_type(grib, key):
            assert key == "scaleFactorAtReferencePoint"
            return float
        self.mock_gribapi.grib_get_native_type = get_native_type
        grid_definition_template_12(self.test_cube, self.mock_grib)
        self._check_key("scaleFactorAtReferencePoint", 0.9996012717)

    def test__scanmode(self):
        grid_definition_template_12(self.test_cube, self.mock_grib)
        self._check_key('iScansPositively', 1)
        self._check_key('jScansPositively', 1)

    def test__scanmode_reverse(self):
        test_cube = self._make_test_cube(x_points=np.arange(7, 0, -1))
        grid_definition_template_12(test_cube, self.mock_grib)
        self._check_key('iScansPositively', 0)
        self._check_key('jScansPositively', 1)


if __name__ == "__main__":
    tests.main()
