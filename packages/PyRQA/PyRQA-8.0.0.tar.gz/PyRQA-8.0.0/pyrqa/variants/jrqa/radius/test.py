#!/usr/bin/env python

"""
Testing joint recurrence quantification analysis implementations.
"""

import numpy as np
import unittest

from pyrqa.analysis_type import Classic, \
    Cross
from pyrqa.exceptions import NoMatchingVariantException
from pyrqa.neighbourhood import FixedRadius, \
    RadiusCorridor
from pyrqa.selector import SingleSelector
from pyrqa.time_series import TimeSeries, \
    EmbeddedSeries

from pyrqa.variants.jrp.radius.test import JRPClassicClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase
from pyrqa.variants.jrqa.radius.baseline import Baseline
from pyrqa.variants.jrqa.radius.engine import Engine

from pyrqa.variants.jrqa.radius.column_no_overlap_materialisation_byte_no_recycling import ColumnNoOverlapMaterialisationByteNoRecycling
from pyrqa.variants.jrqa.radius.column_overlap_materialisation_bit_no_recycling import ColumnOverlapMaterialisationBitNoRecycling
from pyrqa.variants.jrqa.radius.column_overlap_materialisation_byte_no_recycling import ColumnOverlapMaterialisationByteNoRecycling
from pyrqa.variants.jrqa.radius.row_no_overlap_materialisation_bit_no_recycling import RowNoOverlapMaterialisationBitNoRecycling
from pyrqa.variants.jrqa.radius.row_no_overlap_materialisation_byte_no_recycling import RowNoOverlapMaterialisationByteNoRecycling

VARIANTS = (ColumnNoOverlapMaterialisationByteNoRecycling,
            ColumnOverlapMaterialisationBitNoRecycling,
            ColumnOverlapMaterialisationByteNoRecycling,
            RowNoOverlapMaterialisationBitNoRecycling,
            RowNoOverlapMaterialisationByteNoRecycling)

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2021 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


class JRQAClassicClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase(JRPClassicClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Classic x Classic, Fixed Radius x Fixed Radius, Time Series x Time Series.
    """
    @classmethod
    def setUpTimeSeriesLength(cls):
        """
        Set up time series length.

        :cvar time_series_length_minimum: Minimum length of time series.
        :cvar time_series_length_maximum: Maximum length of time series.
        :cvar time_series_length: Length of time series.
        """
        cls.time_series_length_minimum = pow(2, 6)
        cls.time_series_length_maximum = pow(2, 7)

        cls.time_series_length = np.random.randint(cls.time_series_length_minimum,
                                                   cls.time_series_length_maximum)

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


class JRQAClassicClassicFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase(JRQAClassicClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Classic x Classic, Fixed Radius x Fixed Radius, Time Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_1_x.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """
        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_x.number_of_vectors)]))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    def test_embedding_parameters(self):
        """
        Test using different than the default recurrence analysis settings.
        """
        pass


class JRQAClassicClassicFixedRadiusFixedRadiusEmbeddedSeriesTimeSeriesTestCase(JRQAClassicClassicFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Classic x Classic, Fixed Radius x Fixed Radius, Embedded Series x Time Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_2_x.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_1_x.
        """
        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_x.number_of_vectors)]))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)


class JRQAClassicClassicFixedRadiusFixedRadiusEmbeddedSeriesEmbeddedSeriesTestCase(JRQAClassicClassicFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Classic x Classic, Fixed Radius x Fixed Radius, Embedded Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_1_x.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)


class JRQAClassicClassicFixedRadiusRadiusCorridorTimeSeriesTimeSeriesTestCase(JRQAClassicClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Classic x Classic, Fixed Radius x Radius Corridor, Time Series x Time Series.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Fixed Radius neighbourhood condition.
        :cvar neighbourhood_2: Radius corridor neighbourhood condition.
        """
        cls.neighbourhood_1 = FixedRadius(np.random.uniform(.1, 1.))

        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_2 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)


class JRQAClassicClassicFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase(JRQAClassicClassicFixedRadiusRadiusCorridorTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Classic x Classic, Fixed Radius x Radius Corridor, Time Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_1_x.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """
        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_x.number_of_vectors)]))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    def test_embedding_parameters(self):
        """
        Test using different than the default recurrence analysis settings.
        """
        pass


class JRQAClassicClassicFixedRadiusRadiusCorridorEmbeddedSeriesTimeSeriesTestCase(JRQAClassicClassicFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Classic x Classic, Fixed Radius x Radius Corridor, Embedded Series x Time Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_2_x.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_1_x.
        """
        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_x.number_of_vectors)]))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)


class JRQAClassicClassicFixedRadiusRadiusCorridorEmbeddedSeriesEmbeddedSeriesTestCase(JRQAClassicClassicFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Classic x Classic, Fixed Radius x Radius Corridor, Embedded Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_1_x.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)


class JRQAClassicClassicRadiusCorridorFixedRadiusTimeSeriesTimeSeriesTestCase(JRQAClassicClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Classic x Classic, Radius Corridor x Fixed Radius, Time Series x Time Series.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Radius corridor neighbourhood condition.
        :cvar neighbourhood_2: Fixed radius neighbourhood condition.
        """
        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_1 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)

        cls.neighbourhood_2 = FixedRadius(np.random.uniform(.1, 1.))


class JRQAClassicClassicRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase(JRQAClassicClassicRadiusCorridorFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Classic x Classic, Radius Corridor x Fixed Radius, Time Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_1_x.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """
        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_x.number_of_vectors)]))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    def test_embedding_parameters(self):
        """
        Test using different than the default recurrence analysis settings.
        """
        pass


class JRQAClassicClassicRadiusCorridorFixedRadiusEmbeddedSeriesTimeSeriesTestCase(JRQAClassicClassicRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Classic x Classic, Radius Corridor x Fixed Radius, Embedded Series x Time Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_2_x.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_1_x.
        """
        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_x.number_of_vectors)]))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)


class JRQAClassicClassicRadiusCorridorFixedRadiusEmbeddedSeriesEmbeddedSeriesTestCase(JRQAClassicClassicRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Classic x Classic, Radius Corridor x Fixed Radius, Embedded Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_1_x.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)


class JRQAClassicClassicRadiusCorridorRadiusCorridorTimeSeriesTimeSeriesTestCase(JRQAClassicClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Classic x Classic, Radius Corridor x Radius Corridor, Time Series x Time Series.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Radius corridor neighbourhood condition.
        :cvar neighbourhood_2: Radius corridor neighbourhood condition.
        """
        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_1 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)

        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_2 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)


class JRQAClassicClassicRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase(JRQAClassicClassicRadiusCorridorRadiusCorridorTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Classic x Classic, Radius Corridor x Radius Corridor, Time Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_1_x.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """
        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_x.number_of_vectors)]))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    def test_embedding_parameters(self):
        """
        Test using different than the default recurrence analysis settings.
        """
        pass


class JRQAClassicClassicRadiusCorridorRadiusCorridorEmbeddedSeriesTimeSeriesTestCase(JRQAClassicClassicRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Classic x Classic, Radius Corridor x Radius Corridor, Embedded Series x Time Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_2_x.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_1_x.
        """
        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_x.number_of_vectors)]))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)


class JRQAClassicClassicRadiusCorridorRadiusCorridorEmbeddedSeriesEmbeddedSeriesTestCase(JRQAClassicClassicRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Classic x Classic, Radius Corridor x Radius Corridor, Embedded Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_1_x.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)


class JRQAClassicCrossFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase(JRQAClassicClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Classic x Cross, Fixed Radius x Fixed Radius, Time Series x Time Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_1_x.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Time series consisting random floating point values.
        """
        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_2_y = TimeSeries(np.random.rand(cls.time_series_length))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    @classmethod
    def setUpAnalysisType(cls):
        """
        Set up analysis type.

        :cvar analysis_type_1: Classic analysis type.
        :cvar analysis_type_2: Cross analysis type.
        """
        cls.analysis_type_1 = Classic
        cls.analysis_type_2 = Cross


class JRQAClassicCrossFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase(JRQAClassicCrossFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Classic x Cross, Fixed Radius x Fixed Radius, Time Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_1_x.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Embedded series consisting random floating point values.
        """
        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_x.number_of_vectors)]))
        cls.time_series_2_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_x.number_of_vectors)]))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    def test_embedding_parameters(self):
        """
        Test using different than the default recurrence analysis settings.
        """
        pass


class JRQAClassicCrossFixedRadiusFixedRadiusEmbeddedSeriesTimeSeriesTestCase(JRQAClassicCrossFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Classic x Cross, Fixed Radius x Fixed Radius, Embedded Series x Time Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_2_x.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Time series consisting random floating point values.
        """
        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_2_y = TimeSeries(np.random.rand(cls.time_series_length))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_x.number_of_vectors)]))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)


class JRQAClassicCrossFixedRadiusFixedRadiusEmbeddedSeriesEmbeddedSeriesTestCase(JRQAClassicCrossFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Classic x Cross, Fixed Radius x Fixed Radius, Embedded Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_1_x.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Embedded series consisting random floating point values.
        """

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_2_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length)]))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)


class JRQAClassicCrossFixedRadiusRadiusCorridorTimeSeriesTimeSeriesTestCase(JRQAClassicCrossFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Classic x Cross, Fixed Radius x Radius Corridor, Time Series x Time Series.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Fixed Radius neighbourhood condition.
        :cvar neighbourhood_2: Radius corridor neighbourhood condition.
        """
        cls.neighbourhood_1 = FixedRadius(np.random.uniform(.1, 1.))

        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_2 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)


class JRQAClassicCrossFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase(JRQAClassicCrossFixedRadiusRadiusCorridorTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Classic x Cross, Fixed Radius x Radius Corridor, Time Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_1_x.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Embedded series consisting random floating point values.
        """
        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_x.number_of_vectors)]))
        cls.time_series_2_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_x.number_of_vectors)]))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    def test_embedding_parameters(self):
        """
        Test using different than the default recurrence analysis settings.
        """
        pass


class JRQAClassicCrossFixedRadiusRadiusCorridorEmbeddedSeriesTimeSeriesTestCase(JRQAClassicCrossFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Classic x Cross, Fixed Radius x Radius Corridor, Embedded Series x Time Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_2_x.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Time series consisting random floating point values.
        """
        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_2_y = TimeSeries(np.random.rand(cls.time_series_length))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_x.number_of_vectors)]))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)


class JRQAClassicCrossFixedRadiusRadiusCorridorEmbeddedSeriesEmbeddedSeriesTestCase(JRQAClassicCrossFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Classic x Cross, Fixed Radius x Radius Corridor, Embedded Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_1_x.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Embedded series consisting random floating point values.
        """

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_2_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length)]))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)


class JRQAClassicCrossRadiusCorridorFixedRadiusTimeSeriesTimeSeriesTestCase(JRQAClassicCrossFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Classic x Cross, Radius Corridor x Fixed Radius, Time Series x Time Series.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Radius corridor neighbourhood condition.
        :cvar neighbourhood_2: Fixed radius neighbourhood condition.
        """
        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_1 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)

        cls.neighbourhood_2 = FixedRadius(np.random.uniform(.1, 1.))


class JRQAClassicCrossRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase(JRQAClassicCrossRadiusCorridorFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Classic x Cross, Radius Corridor x Fixed Radius, Time Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_1_x.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Embedded series consisting random floating point values.
        """
        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_x.number_of_vectors)]))
        cls.time_series_2_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_x.number_of_vectors)]))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    def test_embedding_parameters(self):
        """
        Test using different than the default recurrence analysis settings.
        """
        pass


class JRQAClassicCrossRadiusCorridorFixedRadiusEmbeddedSeriesTimeSeriesTestCase(JRQAClassicCrossRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Classic x Cross, Radius Corridor x Fixed Radius, Embedded Series x Time Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_2_x.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Time series consisting random floating point values.
        """
        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_2_y = TimeSeries(np.random.rand(cls.time_series_length))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_x.number_of_vectors)]))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)


class JRQAClassicCrossRadiusCorridorFixedRadiusEmbeddedSeriesEmbeddedSeriesTestCase(JRQAClassicCrossRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Classic x Cross, Radius Corridor x Fixed Radius, Embedded Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_1_x.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Embedded series consisting random floating point values.
        """

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_2_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length)]))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)


class JRQAClassicCrossRadiusCorridorRadiusCorridorTimeSeriesTimeSeriesTestCase(JRQAClassicCrossFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Classic x Cross, Radius Corridor x Radius Corridor, Time Series x Time Series.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Radius corridor neighbourhood condition.
        :cvar neighbourhood_2: Radius corridor neighbourhood condition.
        """
        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_1 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)

        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_2 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)


class JRQAClassicCrossRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase(JRQAClassicCrossRadiusCorridorRadiusCorridorTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Classic x Cross, Radius Corridor x Radius Corridor, Time Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_1_x.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Embedded series consisting random floating point values.
        """
        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_x.number_of_vectors)]))
        cls.time_series_2_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_x.number_of_vectors)]))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    def test_embedding_parameters(self):
        """
        Test using different than the default recurrence analysis settings.
        """
        pass


class JRQAClassicCrossRadiusCorridorRadiusCorridorEmbeddedSeriesTimeSeriesTestCase(JRQAClassicCrossRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Classic x Cross, Radius Corridor x Radius Corridor, Embedded Series x Time Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_1_x.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Time series consisting random floating point values.
        """
        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_2_y = TimeSeries(np.random.rand(cls.time_series_length))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_x.number_of_vectors)]))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)


class JRQAClassicCrossRadiusCorridorRadiusCorridorEmbeddedSeriesEmbeddedSeriesTestCase(JRQAClassicCrossRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Classic x Cross, Radius Corridor x Radius Corridor, Embedded Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_1_x.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Embedded series consisting random floating point values.
        """

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_1_y = cls.time_series_1_x

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_2_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length)]))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)


class JRQACrossClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase(JRQAClassicClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Cross x Classic, Fixed Radius x Fixed Radius, Time Series x Time Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Time series consisting random floating point values.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Time series consisting random floating point values.
        """
        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_1_y = TimeSeries(np.random.rand(cls.time_series_length))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    @classmethod
    def setUpAnalysisType(cls):
        """
        Set up analysis type.

        :cvar analysis_type_1: Cross analysis type.
        :cvar analysis_type_2: Classic analysis type.
        """
        cls.analysis_type_1 = Cross
        cls.analysis_type_2 = Classic


class JRQACrossClassicFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase(JRQACrossClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Cross x Classic, Fixed Radius x Fixed Radius, Time Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Time series consisting random floating point values.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """
        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_1_y = TimeSeries(np.random.rand(cls.time_series_length))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_x.number_of_vectors)]))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    def test_embedding_parameters(self):
        """
        Test using different than the default recurrence analysis settings.
        """
        pass


class JRQACrossClassicFixedRadiusFixedRadiusEmbeddedSeriesTimeSeriesTestCase(JRQACrossClassicFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Cross x Classic, Fixed Radius x Fixed Radius, Embedded Series x Time Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Embedded series consisting random floating point values.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """
        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_x.number_of_vectors)]))
        cls.time_series_1_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_x.number_of_vectors)]))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)


class JRQACrossClassicFixedRadiusFixedRadiusEmbeddedSeriesEmbeddedSeriesTestCase(JRQACrossClassicFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Cross x Classic, Fixed Radius x Fixed Radius, Embedded Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Embedded series consisting random floating point values.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """
        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_1_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length)]))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)


class JRQACrossClassicFixedRadiusRadiusCorridorTimeSeriesTimeSeriesTestCase(JRQACrossClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Cross x Classic, Fixed Radius x Radius Corridor, Time Series x Time Series.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Fixed radius neighbourhood condition.
        :cvar neighbourhood_2: Radius corridor neighbourhood condition.
        """
        cls.neighbourhood_1 = FixedRadius(np.random.uniform(.1, 1.))

        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_2 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)


class JRQACrossClassicFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase(JRQACrossClassicFixedRadiusRadiusCorridorTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Cross x Classic, Fixed Radius x Radius Corridor, Time Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Time series consisting random floating point values.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """
        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_1_y = TimeSeries(np.random.rand(cls.time_series_length))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_x.number_of_vectors)]))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    def test_embedding_parameters(self):
        """
        Test using different than the default recurrence analysis settings.
        """
        pass


class JRQACrossClassicFixedRadiusRadiusCorridorEmbeddedSeriesTimeSeriesTestCase(JRQACrossClassicFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Cross x Classic, Fixed Radius x Radius Corridor, Embedded Series x Time Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Embedded series consisting random floating point values.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """
        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_x.number_of_vectors)]))
        cls.time_series_1_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_x.number_of_vectors)]))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)


class JRQACrossClassicFixedRadiusRadiusCorridorEmbeddedSeriesEmbeddedSeriesTestCase(JRQACrossClassicFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Cross x Classic, Fixed Radius x Radius Corridor, Embedded Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Embedded series consisting random floating point values.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """
        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_1_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length)]))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)


class JRQACrossClassicRadiusCorridorFixedRadiusTimeSeriesTimeSeriesTestCase(JRQACrossClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Cross x Classic, Radius Corridor x Fixed Radius, Time Series x Time Series.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Radius corridor neighbourhood condition.
        :cvar neighbourhood_2: Fixed radius neighbourhood condition.
        """
        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_1 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)

        cls.neighbourhood_2 = FixedRadius(np.random.uniform(.1, 1.))


class JRQACrossClassicRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase(JRQACrossClassicRadiusCorridorFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Cross x Classic, Radius Corridor x Fixed Radius, Time Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Time series consisting random floating point values.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """
        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_1_y = TimeSeries(np.random.rand(cls.time_series_length))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_x.number_of_vectors)]))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    def test_embedding_parameters(self):
        """
        Test using different than the default recurrence analysis settings.
        """
        pass


class JRQACrossClassicRadiusCorridorFixedRadiusEmbeddedSeriesTimeSeriesTestCase(JRQACrossClassicRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Cross x Classic, Radius Corridor x Fixed Radius, Embedded Series x Time Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Embedded series consisting random floating point values.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """
        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_x.number_of_vectors)]))
        cls.time_series_1_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_x.number_of_vectors)]))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)


class JRQACrossClassicRadiusCorridorFixedRadiusEmbeddedSeriesEmbeddedSeriesTestCase(JRQACrossClassicRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Cross x Classic, Radius Corridor x Fixed Radius, Embedded Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Embedded series consisting random floating point values.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """
        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_1_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length)]))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)


class JRQACrossClassicRadiusCorridorRadiusCorridorTimeSeriesTimeSeriesTestCase(JRQACrossClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Cross x Classic, Radius Corridor x Radius Corridor, Time Series x Time Series.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Radius corridor neighbourhood condition.
        :cvar neighbourhood_2: Radius corridor neighbourhood condition.
        """
        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_1 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)

        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_2 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)


class JRQACrossClassicRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase(JRQACrossClassicRadiusCorridorRadiusCorridorTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Cross x Classic, Radius Corridor x Radius Corridor, Time Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Time series consisting random floating point values.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """
        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_1_y = TimeSeries(np.random.rand(cls.time_series_length))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_x.number_of_vectors)]))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    def test_embedding_parameters(self):
        """
        Test using different than the default recurrence analysis settings.
        """
        pass


class JRQACrossClassicRadiusCorridorRadiusCorridorEmbeddedSeriesTimeSeriesTestCase(JRQACrossClassicRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Cross x Classic, Radius Corridor x Radius Corridor, Embedded Series x Time Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Embedded series consisting random floating point values.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """
        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_x.number_of_vectors)]))
        cls.time_series_1_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_x.number_of_vectors)]))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)


class JRQACrossClassicRadiusCorridorRadiusCorridorEmbeddedSeriesEmbeddedSeriesTestCase(JRQACrossClassicRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Cross x Classic, Radius Corridor x Radius Corridor, Embedded Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Embedded series consisting random floating point values.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """
        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_1_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length)]))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length)]))
        cls.time_series_2_y = cls.time_series_2_x

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)


class JRQACrossCrossFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase(JRQAClassicClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Cross x Cross, Fixed Radius x Fixed Radius, Time Series x Time Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length_x: Length of time series regarding X axis.
        :cvar time_series_length_y: Length of time series regarding Y axis.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Time series consisting random floating point values.
        :cvar time_series_1: Tuple consisting of time_series_1_x and time_series_1_y.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Time series consisting random floating point values.
        :cvar time_series_2: Tuple consisting of time_series_2_x and time_series_2_y.
        """
        cls.time_series_length_x = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)
        cls.time_series_length_y = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)

        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length_x))
        cls.time_series_1_y = TimeSeries(np.random.rand(cls.time_series_length_y))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length_x))
        cls.time_series_2_y = TimeSeries(np.random.rand(cls.time_series_length_y))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    @classmethod
    def setUpAnalysisType(cls):
        """
        Set up analysis type.

        :cvar analysis_type_1: Cross analysis type.
        :cvar analysis_type_2: Cross analysis type.
        """
        cls.analysis_type_1 = Cross
        cls.analysis_type_2 = Cross


class JRQACrossCrossFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase(JRQACrossCrossFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Cross x Cross, Fixed Radius x Fixed Radius, Time Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length_x: Length of time series regarding X axis.
        :cvar time_series_length_y: Length of time series regarding Y axis.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Time series consisting random floating point values.
        :cvar time_series_1: Tuple consisting of time_series_1_x and time_series_1_y.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Embedded series consisting random floating point values.
        :cvar time_series_2: Tuple consisting of time_series_2_x and time_series_2_y.
        """
        cls.time_series_length_x = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)
        cls.time_series_length_y = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)

        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length_x))
        cls.time_series_1_y = TimeSeries(np.random.rand(cls.time_series_length_y))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_x.number_of_vectors)]))
        cls.time_series_2_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_y.number_of_vectors)]))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    def test_embedding_parameters(self):
        """
        Test using different than the default recurrence analysis settings.
        """
        pass


class JRQACrossCrossFixedRadiusFixedRadiusEmbeddedSeriesTimeSeriesTestCase(JRQACrossCrossFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Cross x Cross, Fixed Radius x Fixed Radius, Embedded Series x Time Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length_x: Length of time series regarding X axis.
        :cvar time_series_length_y: Length of time series regarding Y axis.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Embedded series consisting random floating point values.
        :cvar time_series_1: Tuple consisting of time_series_1_x and time_series_1_y.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Time series consisting random floating point values.
        :cvar time_series_2: Tuple consisting of time_series_2_x and time_series_2_y.
        """
        cls.time_series_length_x = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)
        cls.time_series_length_y = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)

        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length_x))
        cls.time_series_2_y = TimeSeries(np.random.rand(cls.time_series_length_y))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_x.number_of_vectors)]))
        cls.time_series_1_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_y.number_of_vectors)]))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)


class JRQACrossCrossFixedRadiusFixedRadiusEmbeddedSeriesEmbeddedSeriesTestCase(JRQACrossCrossFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Cross x Cross, Fixed Radius x Fixed Radius, Embedded Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length_x: Length of time series regarding X axis.
        :cvar time_series_length_y: Length of time series regarding Y axis.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Embedded series consisting random floating point values.
        :cvar time_series_1: Tuple consisting of time_series_1_x and time_series_1_y.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Embedded series consisting random floating point values.
        :cvar time_series_2: Tuple consisting of time_series_2_x and time_series_2_y.
        """
        cls.time_series_length_x = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)
        cls.time_series_length_y = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length_x)]))
        cls.time_series_1_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length_y)]))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length_x)]))
        cls.time_series_2_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length_y)]))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)


class JRQACrossCrossFixedRadiusRadiusCorridorTimeSeriesTimeSeriesTestCase(JRQACrossCrossFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Cross x Cross, Fixed Radius x Radius Corridor, Time Series x Time Series.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Fixed radius neighbourhood condition.
        :cvar neighbourhood_2: Radius corridor neighbourhood condition.
        """
        cls.neighbourhood_1 = FixedRadius(np.random.uniform(.1, 1.))

        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_2 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)


class JRQACrossCrossFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase(JRQACrossCrossFixedRadiusRadiusCorridorTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Cross x Cross, Fixed Radius x Radius Corridor, Time Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length_x: Length of time series regarding X axis.
        :cvar time_series_length_y: Length of time series regarding Y axis.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Time series consisting random floating point values.
        :cvar time_series_1: Tuple consisting of time_series_1_x and time_series_1_y.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Embedded series consisting random floating point values.
        :cvar time_series_2: Tuple consisting of time_series_2_x and time_series_2_y.
        """
        cls.time_series_length_x = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)
        cls.time_series_length_y = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)

        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length_x))
        cls.time_series_1_y = TimeSeries(np.random.rand(cls.time_series_length_y))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_x.number_of_vectors)]))
        cls.time_series_2_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_y.number_of_vectors)]))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    def test_embedding_parameters(self):
        """
        Test using different than the default recurrence analysis settings.
        """
        pass


class JRQACrossCrossFixedRadiusRadiusCorridorEmbeddedSeriesTimeSeriesTestCase(JRQACrossCrossFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Cross x Cross, Fixed Radius x Radius Corridor, Embedded Series x Time Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length_x: Length of time series regarding X axis.
        :cvar time_series_length_y: Length of time series regarding Y axis.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Embedded series consisting random floating point values.
        :cvar time_series_1: Tuple consisting of time_series_1_x and time_series_1_y.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Time series consisting random floating point values.
        :cvar time_series_2: Tuple consisting of time_series_2_x and time_series_2_y.
        """
        cls.time_series_length_x = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)
        cls.time_series_length_y = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)

        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length_x))
        cls.time_series_2_y = TimeSeries(np.random.rand(cls.time_series_length_y))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_x.number_of_vectors)]))
        cls.time_series_1_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_y.number_of_vectors)]))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)


class JRQACrossCrossFixedRadiusRadiusCorridorEmbeddedSeriesEmbeddedSeriesTestCase(JRQACrossCrossFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Cross x Cross, Fixed Radius x Radius Corridor, Embedded Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length_x: Length of time series regarding X axis.
        :cvar time_series_length_y: Length of time series regarding Y axis.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Embedded series consisting random floating point values.
        :cvar time_series_1: Tuple consisting of time_series_1_x and time_series_1_y.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Embedded series consisting random floating point values.
        :cvar time_series_2: Tuple consisting of time_series_2_x and time_series_2_y.
        """
        cls.time_series_length_x = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)
        cls.time_series_length_y = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length_x)]))
        cls.time_series_1_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length_y)]))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length_x)]))
        cls.time_series_2_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length_y)]))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)


class JRQACrossCrossRadiusCorridorFixedRadiusTimeSeriesTimeSeriesTestCase(JRQACrossCrossFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Cross x Cross, Radius Corridor x Fixed Radius, Time Series x Time Series.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Radius corridor neighbourhood condition.
        :cvar neighbourhood_2: Fixed radius neighbourhood condition.
        """
        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_1 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)

        cls.neighbourhood_2 = FixedRadius(np.random.uniform(.1, 1.))


class JRQACrossCrossRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase(JRQACrossCrossRadiusCorridorFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Cross x Cross, Radius Corridor x Fixed Radius, Time Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length_x: Length of time series regarding X axis.
        :cvar time_series_length_y: Length of time series regarding Y axis.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Time series consisting random floating point values.
        :cvar time_series_1: Tuple consisting of time_series_1_x and time_series_1_y.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Embedded series consisting random floating point values.
        :cvar time_series_2: Tuple consisting of time_series_2_x and time_series_2_y.
        """
        cls.time_series_length_x = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)
        cls.time_series_length_y = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)

        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length_x))
        cls.time_series_1_y = TimeSeries(np.random.rand(cls.time_series_length_y))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_x.number_of_vectors)]))
        cls.time_series_2_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_y.number_of_vectors)]))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    def test_embedding_parameters(self):
        """
        Test using different than the default recurrence analysis settings.
        """
        pass


class JRQACrossCrossRadiusCorridorFixedRadiusEmbeddedSeriesTimeSeriesTestCase(JRQACrossCrossRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Cross x Cross, Radius Corridor x Fixed Radius, Embedded Series x Time Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length_x: Length of time series regarding X axis.
        :cvar time_series_length_y: Length of time series regarding Y axis.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Embedded series consisting random floating point values.
        :cvar time_series_1: Tuple consisting of time_series_1_x and time_series_1_y.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Time series consisting random floating point values.
        :cvar time_series_2: Tuple consisting of time_series_2_x and time_series_2_y.
        """
        cls.time_series_length_x = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)
        cls.time_series_length_y = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)

        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length_x))
        cls.time_series_2_y = TimeSeries(np.random.rand(cls.time_series_length_y))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_x.number_of_vectors)]))
        cls.time_series_1_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_y.number_of_vectors)]))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)


class JRQACrossCrossRadiusCorridorFixedRadiusEmbeddedSeriesEmbeddedSeriesTestCase(JRQACrossCrossRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Cross x Cross, Radius Corridor x Fixed Radius, Embedded Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length_x: Length of time series regarding X axis.
        :cvar time_series_length_y: Length of time series regarding Y axis.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Embedded series consisting random floating point values.
        :cvar time_series_1: Tuple consisting of time_series_1_x and time_series_1_y.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Embedded series consisting random floating point values.
        :cvar time_series_2: Tuple consisting of time_series_2_x and time_series_2_y.
        """
        cls.time_series_length_x = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)
        cls.time_series_length_y = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length_x)]))
        cls.time_series_1_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length_y)]))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length_x)]))
        cls.time_series_2_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length_y)]))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)


class JRQACrossCrossRadiusCorridorRadiusCorridorTimeSeriesTimeSeriesTestCase(JRQACrossCrossFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Cross x Cross, Radius Corridor x Radius Corridor, Time Series x Time Series.
    """
    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Radius corridor neighbourhood condition.
        :cvar neighbourhood_2: Radius corridor neighbourhood condition.
        """
        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_1 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)

        inner_radius = np.random.uniform(.1, 1.)
        outer_radius = np.random.uniform(inner_radius, 1.)

        cls.neighbourhood_2 = RadiusCorridor(inner_radius=inner_radius,
                                             outer_radius=outer_radius)


class JRQACrossCrossRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase(JRQACrossCrossRadiusCorridorRadiusCorridorTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRQA, Cross x Cross, Radius Corridor x Radius Corridor, Time Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length_x: Length of time series regarding X axis.
        :cvar time_series_length_y: Length of time series regarding Y axis.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Time series consisting random floating point values.
        :cvar time_series_1: Tuple consisting of time_series_1_x and time_series_1_y.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Embedded series consisting random floating point values.
        :cvar time_series_2: Tuple consisting of time_series_2_x and time_series_2_y.
        """
        cls.time_series_length_x = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)
        cls.time_series_length_y = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)

        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length_x))
        cls.time_series_1_y = TimeSeries(np.random.rand(cls.time_series_length_y))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_x.number_of_vectors)]))
        cls.time_series_2_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_1_y.number_of_vectors)]))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

    def test_embedding_parameters(self):
        """
        Test using different than the default recurrence analysis settings.
        """
        pass


class JRQACrossCrossRadiusCorridorRadiusCorridorEmbeddedSeriesTimeSeriesTestCase(JRQACrossCrossRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Cross x Cross, Radius Corridor x Radius Corridor, Embedded Series x Time Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length_x: Length of time series regarding X axis.
        :cvar time_series_length_y: Length of time series regarding Y axis.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Embedded series consisting random floating point values.
        :cvar time_series_1: Tuple consisting of time_series_1_x and time_series_1_y.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Time series consisting random floating point values.
        :cvar time_series_2: Tuple consisting of time_series_2_x and time_series_2_y.
        """
        cls.time_series_length_x = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)
        cls.time_series_length_y = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)

        cls.time_series_2_x = TimeSeries(np.random.rand(cls.time_series_length_x))
        cls.time_series_2_y = TimeSeries(np.random.rand(cls.time_series_length_y))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_x.number_of_vectors)]))
        cls.time_series_1_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_2_y.number_of_vectors)]))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)


class JRQACrossCrossRadiusCorridorRadiusCorridorEmbeddedSeriesEmbeddedSeriesTestCase(JRQACrossCrossRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRQA, Cross x Cross, Radius Corridor x Radius Corridor, Embedded Series x Embedded Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length_x: Length of time series regarding X axis.
        :cvar time_series_length_y: Length of time series regarding Y axis.
        :cvar time_series_1_x: Embedded series consisting random floating point values.
        :cvar time_series_1_y: Embedded series consisting random floating point values.
        :cvar time_series_1: Tuple consisting of time_series_1_x and time_series_1_y.
        :cvar time_series_2_x: Embedded series consisting random floating point values.
        :cvar time_series_2_y: Embedded series consisting random floating point values.
        :cvar time_series_2: Tuple consisting of time_series_2_x and time_series_2_y.
        """
        cls.time_series_length_x = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)
        cls.time_series_length_y = np.random.randint(cls.time_series_length_minimum,
                                                     cls.time_series_length_maximum)

        embedding_dimension_1 = np.random.randint(1, 10)

        cls.time_series_1_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length_x)]))
        cls.time_series_1_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_1) for _ in np.arange(cls.time_series_length_y)]))

        cls.time_series_1 = (cls.time_series_1_x,
                             cls.time_series_1_y)

        embedding_dimension_2 = np.random.randint(1, 10)

        cls.time_series_2_x = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length_x)]))
        cls.time_series_2_y = EmbeddedSeries(
            np.array([np.random.rand(embedding_dimension_2) for _ in np.arange(cls.time_series_length_y)]))

        cls.time_series_2 = (cls.time_series_2_x,
                             cls.time_series_2_y)


if __name__ == "__main__":
    unittest.main()
