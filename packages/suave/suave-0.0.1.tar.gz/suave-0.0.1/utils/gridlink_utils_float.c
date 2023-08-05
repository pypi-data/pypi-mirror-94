/* This file is auto-generated from gridlink_utils.c.src */
#ifdef DOUBLE_PREC
#undef DOUBLE_PREC
#endif
// # -*- mode: c -*-
/* File: gridlink_utils.c.src */
/*
  This file is a part of the Corrfunc package
  Copyright (C) 2015-- Manodeep Sinha (manodeep@gmail.com)
  License: MIT LICENSE. See LICENSE file under the top-level
  directory at https://github.com/manodeep/Corrfunc/
*/


#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#include "sglib.h"
#include "function_precision.h"
#include "utils.h"

#include "gridlink_utils_float.h"


#ifndef MEMORY_INCREASE_FAC
#define MEMORY_INCREASE_FAC   1.1
#endif

#ifndef CONVERT_3D_INDEX_TO_LINEAR
#define CONVERT_3D_INDEX_TO_LINEAR(ix, iy, iz, nx, ny, nz)           {ix*ny*nz + iy*nz + iz}
#endif


int get_binsize_float(const float xmin,const float xmax, const float rmax, const int refine_factor, const int max_ncells,
                       float *xbinsize, int *nlattice, const struct config_options *options)
{
    const float xdiff = (options->periodic && options->boxsize > 0) ? options->boxsize:(xmax-xmin);
    int nmesh=(int)(refine_factor*xdiff/rmax) ;
    nmesh = nmesh < 1 ? 1:nmesh;
    if(options->periodic == 1) {
        if (nmesh<(2*refine_factor+1))  {
            fprintf(stderr,"%s> ERROR:  nlattice = %d is so small that with periodic wrapping the same cells will be counted twice ....exiting\n",__FILE__,nmesh) ;
            fprintf(stderr,"%s> Please reduce Rmax = %"REAL_FORMAT" to be a smaller fraction of the particle distribution region = %"REAL_FORMAT"\n",
                    __FILE__,rmax, xdiff);
            return EXIT_FAILURE;
        }
    }

    if (nmesh>max_ncells)  nmesh=max_ncells;
    *xbinsize = xdiff/nmesh;
    *nlattice = nmesh;

    return EXIT_SUCCESS;
}


void get_max_min_float(const int64_t ND1, const float * restrict X1, const float * restrict Y1, const float * restrict Z1,
                        float *min_x, float *min_y, float *min_z, float *max_x, float *max_y, float *max_z)
{
    float xmin = *min_x, ymin = *min_y, zmin=*min_z;
    float xmax = *max_x, ymax = *max_y, zmax=*max_z;

    for(int64_t i=0;i<ND1;i++) {
        if(X1[i] < xmin) xmin=X1[i];
        if(Y1[i] < ymin) ymin=Y1[i];
        if(Z1[i] < zmin) zmin=Z1[i];


        if(X1[i] > xmax) xmax=X1[i];
        if(Y1[i] > ymax) ymax=Y1[i];
        if(Z1[i] > zmax) zmax=Z1[i];
    }
    *min_x=xmin;*min_y=ymin;*min_z=zmin;
    *max_x=xmax;*max_y=ymax;*max_z=zmax;
}



void get_max_min_ra_dec_float(const int64_t ND1, const float *RA, const float *DEC,
                               float *ra_min, float *dec_min, float *ra_max, float *dec_max)
{
    float xmin = *ra_min, ymin = *dec_min;
    float xmax = *ra_max, ymax = *dec_max;

    for(int64_t i=0;i<ND1;i++) {
        if(RA[i]  < xmin) xmin=RA[i];
        if(DEC[i] < ymin) ymin=DEC[i];

        if(RA[i] > xmax) xmax=RA[i];
        if(DEC[i] > ymax) ymax=DEC[i];
    }
    *ra_min=xmin;*dec_min=ymin;
    *ra_max=xmax;*dec_max=ymax;
}

float find_closest_pos_float(const float first_xbounds[2], const float second_xbounds[2], float *closest_pos0)
{
    *closest_pos0 = ZERO;
    /* if the limits are overlapping then the minimum possible separation is 0 */
    if(first_xbounds[0] <= second_xbounds[1]
       && second_xbounds[0] <= first_xbounds[1]) {
        return ZERO;
    }

    float min_dx = FABS(first_xbounds[0] - second_xbounds[0]);
    *closest_pos0 = first_xbounds[0];
    for(int i=0;i<2;i++) {
        for(int j=0;j<2;j++) {
            const float dx = FABS(first_xbounds[i] - second_xbounds[j]);
            if(dx < min_dx) {
                *closest_pos0 = first_xbounds[i];
                min_dx = dx;
            }
        }
    }

    return min_dx;
}


int reorder_particles_back_into_original_order_float(const int64_t np, int64_t *original_indices, float *X, float *Y, float *Z, weight_struct *weights)
{
    if(original_indices == NULL || X == NULL || Y == NULL || Z == NULL || weights == NULL) {
        fprintf(stderr,"Error: In %s> While re-ordering the particles back into their input order, the passed pointers "
                "can not be NULL. May be this function does not need to be called ?\n"
                "Please check the value of 'copy_positions' in the 'struct config_options'. This function "
                "should only be called when 'copy_positions' is set to 0", __FUNCTION__);
        return EXIT_FAILURE;
    }

    // Now sort the particles based on their original index in the input arrays
    // That will re-order the particles back into the original input order!
#define MULTIPLE_ARRAY_EXCHANGER(type,a,i,j) {                          \
        SGLIB_ARRAY_ELEMENTS_EXCHANGER(float, X, i, j);                \
        SGLIB_ARRAY_ELEMENTS_EXCHANGER(float, Y, i, j);                \
        SGLIB_ARRAY_ELEMENTS_EXCHANGER(float, Z, i, j);                \
        SGLIB_ARRAY_ELEMENTS_EXCHANGER(int64_t, original_indices, i, j); \
        for(int w = 0; w < weights->num_weights; w++) {                 \
            SGLIB_ARRAY_ELEMENTS_EXCHANGER(float, ((float *) weights->weights[w]), i, j); \
        }                                                               \
    }

    int64_t num_sorted = 1;//an array with 1 element is always sorted
    for(int64_t ii=0;ii<np-1;ii++) {
        num_sorted += original_indices[ii + 1] >= original_indices[ii] ? +1:-1;
    }

    //the list is already sorted -> nothing to do
    if(num_sorted == np) {
        return EXIT_SUCCESS;
    }

    //Since the particles might be coming from an already sorted array - quicksort might degenerate to
    //an O(N^2) process -- use the heap-sort when the array is mostly sorted
    if(num_sorted >= FRACTION_SORTED_REQD_TO_HEAP_SORT * np) {
        SGLIB_ARRAY_HEAP_SORT(int64_t, original_indices, np, SGLIB_NUMERIC_COMPARATOR, MULTIPLE_ARRAY_EXCHANGER);
    } else {
        SGLIB_ARRAY_QUICK_SORT(int64_t, original_indices, np, SGLIB_NUMERIC_COMPARATOR, MULTIPLE_ARRAY_EXCHANGER);
    }
#undef MULTIPLE_ARRAY_EXCHANGER

    return EXIT_SUCCESS;
}



int reorder_particles_mocks_back_into_original_order_float(const int64_t np, int64_t *original_indices, weight_struct *weights)
{
    if(original_indices == NULL || weights == NULL) {
        fprintf(stderr,"Error: In %s> While re-ordering the particles back into their input order, the passed pointers "
                "can not be NULL. May be this function does not need to be called ?\n"
                "Please check the value of 'copy_positions' in the 'struct config_options'. This function "
                "should only be called when 'copy_positions' is set to 0", __FUNCTION__);
        return EXIT_FAILURE;
    }

    // Now sort the particles based on their original index in the input arrays
    // That will re-order the particles back into the original input order!
#define MULTIPLE_ARRAY_EXCHANGER(type,a,i,j) {                          \
        SGLIB_ARRAY_ELEMENTS_EXCHANGER(int64_t, original_indices, i, j); \
        for(int w = 0; w < weights->num_weights; w++) {                 \
            SGLIB_ARRAY_ELEMENTS_EXCHANGER(float, ((float *) weights->weights[w]), i, j); \
        }                                                               \
    }

    int64_t num_sorted = 1;//an array with 1 element is always sorted
    for(int64_t ii=0;ii<np-1;ii++) {
        num_sorted += original_indices[ii + 1] >= original_indices[ii] ? +1:-1;
    }

    //the list is already sorted -> nothing to do
    if(num_sorted == np) {
        return EXIT_SUCCESS;
    }

    //Since the particles might be coming from an already sorted array - quicksort might degenerate to
    //an O(N^2) process -- use the heap-sort when the array is mostly sorted
    if(num_sorted >= FRACTION_SORTED_REQD_TO_HEAP_SORT * np) {
        SGLIB_ARRAY_HEAP_SORT(int64_t, original_indices, np, SGLIB_NUMERIC_COMPARATOR, MULTIPLE_ARRAY_EXCHANGER);
    } else {
        SGLIB_ARRAY_QUICK_SORT(int64_t, original_indices, np, SGLIB_NUMERIC_COMPARATOR, MULTIPLE_ARRAY_EXCHANGER);
    }
#undef MULTIPLE_ARRAY_EXCHANGER

    return EXIT_SUCCESS;
}



void find_min_and_max_sqr_sep_between_cell_pairs_float(const float first_xbounds[2], const float first_ybounds[2], const float first_zbounds[2],
                                                        const float second_xbounds[2], const float second_ybounds[2], const float second_zbounds[2],
                                                        float *sqr_sep_min, float *sqr_sep_max)
{
    float min_sqr_sep = ZERO;

    if (first_xbounds[0] > second_xbounds[1]) min_sqr_sep += (first_xbounds[0] - second_xbounds[1])*(first_xbounds[0] - second_xbounds[1]);
    if (second_xbounds[0] > first_xbounds[1]) min_sqr_sep += (second_xbounds[0] - first_xbounds[1])*(second_xbounds[0] - first_xbounds[1]);

    if (first_ybounds[0] > second_ybounds[1]) min_sqr_sep += (first_ybounds[0] - second_ybounds[1])*(first_ybounds[0] - second_ybounds[1]);
    if (second_ybounds[0] > first_ybounds[1]) min_sqr_sep += (second_ybounds[0] - first_ybounds[1])*(second_ybounds[0] - first_ybounds[1]);

    if (first_zbounds[0] > second_zbounds[1]) min_sqr_sep += (first_zbounds[0] - second_zbounds[1])*(first_zbounds[0] - second_zbounds[1]);
    if (second_zbounds[0] > first_zbounds[1]) min_sqr_sep += (second_zbounds[0] - first_zbounds[1])*(second_zbounds[0] - first_zbounds[1]);

    const float xmin = MIN(first_xbounds[0], second_xbounds[0]);
    const float xmax = MAX(first_xbounds[1], second_xbounds[1]);

    const float ymin = MIN(first_ybounds[0], second_ybounds[0]);
    const float ymax = MAX(first_ybounds[1], second_ybounds[1]);

    const float zmin = MIN(first_zbounds[0], second_zbounds[0]);
    const float zmax = MAX(first_zbounds[1], second_zbounds[1]);

    const float max_sqr_sep = (xmax - xmin) * (xmax - xmin) + (ymax - ymin) * (ymax - ymin) + (zmax - zmin) * (zmax - zmin);

    *sqr_sep_min = min_sqr_sep;
    *sqr_sep_max = max_sqr_sep;

}
