#!/usr/bin/env python

"""
Testing joint recurrence plot implementations.
"""

import numpy as np
import unittest

from pyrqa.analysis_type import Classic, \
    Cross
from pyrqa.exceptions import NoMatchingVariantException
from pyrqa.neighbourhood import FixedRadius, \
    RadiusCorridor
from pyrqa.selector import SingleSelector
from pyrqa.tests.joint import JointTestCase
from pyrqa.time_series import TimeSeries, \
    EmbeddedSeries

from pyrqa.variants.jrp.radius.baseline import Baseline
from pyrqa.variants.jrp.radius.engine import Engine

from pyrqa.variants.jrp.radius.column_overlap_materialisation_byte import ColumnOverlapMaterialisationByte
from pyrqa.variants.jrp.radius.column_no_overlap_materialisation_byte import ColumnNoOverlapMaterialisationByte
from pyrqa.variants.jrp.radius.row_no_overlap_materialisation_byte import RowNoOverlapMaterialisationByte

VARIANTS = (ColumnOverlapMaterialisationByte,
            ColumnNoOverlapMaterialisationByte,
            RowNoOverlapMaterialisationByte)

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2021 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


class JRPClassicClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase(JointTestCase):
    """
    Tests for JRP, Classic x Classic, Fixed Radius x Fixed Radius, Time Series x Time Series.
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

    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Same time series as time_series_1_x.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
        """
        cls.time_series_1_x = TimeSeries(np.random.rand(cls.time_series_length))
        cls.time_series_1_y = cls.time_series_1_x

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

        :cvar analysis_type_1: Classic analysis type.
        :cvar analysis_type_2: Classic analysis type.
        """
        cls.analysis_type_1 = Classic
        cls.analysis_type_2 = Classic

    @classmethod
    def setUpNeighbourhood(cls):
        """
        Set up neighbourhood.

        :cvar neighbourhood_1: Fixed Radius neighbourhood condition.
        :cvar neighbourhood_2: Fixed Radius neighbourhood condition.
        """
        cls.neighbourhood_1 = FixedRadius(np.random.uniform(.1, 1.))
        cls.neighbourhood_2 = FixedRadius(np.random.uniform(.1, 1.))

    @classmethod
    def setUpMinimumEdgeLength(cls):
        """
        Set up minimum edge length.

        :return: Minimum edge length.
        """
        cls.minimum_edge_length = pow(2, 5)

    @classmethod
    def setUpClass(cls):
        """
        Set up test case.
        """
        cls.setUpTimeSeriesLength()
        cls.setUpTimeSeries()
        cls.setUpAnalysisType()
        cls.setUpNeighbourhood()
        cls.setUpMinimumEdgeLength()

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
            engine = Engine(settings,
                            opencl=opencl,
                            verbose=False,
                            edge_length=edge_length,
                            selector=selector,
                            variants=VARIANTS,
                            variants_kwargs=variants_kwargs)

            result = engine.run()

            self.compare_recurrence_plot_results(result_baseline,
                                                 result)
        else:
            for variant in VARIANTS:
                try:
                    engine = Engine(settings,
                                    opencl=opencl,
                                    verbose=False,
                                    edge_length=edge_length,
                                    selector=selector,
                                    variants=(variant,),
                                    variants_kwargs=variants_kwargs)

                    result = engine.run()

                    self.compare_recurrence_plot_results(result_baseline,
                                                         result,
                                                         variant=variant)
                except NoMatchingVariantException:
                    continue


class JRPClassicClassicFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase(JRPClassicClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Classic x Classic, Fixed Radius x Fixed Radius, Time Series x Embedded Series.
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


class JRPClassicClassicFixedRadiusFixedRadiusEmbeddedSeriesTimeSeriesTestCase(JRPClassicClassicFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Classic x Classic, Fixed Radius x Fixed Radius, Embedded Series x Time Series.
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


class JRPClassicClassicFixedRadiusFixedRadiusEmbeddedSeriesEmbeddedSeriesTestCase(JRPClassicClassicFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Classic x Classic, Fixed Radius x Fixed Radius, Embedded Series x Embedded Series.
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


class JRPClassicClassicFixedRadiusRadiusCorridorTimeSeriesTimeSeriesTestCase(JRPClassicClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Classic x Classic, Fixed Radius x Radius Corridor, Time Series x Time Series.
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


class JRPClassicClassicFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase(JRPClassicClassicFixedRadiusRadiusCorridorTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Classic x Classic, Fixed Radius x Radius Corridor, Time Series x Embedded Series.
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


class JRPClassicClassicFixedRadiusRadiusCorridorEmbeddedSeriesTimeSeriesTestCase(JRPClassicClassicFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Classic x Classic, Fixed Radius x Radius Corridor, Embedded Series x Time Series.
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


class JRPClassicClassicFixedRadiusRadiusCorridorEmbeddedSeriesEmbeddedSeriesTestCase(JRPClassicClassicFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Classic x Classic, Fixed Radius x Radius Corridor, Embedded Series x Embedded Series.
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


class JRPClassicClassicRadiusCorridorFixedRadiusTimeSeriesTimeSeriesTestCase(JRPClassicClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Classic x Classic, Radius Corridor x Fixed Radius, Time Series x Time Series.
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


class JRPClassicClassicRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase(JRPClassicClassicRadiusCorridorFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Classic x Classic, Radius Corridor x Fixed Radius, Time Series x Embedded Series.
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


class JRPClassicClassicRadiusCorridorFixedRadiusEmbeddedSeriesTimeSeriesTestCase(JRPClassicClassicRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Classic x Classic, Radius Corridor x Fixed Radius, Embedded Series x Time Series.
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


class JRPClassicClassicRadiusCorridorFixedRadiusEmbeddedSeriesEmbeddedSeriesTestCase(JRPClassicClassicRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Classic x Classic, Radius Corridor x Fixed Radius, Embedded Series x Embedded Series.
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


class JRPClassicClassicRadiusCorridorRadiusCorridorTimeSeriesTimeSeriesTestCase(JRPClassicClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Classic x Classic, Radius Corridor x Radius Corridor, Time Series x Time Series.
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


class JRPClassicClassicRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase(JRPClassicClassicRadiusCorridorRadiusCorridorTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Classic x Classic, Radius Corridor x Radius Corridor, Time Series x Embedded Series.
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


class JRPClassicClassicRadiusCorridorRadiusCorridorEmbeddedSeriesTimeSeriesTestCase(JRPClassicClassicRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Classic x Classic, Radius Corridor x Radius Corridor, Embedded Series x Time Series.
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


class JRPClassicClassicRadiusCorridorRadiusCorridorEmbeddedSeriesEmbeddedSeriesTestCase(JRPClassicClassicRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Classic x Classic, Radius Corridor x Radius Corridor, Embedded Series x Embedded Series.
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


class JRPClassicCrossFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase(JRPClassicClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Classic x Cross, Fixed Radius x Fixed Radius, Time Series x Time Series.
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


class JRPClassicCrossFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase(JRPClassicCrossFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Classic x Cross, Fixed Radius x Fixed Radius, Time Series x Embedded Series.
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


class JRPClassicCrossFixedRadiusFixedRadiusEmbeddedSeriesTimeSeriesTestCase(JRPClassicCrossFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Classic x Cross, Fixed Radius x Fixed Radius, Embedded Series x Time Series.
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


class JRPClassicCrossFixedRadiusFixedRadiusEmbeddedSeriesEmbeddedSeriesTestCase(JRPClassicCrossFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Classic x Cross, Fixed Radius x Fixed Radius, Embedded Series x Embedded Series.
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


class JRPClassicCrossFixedRadiusRadiusCorridorTimeSeriesTimeSeriesTestCase(JRPClassicCrossFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Classic x Cross, Fixed Radius x Radius Corridor, Time Series x Time Series.
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


class JRPClassicCrossFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase(JRPClassicCrossFixedRadiusRadiusCorridorTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Classic x Cross, Fixed Radius x Radius Corridor, Time Series x Embedded Series.
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


class JRPClassicCrossFixedRadiusRadiusCorridorEmbeddedSeriesTimeSeriesTestCase(JRPClassicCrossFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Classic x Cross, Fixed Radius x Radius Corridor, Embedded Series x Time Series.
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


class JRPClassicCrossFixedRadiusRadiusCorridorEmbeddedSeriesEmbeddedSeriesTestCase(JRPClassicCrossFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Classic x Cross, Fixed Radius x Radius Corridor, Embedded Series x Embedded Series.
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


class JRPClassicCrossRadiusCorridorFixedRadiusTimeSeriesTimeSeriesTestCase(JRPClassicCrossFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Classic x Cross, Radius Corridor x Fixed Radius, Time Series x Time Series.
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


class JRPClassicCrossRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase(JRPClassicCrossRadiusCorridorFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Classic x Cross, Radius Corridor x Fixed Radius, Time Series x Embedded Series.
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


class JRPClassicCrossRadiusCorridorFixedRadiusEmbeddedSeriesTimeSeriesTestCase(JRPClassicCrossRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Classic x Cross, Radius Corridor x Fixed Radius, Embedded Series x Time Series.
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


class JRPClassicCrossRadiusCorridorFixedRadiusEmbeddedSeriesEmbeddedSeriesTestCase(JRPClassicCrossRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Classic x Cross, Radius Corridor x Fixed Radius, Embedded Series x Embedded Series.
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


class JRPClassicCrossRadiusCorridorRadiusCorridorTimeSeriesTimeSeriesTestCase(JRPClassicCrossFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Classic x Cross, Radius Corridor x Radius Corridor, Time Series x Time Series.
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


class JRPClassicCrossRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase(JRPClassicCrossRadiusCorridorRadiusCorridorTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Classic x Cross, Radius Corridor x Radius Corridor, Time Series x Embedded Series.
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


class JRPClassicCrossRadiusCorridorRadiusCorridorEmbeddedSeriesTimeSeriesTestCase(JRPClassicCrossRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Classic x Cross, Radius Corridor x Radius Corridor, Embedded Series x Time Series.
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


class JRPClassicCrossRadiusCorridorRadiusCorridorEmbeddedSeriesEmbeddedSeriesTestCase(JRPClassicCrossRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Classic x Cross, Radius Corridor x Radius Corridor, Embedded Series x Embedded Series.
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


class JRPCrossClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase(JRPClassicClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Cross x Classic, Fixed Radius x Fixed Radius, Time Series x Time Series.
    """
    @classmethod
    def setUpTimeSeries(cls):
        """
        Set up time series.

        :cvar time_series_length: Length of time series.
        :cvar time_series_1_x: Time series consisting random floating point values.
        :cvar time_series_1_y: Time series consisting random floating point values.
        :cvar time_series_2_x: Time series consisting random floating point values.
        :cvar time_series_2_y: Same time series as time_series_2_x.
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


class JRPCrossClassicFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase(JRPCrossClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Cross x Classic, Fixed Radius x Fixed Radius, Time Series x Embedded Series.
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


class JRPCrossClassicFixedRadiusFixedRadiusEmbeddedSeriesTimeSeriesTestCase(JRPCrossClassicFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Cross x Classic, Fixed Radius x Fixed Radius, Embedded Series x Time Series.
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


class JRPCrossClassicFixedRadiusFixedRadiusEmbeddedSeriesEmbeddedSeriesTestCase(JRPCrossClassicFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Cross x Classic, Fixed Radius x Fixed Radius, Embedded Series x Embedded Series.
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


class JRPCrossClassicFixedRadiusRadiusCorridorTimeSeriesTimeSeriesTestCase(JRPCrossClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Cross x Classic, Fixed Radius x Radius Corridor, Time Series x Time Series.
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


class JRPCrossClassicFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase(JRPCrossClassicFixedRadiusRadiusCorridorTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Cross x Classic, Fixed Radius x Radius Corridor, Time Series x Embedded Series.
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


class JRPCrossClassicFixedRadiusRadiusCorridorEmbeddedSeriesTimeSeriesTestCase(JRPCrossClassicFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Cross x Classic, Fixed Radius x Radius Corridor, Embedded Series x Time Series.
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


class JRPCrossClassicFixedRadiusRadiusCorridorEmbeddedSeriesEmbeddedSeriesTestCase(JRPCrossClassicFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Cross x Classic, Fixed Radius x Radius Corridor, Embedded Series x Embedded Series.
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


class JRPCrossClassicRadiusCorridorFixedRadiusTimeSeriesTimeSeriesTestCase(JRPCrossClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Cross x Classic, Radius Corridor x Fixed Radius, Time Series x Time Series.
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


class JRPCrossClassicRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase(JRPCrossClassicRadiusCorridorFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Cross x Classic, Radius Corridor x Fixed Radius, Time Series x Embedded Series.
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


class JRPCrossClassicRadiusCorridorFixedRadiusEmbeddedSeriesTimeSeriesTestCase(JRPCrossClassicRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Cross x Classic, Radius Corridor x Fixed Radius, Embedded Series x Time Series.
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


class JRPCrossClassicRadiusCorridorFixedRadiusEmbeddedSeriesEmbeddedSeriesTestCase(JRPCrossClassicRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Cross x Classic, Radius Corridor x Fixed Radius, Embedded Series x Embedded Series.
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


class JRPCrossClassicRadiusCorridorRadiusCorridorTimeSeriesTimeSeriesTestCase(JRPCrossClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Cross x Classic, Radius Corridor x Radius Corridor, Time Series x Time Series.
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


class JRPCrossClassicRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase(JRPCrossClassicRadiusCorridorRadiusCorridorTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Cross x Classic, Radius Corridor x Radius Corridor, Time Series x Embedded Series.
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


class JRPCrossClassicRadiusCorridorRadiusCorridorEmbeddedSeriesTimeSeriesTestCase(JRPCrossClassicRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Cross x Classic, Radius Corridor x Radius Corridor, Embedded Series x Time Series.
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


class JRPCrossClassicRadiusCorridorRadiusCorridorEmbeddedSeriesEmbeddedSeriesTestCase(JRPCrossClassicRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Cross x Classic, Radius Corridor x Radius Corridor, Embedded Series x Embedded Series.
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


class JRPCrossCrossFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase(JRPClassicClassicFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Cross x Cross, Fixed Radius x Fixed Radius, Time Series x Time Series.
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


class JRPCrossCrossFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase(JRPCrossCrossFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Cross x Cross, Fixed Radius x Fixed Radius, Time Series x Embedded Series.
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


class JRPCrossCrossFixedRadiusFixedRadiusEmbeddedSeriesTimeSeriesTestCase(JRPCrossCrossFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Cross x Cross, Fixed Radius x Fixed Radius, Embedded Series x Time Series.
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


class JRPCrossCrossFixedRadiusFixedRadiusEmbeddedSeriesEmbeddedSeriesTestCase(JRPCrossCrossFixedRadiusFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Cross x Cross, Fixed Radius x Fixed Radius, Embedded Series x Embedded Series.
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


class JRPCrossCrossFixedRadiusRadiusCorridorTimeSeriesTimeSeriesTestCase(JRPCrossCrossFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Cross x Cross, Fixed Radius x Radius Corridor, Time Series x Time Series.
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


class JRPCrossCrossFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase(JRPCrossCrossFixedRadiusRadiusCorridorTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Cross x Cross, Fixed Radius x Radius Corridor, Time Series x Embedded Series.
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


class JRPCrossCrossFixedRadiusRadiusCorridorEmbeddedSeriesTimeSeriesTestCase(JRPCrossCrossFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Cross x Cross, Fixed Radius x Radius Corridor, Embedded Series x Time Series.
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


class JRPCrossCrossFixedRadiusRadiusCorridorEmbeddedSeriesEmbeddedSeriesTestCase(JRPCrossCrossFixedRadiusRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Cross x Cross, Fixed Radius x Radius Corridor, Embedded Series x Embedded Series.
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


class JRPCrossCrossRadiusCorridorFixedRadiusTimeSeriesTimeSeriesTestCase(JRPCrossCrossFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Cross x Cross, Radius Corridor x Fixed Radius, Time Series x Time Series.
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


class JRPCrossCrossRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase(JRPCrossCrossRadiusCorridorFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Cross x Cross, Radius Corridor x Fixed Radius, Time Series x Embedded Series.
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


class JRPCrossCrossRadiusCorridorFixedRadiusEmbeddedSeriesTimeSeriesTestCase(JRPCrossCrossRadiusCorridorFixedRadiusTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Cross x Cross, Radius Corridor x Fixed Radius, Embedded Series x Time Series.
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


class JRPCrossCrossRadiusCorridorFixedRadiusEmbeddedSeriesEmbeddedSeriesTestCase(JRPCrossCrossRadiusCorridorFixedRadiusEmbeddedSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Cross x Cross, Radius Corridor x Fixed Radius, Embedded Series x Embedded Series.
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


class JRPCrossCrossRadiusCorridorRadiusCorridorTimeSeriesTimeSeriesTestCase(JRPCrossCrossFixedRadiusFixedRadiusTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Cross x Cross, Radius Corridor x Radius Corridor, Time Series x Time Series.
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


class JRPCrossCrossRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase(JRPCrossCrossRadiusCorridorRadiusCorridorTimeSeriesTimeSeriesTestCase):
    """
    Tests for JRP, Cross x Cross, Radius Corridor x Radius Corridor, Time Series x Embedded Series.
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


class JRPCrossCrossRadiusCorridorRadiusCorridorEmbeddedSeriesTimeSeriesTestCase(JRPCrossCrossRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Cross x Cross, Radius Corridor x Radius Corridor, Embedded Series x Time Series.
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


class JRPCrossCrossRadiusCorridorRadiusCorridorEmbeddedSeriesEmbeddedSeriesTestCase(JRPCrossCrossRadiusCorridorRadiusCorridorTimeSeriesEmbeddedSeriesTestCase):
    """
    Tests for JRP, Cross x Cross, Radius Corridor x Radius Corridor, Embedded Series x Embedded Series.
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
