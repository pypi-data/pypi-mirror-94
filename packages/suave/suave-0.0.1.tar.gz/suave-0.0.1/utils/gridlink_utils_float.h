/* This file is auto-generated from gridlink_utils.h.src */
#ifdef DOUBLE_PREC
#undef DOUBLE_PREC
#endif
// # -*- mode: c -*-
/* File: gridlink_utils.h.src */
/*
  This file is a part of the Corrfunc package
  Copyright (C) 2015-- Manodeep Sinha (manodeep@gmail.com)
  License: MIT LICENSE. See LICENSE file under the top-level
  directory at https://github.com/manodeep/Corrfunc/
*/

#pragma once

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif


#include "defs.h" //for definition of config_options
#include "weight_defs_float.h" //for definition of weight_struct

    extern int get_binsize_float(const float xmin,const float xmax,
                                  const float rmax,
                                  const int refine_factor, const int max_ncells, float *xbinsize, int *nlattice,
                                  const struct config_options *options) __attribute__((warn_unused_result));

    extern void get_max_min_float(const int64_t ND1, const float * restrict X1, const float * restrict Y1, const float * restrict Z1,
                                   float *min_x, float *min_y, float *min_z, float *max_x, float *max_y, float *max_z);

    extern int reorder_particles_back_into_original_order_float(const int64_t np, int64_t *original_indices, float *X,
                                                                 float *Y, float *Z, weight_struct *weights);

    extern int reorder_particles_mocks_back_into_original_order_float(const int64_t np, int64_t *original_indices, weight_struct *weights);

    extern void get_max_min_ra_dec_float(const int64_t ND1, const float *RA, const float *DEC,
                                          float *ra_min, float *dec_min, float *ra_max, float *dec_max);

    extern float find_closest_pos_float(const float first_xbounds[2], const float second_xbounds[2], float *closest_pos0)__attribute__((warn_unused_result));

    extern void find_min_and_max_sqr_sep_between_cell_pairs_float(const float first_xbounds[2], const float first_ybounds[2], const float first_zbounds[2],
                                                                   const float second_xbounds[2], const float second_ybounds[2], const float second_zbounds[2],
                                                                   float *sqr_sep_min, float *sqr_sep_max);


#define CHECK_AND_CONTINUE_FOR_DUPLICATE_NGB_CELLS_float(icell, icell2, num_cell_pairs, num_ngb_this_cell, all_cell_pairs) { \
        int duplicate_flag = 0;                                         \
        XRETURN(num_cell_pairs - num_ngb_this_cell >= 0, NULL,          \
                "Error: While working on detecting (potential) duplicate cell-pairs on primary cell = %"PRId64"\n" \
                "The total number of cell-pairs (across all primary cells) = %"PRId64" should be >= the number of cell-pairs for " \
                "this primary cell = %"PRId64"\n", icell, num_cell_pairs, num_ngb_this_cell); \
                                                                        \
        for(int jj=0;jj<num_ngb_this_cell;jj++) {                       \
            struct cell_pair_float *this_cell_pair = &all_cell_pairs[num_cell_pairs - jj - 1]; \
            XRETURN(this_cell_pair->cellindex1 == icell, NULL,          \
                    "Error: While working on detecting (potential) duplicate cell-pairs on primary cell = %"PRId64"\n" \
                    "For cell-pair # %"PRId64", the primary cellindex (within cell-pair) = %"PRId64" should be *exactly* " \
                    "equal to current primary cellindex = %"PRId64". Num_cell_pairs = %"PRId64" num_ngb_this_cell = %"PRId64"\n", \
                    icell, num_cell_pairs - jj, this_cell_pair->cellindex1, icell, num_cell_pairs, num_ngb_this_cell); \
            if (this_cell_pair->cellindex2 == icell2) {                 \
                duplicate_flag = 1;                                     \
                break;                                                  \
            }                                                           \
        }                                                               \
        if(duplicate_flag == 1) continue;                               \
    }





#ifdef __cplusplus
}
#endif
