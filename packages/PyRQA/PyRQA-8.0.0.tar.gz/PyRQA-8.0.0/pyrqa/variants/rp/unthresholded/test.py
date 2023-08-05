#!/usr/bin/env python

"""
Testing recurrence plot implementations according to the unthresholded neighbourhood condition.
"""

import numpy as np
import unittest

from pyrqa.exceptions import NoMatchingVariantException
from pyrqa.neighbourhood import Unthresholded
from pyrqa.selector import SingleSelector
from pyrqa.time_series import EmbeddedSeries
from pyrqa.variants.rp.unthresholded.baseline import Baseline
from pyrqa.variants.rp.unthresholded.engine import Engine

from pyrqa.variants.rp.radius.test import RPClassicFixedRadiusTimeSeriesTestCase, \
    RPCrossFixedRadiusTimeSeriesTestCase

from pyrqa.variants.rp.unthresholded.column_no_overlap_materialisation_float import \
    ColumnNoOverlapMaterialisationFloat
from pyrqa.variants.rp.unthresholded.column_overlap_materialisation_float import \
    ColumnOverlapMaterialisationFloat
from pyrqa.variants.rp.unthresholded.row_no_overlap_materialisation_float import \
    RowNoOverlapMaterialisationFloat

VARIANTS = (ColumnNoOverlapMaterialisationFloat,
            ColumnOverlapMaterialisationFloat,
            RowNoOverlapMaterialisationFloat)

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2021 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


class RPClassicUnthresholdedTimeSeriesTestCase(RPClassicFixedRadiusTimeSeriesTestCase):
    """
    Tests for RP, Classic, Unthresholded, Time Series.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood: Unthresholded neighbourhood condition.
        """
        cls.neighbourhood = Unthresholded()

    def perform_recurrence_analysis_computations(self,
                                                 settings,
                                                 opencl=None,
                                                 verbose=False,
                                                 edge_length=None,
                                                 selector=SingleSelector(),
                                                 variants_kwargs=None,
                                                 all_variants=False):
        if opencl:
            opencl.reset()

        baseline = Baseline(settings,
                            verbose=verbose)

        result_baseline = baseline.run()

        if all_variants:
            execution_engine = Engine(settings,
                                      opencl=opencl,
                                      verbose=False,
                                      edge_length=edge_length,
                                      selector=selector,
                                      variants=VARIANTS,
                                      variants_kwargs=variants_kwargs)

            result = execution_engine.run()

            self.compare_unthresholded_recurrence_plot_results(result_baseline,
                                                               result)
        else:
            for variant in VARIANTS:
                try:
                    execution_engine = Engine(settings,
                                              opencl=opencl,
                                              verbose=False,
                                              edge_length=edge_length,
                                              selector=selector,
                                              variants=(variant,),
                                              variants_kwargs=variants_kwargs)

                    result = execution_engine.run()

                    self.compare_unthresholded_recurrence_plot_results(result_baseline,
                                                                       result,
                                                                       variant=variant)
                except NoMatchingVariantException:
                    continue


class RPClassicUnthresholdedEmbeddedSeriesTestCase(RPClassicUnthresholdedTimeSeriesTestCase):
    """
    Tests for RP, Classic, Unthresholded, Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series: Embedded series comprising vectors consisting of random floating point values.
        """
        embedding_dimension = np.random.randint(1, 10)

        cls.time_series = EmbeddedSeries(np.array([np.random.rand(embedding_dimension) for _ in np.arange(cls.time_series_length)]))

    def test_embedding_parameters(self):
        """
        Test using different than the default recurrence analysis settings.
        """
        pass


class RPCrossUnthresholdedTimeSeriesTestCase(RPCrossFixedRadiusTimeSeriesTestCase):
    """
    Tests for RP, Cross, Unthresholded, Time Series.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood: Unthresholded neighbourhood condition.
        """
        cls.neighbourhood = Unthresholded()

    def perform_recurrence_analysis_computations(self,
                                                 settings,
                                                 opencl=None,
                                                 verbose=False,
                                                 edge_length=None,
                                                 selector=SingleSelector(),
                                                 variants_kwargs=None,
                                                 all_variants=False):
        if opencl:
            opencl.reset()

        if not edge_length:
            edge_length = settings.max_number_of_vectors

        baseline = Baseline(settings,
                            verbose=verbose)

        result_baseline = baseline.run()

        if all_variants:
            execution_engine = Engine(settings,
                                      opencl=opencl,
                                      verbose=False,
                                      edge_length=edge_length,
                                      selector=selector,
                                      variants=VARIANTS,
                                      variants_kwargs=variants_kwargs)

            result = execution_engine.run()

            self.compare_unthresholded_recurrence_plot_results(result_baseline,
                                                               result)
        else:
            for variant in VARIANTS:
                try:
                    execution_engine = Engine(settings,
                                              opencl=opencl,
                                              verbose=False,
                                              edge_length=edge_length,
                                              selector=selector,
                                              variants=(variant,),
                                              variants_kwargs=variants_kwargs)

                    result = execution_engine.run()

                    self.compare_unthresholded_recurrence_plot_results(result_baseline,
                                                                       result,
                                                                       variant=variant)
                except NoMatchingVariantException:
                    continue


class RPCrossUnthresholdedEmbeddedSeriesTestCase(RPCrossUnthresholdedTimeSeriesTestCase):
    """
    Tests for RP, Cross, Unthresholded, Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_x: Embedded series on X axis comprising vectors consisting of random floating point values.
        :cvar time_series_y: Embedded series on X axis comprising vectors consisting of random floating point values.
        """
        embedding_dimension = np.random.randint(1, 10)

        cls.time_series_x = EmbeddedSeries(np.array([np.random.rand(embedding_dimension) for _ in np.arange(cls.time_series_length_x)]))
        cls.time_series_y = EmbeddedSeries(np.array([np.random.rand(embedding_dimension) for _ in np.arange(cls.time_series_length_y)]))

        cls.time_series = (cls.time_series_x,
                           cls.time_series_y)

    def test_embedding_parameters(self):
        """
        Test using different than the default recurrence analysis settings.
        """
        pass


if __name__ == "__main__":
    unittest.main()
