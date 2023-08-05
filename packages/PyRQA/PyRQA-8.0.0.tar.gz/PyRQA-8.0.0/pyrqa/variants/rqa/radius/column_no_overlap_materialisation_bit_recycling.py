#!/usr/bin/env python

"""
Conduct recurrence quantification analysis.

Input data format: Column store
Input data overlap: No
Recurrence matrix materialisation: Yes
Similarity value representation: Bit
Intermediate results recycling: Yes
"""

import numpy as np

from pyrqa.operators.detect_diagonal_lines.materialisation_bit import detect_diagonal_lines
from pyrqa.operators.detect_vertical_lines.radius.column_no_overlap_materialisation_bit_recycling import \
    detect_vertical_lines
from pyrqa.runtimes import FlavourRuntimesMultipleOperators
from pyrqa.utils import SettableSettings
from pyrqa.variants.types import TimeSeriesVariant, \
    EmbeddedSeriesVariant

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2021 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


class ColumnNoOverlapMaterialisationBitRecycling(SettableSettings,
                                                 TimeSeriesVariant,
                                                 EmbeddedSeriesVariant):
    """
    See module description regarding computational properties.

    :ivar opencl: OpenCL environment.
    :ivar device: OpenCL device.
    :ivar data_type: Data type to represent the similarity values.
    :ivar optimisations_enabled: Are the default OpenCL compiler optimisations enabled?
    :ivar loop_unroll: Loop unrolling factor.
    :ivar program: OpenCL program.
    :ivar program_created: Has the OpenCL program already been created?
    :ivar kernels: OpenCL kernels.
    :ivar kernels_created: Have the OpenCL kernels already been created?
    """
    def __init__(self,
                 settings,
                 opencl,
                 device,
                 **kwargs):
        """
        :param settings: Settings.
        :param opencl: OpenCL environment.
        :param device: OpenCL device.
        :param kwargs: Keyword arguments.
        """
        SettableSettings.__init__(self,
                                  settings)

        self.opencl = opencl
        self.device = device

        self.data_type = kwargs['data_type'] if 'data_type' in list(kwargs.keys()) else np.uint32
        self.optimisations_enabled = kwargs['optimisations_enabled'] if 'optimisations_enabled' in list(kwargs.keys()) else False
        self.loop_unroll = kwargs['loop_unroll'] if 'loop_unroll' in list(kwargs.keys()) else 1

        self.program = None
        self.program_created = False

        self.kernels = {}
        self.kernels_created = False

        self.clear_buffer_kernel_name = self.settings.clear_buffer_kernel_name(self.data_type)
        self.detect_vertical_lines_kernel_name = self.settings.detect_vertical_lines_kernel_name
        self.detect_diagonal_lines_kernel_name = self.settings.detect_diagonal_lines_operator_name

        self.__initialize()

    def __initialize(self):
        """
        Initialization of the variant.
        """
        if not self.program_created:
            self.program = self.opencl.create_program(self.device,
                                                      (detect_vertical_lines,
                                                       detect_diagonal_lines),
                                                      self.settings.kernels_sub_dir,
                                                      self.settings.dtype,
                                                      optimisations_enabled=self.optimisations_enabled,
                                                      loop_unroll=self.loop_unroll)

            self.program_created = True

        if not self.kernels_created:
            self.kernels = self.opencl.create_kernels(self.program,
                                                      (self.clear_buffer_kernel_name,
                                                       self.detect_vertical_lines_kernel_name,
                                                       self.detect_diagonal_lines_kernel_name))

            self.kernels_created = True

    def process_sub_matrix(self,
                           sub_matrix):
        """
        Processing of a single sub matrix.

        :param sub_matrix: Sub matrix.
        :return: Runtimes for processing the sub matrix.
        """
        # Create variant runtimes
        variant_runtimes = FlavourRuntimesMultipleOperators()

        # Detect vertical lines
        sub_matrix_buffer, \
            detect_vertical_lines_runtimes = detect_vertical_lines(self.settings,
                                                                   self.data_type,
                                                                   sub_matrix,
                                                                   self.device,
                                                                   self.opencl.contexts[self.device],
                                                                   self.opencl.command_queues[self.device],
                                                                   (self.kernels[self.clear_buffer_kernel_name],
                                                                    self.kernels[self.detect_vertical_lines_kernel_name]))

        variant_runtimes.detect_vertical_lines_runtimes = detect_vertical_lines_runtimes

        # Detect diagonal lines
        detect_diagonal_lines_runtimes = detect_diagonal_lines(self.settings.is_matrix_symmetric,
                                                               self.settings.theiler_corrector,
                                                               self.data_type,
                                                               sub_matrix,
                                                               sub_matrix_buffer,
                                                               self.device,
                                                               self.opencl.contexts[self.device],
                                                               self.opencl.command_queues[self.device],
                                                               (self.kernels[self.detect_diagonal_lines_kernel_name],))

        variant_runtimes.detect_diagonal_lines_runtimes = detect_diagonal_lines_runtimes

        return variant_runtimes
