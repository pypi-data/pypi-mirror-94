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

__kernel void create_matrix_unthresholded_taxicab_metric(
    __global const ${fp_type}* vectors_x,
    __global const ${fp_type}* vectors_y,
    const uint dim_x,
    const uint dim_y,
    const uint m,
    __global ${fp_type}* matrix
)
{
    uint global_id_x = get_global_id(0);
    uint global_id_y = get_global_id(1);

    if (global_id_x < dim_x)
    {
        ${fp_type} sum = 0.0f;

        for (uint i = 0; i < m; ++i)
        {
            sum += fabs(vectors_x[global_id_x + (i * dim_x)] - vectors_y[global_id_y + (i * dim_y)]);
        }

        matrix[global_id_y * dim_x + global_id_x] = sum;
    }
}
