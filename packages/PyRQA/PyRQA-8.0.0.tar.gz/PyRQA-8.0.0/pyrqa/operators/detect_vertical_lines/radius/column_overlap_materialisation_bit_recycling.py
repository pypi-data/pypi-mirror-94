#!/usr/bin/env python

"""
Detect vertical lines.

Input data format: Column store
Input data overlap: Yes
Recurrence matrix materialisation: Yes
Similarity value representation: Bit
Intermediate results recycling: Yes
"""

import numpy as np
import pyopencl as cl

from pyrqa.exceptions import SubMatrixNotProcessedException
from pyrqa.neighbourhood import FixedRadius, \
    RadiusCorridor
from pyrqa.opencl import OpenCL
from pyrqa.runtimes import OperatorRuntimes

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015-2021 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


def detect_vertical_lines(settings,
                          data_type,
                          sub_matrix,
                          device,
                          context,
                          command_queue,
                          kernels):
    """
    :param settings: Settings.
    :param data_type: Data type.
    :param sub_matrix: Sub matrix.
    :param device: OpenCL device.
    :param context: OpenCL context.
    :param command_queue: OpenCL command queue.
    :param kernels: OpenCL kernels.
    :return: OpenCL sub matrix buffer, runtimes.
    """
    transfer_to_device_events = []
    execute_computations_events = []
    transfer_from_device_events = []

    clear_buffer_kernel = kernels[0]
    detect_vertical_lines_kernel = kernels[1]

    # Write to buffers
    time_series_x = settings.time_series_x.get_sub_series(sub_matrix.start_x,
                                                          sub_matrix.dim_x)

    time_series_x_buffer = cl.Buffer(context,
                                     cl.mem_flags.READ_ONLY,
                                     time_series_x.nbytes)

    transfer_to_device_events.append(cl.enqueue_copy(command_queue,
                                                     time_series_x_buffer,
                                                     time_series_x,
                                                     device_offset=0,
                                                     wait_for=None,
                                                     is_blocking=False))

    time_series_y = settings.time_series_y.get_sub_series(sub_matrix.start_y,
                                                          sub_matrix.dim_y)

    time_series_y_buffer = cl.Buffer(context,
                                     cl.mem_flags.READ_ONLY,
                                     time_series_y.nbytes)

    transfer_to_device_events.append(cl.enqueue_copy(command_queue,
                                                     time_series_y_buffer,
                                                     time_series_y,
                                                     device_offset=0,
                                                     wait_for=None,
                                                     is_blocking=False))

    recurrence_points_buffer = cl.Buffer(context,
                                         cl.mem_flags.READ_WRITE,
                                         sub_matrix.recurrence_points.nbytes)

    transfer_to_device_events.append(cl.enqueue_copy(command_queue,
                                                     recurrence_points_buffer,
                                                     sub_matrix.recurrence_points,
                                                     device_offset=0,
                                                     wait_for=None,
                                                     is_blocking=False))

    vertical_carryover_buffer = cl.Buffer(context,
                                          cl.mem_flags.READ_WRITE,
                                          sub_matrix.vertical_length_carryover.nbytes)

    transfer_to_device_events.append(cl.enqueue_copy(command_queue,
                                                     vertical_carryover_buffer,
                                                     sub_matrix.vertical_length_carryover,
                                                     device_offset=0,
                                                     wait_for=None,
                                                     is_blocking=False))

    white_vertical_carryover_buffer = cl.Buffer(context,
                                                cl.mem_flags.READ_WRITE,
                                                sub_matrix.white_vertical_length_carryover.nbytes)

    transfer_to_device_events.append(cl.enqueue_copy(command_queue,
                                                     white_vertical_carryover_buffer,
                                                     sub_matrix.white_vertical_length_carryover,
                                                     device_offset=0,
                                                     wait_for=None,
                                                     is_blocking=False))

    vertical_frequency_distribution_buffer = cl.Buffer(context,
                                                       cl.mem_flags.READ_WRITE,
                                                       sub_matrix.vertical_frequency_distribution.nbytes)

    transfer_to_device_events.append(cl.enqueue_copy(command_queue,
                                                     vertical_frequency_distribution_buffer,
                                                     sub_matrix.vertical_frequency_distribution,
                                                     device_offset=0,
                                                     wait_for=None,
                                                     is_blocking=False))

    white_vertical_frequency_distribution_buffer = cl.Buffer(context,
                                                             cl.mem_flags.READ_WRITE,
                                                             sub_matrix.white_vertical_frequency_distribution.nbytes)

    transfer_to_device_events.append(cl.enqueue_copy(command_queue,
                                                     white_vertical_frequency_distribution_buffer,
                                                     sub_matrix.white_vertical_frequency_distribution,
                                                     device_offset=0,
                                                     wait_for=None,
                                                     is_blocking=False))

    if sub_matrix.size_bit(data_type) > device.max_mem_alloc_size:
        raise SubMatrixNotProcessedException("Calculation aborted: The size of the sub matrix is too large.")

    sub_matrix_buffer = cl.Buffer(context,
                                  cl.mem_flags.READ_WRITE,
                                  int(sub_matrix.size_bit(data_type)))

    command_queue.finish()

    # Execute clear buffer kernel
    clear_buffer_args = [sub_matrix_buffer,
                         data_type(0)]

    OpenCL.set_kernel_args(clear_buffer_kernel,
                           clear_buffer_args)

    global_work_size = [int(sub_matrix.elements_bit(data_type))]
    local_work_size = None

    execute_computations_events.append(cl.enqueue_nd_range_kernel(command_queue,
                                                                  clear_buffer_kernel,
                                                                  global_work_size,
                                                                  local_work_size))

    command_queue.finish()

    # Execute detect vertical lines kernel
    if type(settings.neighbourhood) is FixedRadius:
        detect_vertical_lines_args = [time_series_x_buffer,
                                      time_series_y_buffer,
                                      np.uint32(sub_matrix.dim_x),
                                      np.uint32(sub_matrix.dim_y),
                                      np.uint32(settings.embedding_dimension),
                                      np.uint32(settings.time_series_x.time_delay),
                                      np.uint32(settings.time_series_y.time_delay),
                                      settings.dtype(settings.neighbourhood.condition),
                                      np.uint32(sub_matrix.bits_per_element(data_type)),
                                      recurrence_points_buffer,
                                      vertical_frequency_distribution_buffer,
                                      vertical_carryover_buffer,
                                      white_vertical_frequency_distribution_buffer,
                                      white_vertical_carryover_buffer,
                                      sub_matrix_buffer]
    elif type(settings.neighbourhood) is RadiusCorridor:
        detect_vertical_lines_args = [time_series_x_buffer,
                                      time_series_y_buffer,
                                      np.uint32(sub_matrix.dim_x),
                                      np.uint32(sub_matrix.dim_y),
                                      np.uint32(settings.embedding_dimension),
                                      np.uint32(settings.time_series_x.time_delay),
                                      np.uint32(settings.time_series_y.time_delay),
                                      settings.dtype(settings.neighbourhood.condition[0]),
                                      settings.dtype(settings.neighbourhood.condition[1]),
                                      np.uint32(sub_matrix.bits_per_element(data_type)),
                                      recurrence_points_buffer,
                                      vertical_frequency_distribution_buffer,
                                      vertical_carryover_buffer,
                                      white_vertical_frequency_distribution_buffer,
                                      white_vertical_carryover_buffer,
                                      sub_matrix_buffer]

    OpenCL.set_kernel_args(detect_vertical_lines_kernel, detect_vertical_lines_args)

    global_work_size = [int(sub_matrix.dim_x + (device.max_work_group_size - (sub_matrix.dim_x % device.max_work_group_size)))]
    local_work_size = None

    execute_computations_events.append(cl.enqueue_nd_range_kernel(command_queue,
                                                                  detect_vertical_lines_kernel,
                                                                  global_work_size,
                                                                  local_work_size))

    command_queue.finish()

    # Read from buffers
    transfer_from_device_events.append(cl.enqueue_copy(command_queue,
                                                       sub_matrix.recurrence_points,
                                                       recurrence_points_buffer,
                                                       device_offset=0,
                                                       wait_for=None,
                                                       is_blocking=False))

    transfer_from_device_events.append(cl.enqueue_copy(command_queue,
                                                       sub_matrix.vertical_length_carryover,
                                                       vertical_carryover_buffer,
                                                       device_offset=0,
                                                       wait_for=None,
                                                       is_blocking=False))

    transfer_from_device_events.append(cl.enqueue_copy(command_queue,
                                                       sub_matrix.white_vertical_length_carryover,
                                                       white_vertical_carryover_buffer,
                                                       device_offset=0,
                                                       wait_for=None,
                                                       is_blocking=False))

    transfer_from_device_events.append(cl.enqueue_copy(command_queue,
                                                       sub_matrix.vertical_frequency_distribution,
                                                       vertical_frequency_distribution_buffer,
                                                       device_offset=0,
                                                       wait_for=None,
                                                       is_blocking=False))

    transfer_from_device_events.append(cl.enqueue_copy(command_queue,
                                                       sub_matrix.white_vertical_frequency_distribution,
                                                       white_vertical_frequency_distribution_buffer,
                                                       device_offset=0,
                                                       wait_for=None,
                                                       is_blocking=False))

    command_queue.finish()

    # Determine runtimes
    runtimes = OperatorRuntimes()
    runtimes.transfer_to_device += OpenCL.convert_events_runtime(transfer_to_device_events)
    runtimes.execute_computations += OpenCL.convert_events_runtime(execute_computations_events)
    runtimes.transfer_from_device += OpenCL.convert_events_runtime(transfer_from_device_events)

    return sub_matrix_buffer, \
        runtimes
