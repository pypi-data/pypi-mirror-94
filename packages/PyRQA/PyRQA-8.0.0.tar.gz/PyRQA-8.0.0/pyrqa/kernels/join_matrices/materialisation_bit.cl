/*
Author: Tobias Rawald
Copyright: Copyright 2015-2021 The PyRQA project
Credits: Tobias Rawald, Mike Sips
License: Apache-2.0
Maintainer: Tobias Rawald
Email: pyrqa@gmx.net
Status: Development
*/

__kernel void join_matrices(
    __global uint* matrix_1,
    __global uint* matrix_2,
    const uint dim_x,
    const uint size,
    __global uint* joined_matrix
)
{
    uint global_id_x = get_global_id(0);
    uint global_id_y = get_global_id(1);

    uint bit_mask = convert_uint(1) << (global_id_y % size);
    uint value_1 = matrix_1[(global_id_y / size) * dim_x + global_id_x] & bit_mask;
    uint value_2 = matrix_2[(global_id_y / size) * dim_x + global_id_x] & bit_mask;

    if (global_id_x < dim_x)
    {
        if ((value_1 & value_2) == bit_mask)
        {
            atomic_add(&joined_matrix[(global_id_y / size) * dim_x + global_id_x], bit_mask);
        }
    }
}