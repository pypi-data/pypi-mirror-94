# Copyright iris-grib contributors
#
# This file is part of iris-grib and is released under the LGPL license.
# See COPYING and COPYING.LESSER in the root of the repository for full
# licensing details.
"""
Test function :func:`iris_grib._load_convert.product_definition_template_11`.

"""

# import iris_grib.tests first so that some things can be initialised
# before importing anything else.
import iris_grib.tests as tests

from copy import deepcopy
from unittest import mock
import warnings

from iris.coords import DimCoord, CellMethod

from iris_grib._load_convert import product_definition_template_11


class Test(tests.IrisGribTest):
    def setUp(self):
        def func(s, m, f):
            return m['cell_methods'].append(self.cell_method)

        module = 'iris_grib._load_convert'
        self.patch('warnings.warn')
        this_module = '{}.product_definition_template_11'.format(module)
        self.cell_method = mock.sentinel.cell_method
        self.patch(this_module, side_effect=func)
        self.patch_statistical_fp_coord = self.patch(
            module + '.statistical_forecast_period_coord',
            return_value=mock.sentinel.dummy_fp_coord)
        self.patch_time_coord = self.patch(
            module + '.validity_time_coord',
            return_value=mock.sentinel.dummy_time_coord)
        self.patch_vertical_coords = self.patch(module + '.vertical_coords')
        self.metadata = {'factories': [], 'references': [],
                         'standard_name': None,
                         'long_name': None, 'units': None, 'attributes': {},
                         'cell_methods': [], 'dim_coords_and_dims': [],
                         'aux_coords_and_dims': []}

    def _check(self, request_warning):
        grib_lconv_opt = 'iris_grib._load_convert.options'
        with mock.patch(grib_lconv_opt, warn_on_unsupported=request_warning):
            metadata = deepcopy(self.metadata)
            perturbationNumber = 666
            section = {'productDefinitionTemplateNumber': 11,
                       'perturbationNumber': perturbationNumber,
                       'hoursAfterDataCutoff': 1,
                       'minutesAfterDataCutoff': 1,
                       'numberOfTimeRange': 1,
                       'typeOfStatisticalProcessing': 1,
                       'typeOfTimeIncrement': 2,
                       'timeIncrement': 0,
                       'yearOfEndOfOverallTimeInterval': 2000,
                       'monthOfEndOfOverallTimeInterval': 1,
                       'dayOfEndOfOverallTimeInterval': 1,
                       'hourOfEndOfOverallTimeInterval': 1,
                       'minuteOfEndOfOverallTimeInterval': 0,
                       'secondOfEndOfOverallTimeInterval': 1}
            forecast_reference_time = mock.Mock()
            # The called being tested.
            product_definition_template_11(section, metadata,
                                           forecast_reference_time)
            expected = {'cell_methods': [], 'aux_coords_and_dims': []}
            expected['cell_methods'].append(CellMethod(method='sum',
                                                       coords=('time',)))
            realization = DimCoord(perturbationNumber,
                                   standard_name='realization',
                                   units='no_unit')
            expected['aux_coords_and_dims'].append((realization, None))
            self.maxDiff = None
            self.assertEqual(metadata['aux_coords_and_dims'][-1],
                             expected['aux_coords_and_dims'][0])
            self.assertEqual(metadata['cell_methods'][-1],
                             expected['cell_methods'][0])

            if request_warning:
                warn_msgs = [mcall[1][0] for mcall in warnings.warn.mock_calls]
                expected_msgs = ['type of ensemble', 'number of forecasts']
                for emsg in expected_msgs:
                    matches = [wmsg for wmsg in warn_msgs if emsg in wmsg]
                    self.assertEqual(len(matches), 1)
                    warn_msgs.remove(matches[0])
            else:
                self.assertEqual(len(warnings.warn.mock_calls), 0)

    def test_pdt_no_warn(self):
        self._check(False)

    def test_pdt_warn(self):
        self._check(True)


if __name__ == '__main__':
    tests.main()
