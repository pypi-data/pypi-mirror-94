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

__kernel void create_matrix_fixed_radius_maximum_metric(
    __global const ${fp_type}* time_series_x,
    __global const ${fp_type}* time_series_y,
    const uint dim_x,
    const uint dim_y,
    const uint m,
    const uint t_x,
    const uint t_y,
    const ${fp_type} e,
    const uint size,
    __global uint* matrix
)
{
    uint global_id_x = get_global_id(0);
    uint global_id_y = get_global_id(1);

    if (global_id_x < dim_x)
    {
        ${fp_type} max = 0.0f;

        for (uint i = 0; i < m; ++i)
        {
            max = fmax(fabs(time_series_x[global_id_x + (i * t_x)] - time_series_y[global_id_y + (i * t_y)]), max);
        }

        if (max < e)
        {
            atomic_add(&matrix[(global_id_y / size) * dim_x + global_id_x], (convert_uint(1) << (global_id_y % size)));
        }
    }
}

__kernel void create_matrix_radius_corridor_maximum_metric(
    __global const ${fp_type}* time_series_x,
    __global const ${fp_type}* time_series_y,
    const uint dim_x,
    const uint dim_y,
    const uint m,
    const uint t_x,
    const uint t_y,
    const ${fp_type} e_in,
    const ${fp_type} e_out,
    const uint size,
    __global uint* matrix
)
{
    uint global_id_x = get_global_id(0);
    uint global_id_y = get_global_id(1);

    if (global_id_x < dim_x)
    {
        ${fp_type} max = 0.0f;

        for (uint i = 0; i < m; ++i)
        {
            max = fmax(fabs(time_series_x[global_id_x + (i * t_x)] - time_series_y[global_id_y + (i * t_y)]), max);
        }

        if (e_in < max && max < e_out)
        {
            atomic_add(&matrix[(global_id_y / size) * dim_x + global_id_x], (convert_uint(1) << (global_id_y % size)));
        }
    }
}
