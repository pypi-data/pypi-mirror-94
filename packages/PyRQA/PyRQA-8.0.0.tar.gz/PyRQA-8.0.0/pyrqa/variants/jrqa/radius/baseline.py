#!/usr/bin/env python

"""
Baseline joint recurrence quantification analysis implementation.
"""

import math
import time

import numpy as np

from pyrqa.scalable_recurrence_analysis import RQA, \
    Carryover
from pyrqa.result import RQAResult
from pyrqa.runtimes import MatrixRuntimes,\
    FlavourRuntimesMonolithic

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2021 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


class Baseline(RQA,
               Carryover):
    """
    Full Matrix
    No Sub Matrices
    Plain Python
    """
    def __init__(self,
                 settings,
                 verbose=True):
        RQA.__init__(self, settings, verbose)
        Carryover.__init__(self, settings, verbose)

        self.__initialise()

    def __initialise(self):
        self.diagonal_length_carryover = np.zeros(
            self.settings.number_of_vectors_x + self.settings.number_of_vectors_y - 1,
            dtype=np.uint32)

    def reset(self):
        RQA.reset(self)
        Carryover.reset(self)

        self.__initialise()

    def run(self):
        start = time.time()

        self.reset()

        for index_x in np.arange(self.settings.number_of_vectors_x):

            vertical_index = index_x

            for index_y in np.arange(self.settings.number_of_vectors_y):

                diagonal_index = self.settings.number_of_vectors_y - 1 - index_y + index_x

                distance_1 = self.settings.settings_1.similarity_measure.get_distance_vectors(
                    self.settings.settings_1.time_series_x.get_vectors_as_rows(),
                    self.settings.settings_1.time_series_y.get_vectors_as_rows(),
                    self.settings.settings_1.embedding_dimension,
                    index_x,
                    index_y)

                distance_2 = self.settings.settings_2.similarity_measure.get_distance_vectors(
                    self.settings.settings_2.time_series_x.get_vectors_as_rows(),
                    self.settings.settings_2.time_series_y.get_vectors_as_rows(),
                    self.settings.settings_2.embedding_dimension,
                    index_x,
                    index_y)

                if self.settings.settings_1.neighbourhood.contains(distance_1) and self.settings.settings_2.neighbourhood.contains(distance_2):
                    # Recurrence points
                    self.recurrence_points[vertical_index] += 1

                    # Diagonal lines
                    if math.fabs(index_y - index_x) >= self.settings.theiler_corrector:
                        self.diagonal_length_carryover[diagonal_index] += 1

                    # Vertical lines
                    self.vertical_length_carryover[vertical_index] += 1

                    # White vertical lines
                    if self.white_vertical_length_carryover[vertical_index] > 0:
                        self.white_vertical_frequency_distribution[self.white_vertical_length_carryover[vertical_index] - 1] += 1

                    self.white_vertical_length_carryover[vertical_index] = 0
                else:
                    # Diagonal lines
                    if self.diagonal_length_carryover[diagonal_index] > 0:
                        self.diagonal_frequency_distribution[self.diagonal_length_carryover[diagonal_index] - 1] += 1

                    self.diagonal_length_carryover[diagonal_index] = 0

                    # Vertical lines
                    if self.vertical_length_carryover[vertical_index] > 0:
                        self.vertical_frequency_distribution[self.vertical_length_carryover[vertical_index] - 1] += 1

                    self.vertical_length_carryover[vertical_index] = 0

                    # White vertical lines
                    self.white_vertical_length_carryover[vertical_index] += 1

        for line_length in self.diagonal_length_carryover:
            if line_length > 0:
                self.diagonal_frequency_distribution[line_length - 1] += 1

        for line_length in self.vertical_length_carryover:
            if line_length > 0:
                self.vertical_frequency_distribution[line_length - 1] += 1

        for line_length in self.white_vertical_length_carryover:
            if line_length > 0:
                self.white_vertical_frequency_distribution[line_length - 1] += 1

        end = time.time()

        variant_runtimes = FlavourRuntimesMonolithic(execute_computations=end - start)

        number_of_partitions_x = 1
        number_of_partitions_y = 1

        matrix_runtimes = MatrixRuntimes(number_of_partitions_x,
                                         number_of_partitions_y)
        matrix_runtimes.update_index(0,
                                     0,
                                     variant_runtimes)

        result = RQAResult(self.settings,
                           matrix_runtimes,
                           recurrence_points=self.recurrence_points,
                           diagonal_frequency_distribution=self.diagonal_frequency_distribution,
                           vertical_frequency_distribution=self.vertical_frequency_distribution,
                           white_vertical_frequency_distribution=self.white_vertical_frequency_distribution)

        return result
