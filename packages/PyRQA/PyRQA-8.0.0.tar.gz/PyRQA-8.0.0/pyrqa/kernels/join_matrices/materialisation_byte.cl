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
    __global uchar* matrix_1,
    __global uchar* matrix_2,
    const uint dim_x,
    __global uchar* joined_matrix
)
{
    uint global_id_x = get_global_id(0);
    uint global_id_y = get_global_id(1);

    if (global_id_x < dim_x)
    {
        if (matrix_1[global_id_y * dim_x + global_id_x] == 1 && matrix_2[global_id_y * dim_x + global_id_x] == 1)
        {
            joined_matrix[global_id_y * dim_x + global_id_x] = 1;
        }
        else
        {
            joined_matrix[global_id_y * dim_x + global_id_x] = 0;
        }
    }
}