/*
Author: Tobias Rawald
Copyright: Copyright 2015-2021 The PyRQA project
Credits: Tobias Rawald, Mike Sips
License: Apache-2.0
Maintainer: Tobias Rawald
Email: pyrqa@gmx.net
Status: Development
*/

#ifdef cl_khr_fp16
    #pragma OPENCL EXTENSION cl_khr_fp16 : enable
#endif

#ifdef cl_khr_fp64
    #pragma OPENCL EXTENSION cl_khr_fp64 : enable
#endif

#ifdef cl_nv_pragma_unroll
   #pragma OPENCL EXTENSION cl_nv_pragma_unroll : enable
#endif

__kernel void detect_diagonal_lines(
    __global uint* matrix,
    const uint dim_x,
    const uint dim_y,
    const uint dim_xy,
    const uint start_x,
    const uint start_y,
    const uint w,
    const uint size,
    __global uint* frequency_distribution,
    __global uint* carryover
)
{
    uint global_id_x = get_global_id(0);

    uint id_x = global_id_x;
    uint id_y = 0;

    if (global_id_x < dim_xy && abs_diff(start_x + (id_x - dim_y + 1), start_y) >= w)
    {
        int delta_id_x;
        uint buffer = carryover[global_id_x];

        #pragma unroll loop_unroll
        for (;id_x < dim_xy && id_y < dim_y;)
        {
            delta_id_x = id_x - dim_y + 1;

            if (delta_id_x >= 0)
            {
                if ((matrix[(id_y / size) * dim_x + delta_id_x] & (1 << (id_y % size))) == (1 << (id_y % size)))
                {
                    buffer++;
                }
                else
                {
                    if(buffer > 0)
                    {
                        atomic_inc(&frequency_distribution[buffer - 1]);
                    }

                    buffer = 0;
                }
            }

            id_x++;
            id_y++;
        }

        carryover[global_id_x] = buffer;
    }
}

__kernel void detect_diagonal_lines_symmetric(
    __global uint* matrix,
    const uint dim_x,
    const uint dim_y,
    const uint start_x,
    const uint start_y,
    const uint w,
    const uint size,
    const uint offset,
    __global uint* frequency_distribution,
    __global uint* carryover
)
{
    uint global_id_x = get_global_id(0);

    uint id_x = global_id_x + offset;
    uint id_y = 0;

    if (id_x < dim_x && abs_diff(start_x + id_x, start_y + id_y) >= w)
    {
        uint carryover_id = id_x;
        if (offset > 0)
        {
            carryover_id = dim_x - id_x;
        }

        uint buffer = carryover[carryover_id];

        #pragma unroll loop_unroll
        for (;id_x < dim_x && id_y < dim_y;)
        {
            uint bitmask = (1 << (id_y % size));

            if ((matrix[(id_y / size) * dim_x + id_x] & bitmask) == bitmask)
            {
                buffer++;
            }
            else
            {
                if(buffer > 0)
                {
                    atomic_inc(&frequency_distribution[buffer - 1]);
                }

                buffer = 0;
            }

            id_x++;
            id_y++;
        }

        carryover[carryover_id] = buffer;
    }
}
