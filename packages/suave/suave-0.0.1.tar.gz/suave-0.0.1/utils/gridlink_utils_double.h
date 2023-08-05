/* This file is auto-generated from gridlink_utils.h.src */
#ifndef DOUBLE_PREC
#define DOUBLE_PREC
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
#include "weight_defs_double.h" //for definition of weight_struct

    extern int get_binsize_double(const double xmin,const double xmax,
                                  const double rmax,
                                  const int refine_factor, const int max_ncells, double *xbinsize, int *nlattice,
                                  const struct config_options *options) __attribute__((warn_unused_result));

    extern void get_max_min_double(const int64_t ND1, const double * restrict X1, const double * restrict Y1, const double * restrict Z1,
                                   double *min_x, double *min_y, double *min_z, double *max_x, double *max_y, double *max_z);

    extern int reorder_particles_back_into_original_order_double(const int64_t np, int64_t *original_indices, double *X,
                                                                 double *Y, double *Z, weight_struct *weights);

    extern int reorder_particles_mocks_back_into_original_order_double(const int64_t np, int64_t *original_indices, weight_struct *weights);

    extern void get_max_min_ra_dec_double(const int64_t ND1, const double *RA, const double *DEC,
                                          double *ra_min, double *dec_min, double *ra_max, double *dec_max);

    extern double find_closest_pos_double(const double first_xbounds[2], const double second_xbounds[2], double *closest_pos0)__attribute__((warn_unused_result));

    extern void find_min_and_max_sqr_sep_between_cell_pairs_double(const double first_xbounds[2], const double first_ybounds[2], const double first_zbounds[2],
                                                                   const double second_xbounds[2], const double second_ybounds[2], const double second_zbounds[2],
                                                                   double *sqr_sep_min, double *sqr_sep_max);


#define CHECK_AND_CONTINUE_FOR_DUPLICATE_NGB_CELLS_double(icell, icell2, num_cell_pairs, num_ngb_this_cell, all_cell_pairs) { \
        int duplicate_flag = 0;                                         \
        XRETURN(num_cell_pairs - num_ngb_this_cell >= 0, NULL,          \
                "Error: While working on detecting (potential) duplicate cell-pairs on primary cell = %"PRId64"\n" \
                "The total number of cell-pairs (across all primary cells) = %"PRId64" should be >= the number of cell-pairs for " \
                "this primary cell = %"PRId64"\n", icell, num_cell_pairs, num_ngb_this_cell); \
                                                                        \
        for(int jj=0;jj<num_ngb_this_cell;jj++) {                       \
            struct cell_pair_double *this_cell_pair = &all_cell_pairs[num_cell_pairs - jj - 1]; \
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
