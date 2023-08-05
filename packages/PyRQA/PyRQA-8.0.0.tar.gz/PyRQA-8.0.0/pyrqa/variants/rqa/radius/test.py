#!/usr/bin/env python

"""
Testing recurrence quantification analysis implementations according to the fixed radius and radius corridor neighbourhood condition.
"""

import numpy as np
import unittest

from pyrqa.exceptions import NoMatchingVariantException
from pyrqa.neighbourhood import RadiusCorridor
from pyrqa.selector import SingleSelector
from pyrqa.time_series import EmbeddedSeries
from pyrqa.variants.rp.radius.test import RPClassicFixedRadiusTimeSeriesTestCase, \
    RPCrossFixedRadiusTimeSeriesTestCase
from pyrqa.variants.rqa.radius.baseline import Baseline
from pyrqa.variants.rqa.radius.engine import Engine

from pyrqa.variants.rqa.radius.column_no_overlap_materialisation_bit_no_recycling import ColumnNoOverlapMaterialisationBitNoRecycling
from pyrqa.variants.rqa.radius.column_no_overlap_materialisation_bit_recycling import ColumnNoOverlapMaterialisationBitRecycling
from pyrqa.variants.rqa.radius.column_no_overlap_materialisation_byte_no_recycling import ColumnNoOverlapMaterialisationByteNoRecycling
from pyrqa.variants.rqa.radius.column_no_overlap_materialisation_byte_recycling import ColumnNoOverlapMaterialisationByteRecycling
from pyrqa.variants.rqa.radius.column_no_overlap_no_materialisation import ColumnNoOverlapNoMaterialisation
from pyrqa.variants.rqa.radius.column_overlap_materialisation_bit_no_recycling import ColumnOverlapMaterialisationBitNoRecycling
from pyrqa.variants.rqa.radius.column_overlap_materialisation_bit_recycling import ColumnOverlapMaterialisationBitRecycling
from pyrqa.variants.rqa.radius.column_overlap_materialisation_byte_no_recycling import ColumnOverlapMaterialisationByteNoRecycling
from pyrqa.variants.rqa.radius.column_overlap_materialisation_byte_recycling import ColumnOverlapMaterialisationByteRecycling
from pyrqa.variants.rqa.radius.column_overlap_no_materialisation import ColumnOverlapNoMaterialisation
from pyrqa.variants.rqa.radius.row_no_overlap_materialisation_bit_no_recycling import RowNoOverlapMaterialisationBitNoRecycling
from pyrqa.variants.rqa.radius.row_no_overlap_materialisation_bit_recycling import RowNoOverlapMaterialisationBitRecycling
from pyrqa.variants.rqa.radius.row_no_overlap_materialisation_byte_no_recycling import RowNoOverlapMaterialisationByteNoRecycling
from pyrqa.variants.rqa.radius.row_no_overlap_materialisation_byte_recycling import RowNoOverlapMaterialisationByteRecycling
from pyrqa.variants.rqa.radius.row_no_overlap_no_materialisation import RowNoOverlapNoMaterialisation

VARIANTS = (ColumnNoOverlapMaterialisationBitNoRecycling,
            ColumnNoOverlapMaterialisationBitRecycling,
            ColumnNoOverlapMaterialisationByteNoRecycling,
            ColumnNoOverlapMaterialisationByteRecycling,
            ColumnNoOverlapNoMaterialisation,
            ColumnOverlapMaterialisationBitNoRecycling,
            ColumnOverlapMaterialisationBitRecycling,
            ColumnOverlapMaterialisationByteNoRecycling,
            ColumnOverlapMaterialisationByteRecycling,
            ColumnOverlapNoMaterialisation,
            RowNoOverlapMaterialisationBitNoRecycling,
            RowNoOverlapMaterialisationBitRecycling,
            RowNoOverlapMaterialisationByteNoRecycling,
            RowNoOverlapMaterialisationByteRecycling,
            RowNoOverlapNoMaterialisation)

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2021 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


class RQAClassicFixedRadiusTimeSeriesTestCase(RPClassicFixedRadiusTimeSeriesTestCase):
    """
    Tests for RQA, Classic, Fixed Radius, Time Series.
    """
    @classmethod
    def setUpTimeSeriesLength(cls):
        """
        Set up time series length.

        :cvar time_series_length: Length of time series.
        """
        cls.time_series_length = np.random.randint(pow(2, 7),
                                                   pow(2, 8))

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

            self.compare_rqa_results(result_baseline,
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

                    self.compare_rqa_results(result_baseline,
                                             result,
                                             variant=variant)
                except NoMatchingVariantException:
                    continue


class RQAClassicFixedRadiusEmbeddedSeriesTestCase(RQAClassicFixedRadiusTimeSeriesTestCase):
    """
    Tests for RQA, Classic, Fixed Radius, Embedded Series.
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


class RQAClassicRadiusCorridorTimeSeriesTestCase(RQAClassicFixedRadiusTimeSeriesTestCase):
    """
    Tests for RQA, Classic, Radius Corridor, Time Series.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood: Radius corridor neighbourhood condition.
        """
        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood = RadiusCorridor(inner_radius=inner_radius,
                                           outer_radius=outer_radius)


class RQAClassicRadiusCorridorEmbeddedSeriesTestCase(RQAClassicRadiusCorridorTimeSeriesTestCase):
    """
    Tests for RQA, Classic, Radius Corridor, Embedded Series.
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


class RQACrossFixedRadiusTimeSeriesTestCase(RPCrossFixedRadiusTimeSeriesTestCase):
    """
    Tests for RQA, Cross, Fixed Radius, Time Series.
    """
    @classmethod
    def setUpTimeSeriesLength(cls):
        """
        Set up time series length.

        :cvar time_series_length_x: Length of time series on X axis.
        :cvar time_series_length_y: Length of time series on Y axis.
        """
        cls.time_series_length_x = np.random.randint(pow(2, 7),
                                                     pow(2, 8))
        cls.time_series_length_y = np.random.randint(pow(2, 7),
                                                     pow(2, 8))

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

            self.compare_rqa_results(result_baseline,
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

                    self.compare_rqa_results(result_baseline,
                                             result,
                                             variant=variant)
                except NoMatchingVariantException:
                    continue


class RQACrossFixedRadiusEmbeddedSeriesTestCase(RQACrossFixedRadiusTimeSeriesTestCase):
    """
    Tests for RQA, Cross, Fixed Radius, Embedded Series.
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


class RQACrossRadiusCorridorTimeSeriesTestCase(RQACrossFixedRadiusTimeSeriesTestCase):
    """
    Tests for RQA, Cross, Radius Corridor, Time Series.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood: Radius corridor neighbourhood condition.
        """
        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood = RadiusCorridor(inner_radius=inner_radius,
                                           outer_radius=outer_radius)


class RQACrossRadiusCorridorEmbeddedSeriesTestCase(RQACrossRadiusCorridorTimeSeriesTestCase):
    """
    Tests for RQA, Cross, Radius Corridor, Embedded Series.
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