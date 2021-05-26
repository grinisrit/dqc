/*
 * Copyright (C) 2013-  Qiming Sun <osirpt.sun@gmail.com>
 * Description: code generated by  gen-code.cl
 */
#include <stdlib.h>
#include "cint_bas.h"
#include "cart2sph.h"
#include "g1e.h"
#include "g2e.h"
#include "optimizer.h"
#include "cint1e.h"
#include "cint2e.h"
#include "misc.h"
#include "c2f.h"

/* based on
 * '("int1e_r2_origi" ( r dot r \| ))
 */
static void CINTgout1e_int1e_r2_origi(double *gout, double *g, FINT *idx, CINTEnvVars *envs, FINT empty) {
        FINT nf = envs->nf;
        FINT ix, iy, iz, n;
        double *g0 = g;
        double *g1 = g0  + envs->g_size * 3;
        double *g2 = g1  + envs->g_size * 3;
        double *g3 = g2  + envs->g_size * 3;
        double s;
        G1E_R_I(g1, g0, envs->i_l+1, envs->j_l, 0);
        G1E_R_I(g3, g1, envs->i_l+0, envs->j_l, 0);
        for (n = 0; n < nf; n++) {
                ix = idx[0+n*3];
                iy = idx[1+n*3];
                iz = idx[2+n*3];
                s = g3[ix+0]*g0[iy+0]*g0[iz+0];
                s+= g0[ix+0]*g3[iy+0]*g0[iz+0];
                s+= g0[ix+0]*g0[iy+0]*g3[iz+0];
                gout[n] += s;
        }
}
void int1e_r2_origi_optimizer(CINTOpt **opt, FINT *atm, FINT natm, FINT *bas, FINT nbas, double *env) {
        FINT ng[] = {2, 0, 0, 0, 2, 1, 1, 1};
        CINTall_1e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
FINT int1e_r2_origi_cart(double *out, FINT *dims, FINT *shls,
                FINT *atm, FINT natm, FINT *bas, FINT nbas, double *env, CINTOpt *opt, double *cache) {
        FINT ng[] = {2, 0, 0, 0, 2, 1, 1, 1};
        CINTEnvVars envs;
        CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
        envs.f_gout = &CINTgout1e_int1e_r2_origi;
        return CINT1e_drv(out, dims, &envs, cache, &c2s_cart_1e, 0);
} // int1e_r2_origi_cart
FINT int1e_r2_origi_sph(double *out, FINT *dims, FINT *shls,
                FINT *atm, FINT natm, FINT *bas, FINT nbas, double *env, CINTOpt *opt, double *cache) {
        FINT ng[] = {2, 0, 0, 0, 2, 1, 1, 1};
        CINTEnvVars envs;
        CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
        envs.f_gout = &CINTgout1e_int1e_r2_origi;
        return CINT1e_drv(out, dims, &envs, cache, &c2s_sph_1e, 0);
} // int1e_r2_origi_sph
FINT int1e_r2_origi_spinor(double complex *out, FINT *dims, FINT *shls,
                FINT *atm, FINT natm, FINT *bas, FINT nbas, double *env, CINTOpt *opt, double *cache) {
        FINT ng[] = {2, 0, 0, 0, 2, 1, 1, 1};
        CINTEnvVars envs;
        CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
        envs.f_gout = &CINTgout1e_int1e_r2_origi;
return CINT1e_spinor_drv(out, dims, &envs, cache, &c2s_sf_1e, 0);
} // int1e_r2_origi_spinor
ALL_CINT1E(int1e_r2_origi)

/* based on
 * '("int1e_r4_origi" ( r dot r r dot r \| ))
 */
static void CINTgout1e_int1e_r4_origi(double *gout, double *g, FINT *idx, CINTEnvVars *envs, FINT empty) {
        FINT nf = envs->nf;
        FINT ix, iy, iz, n;
        double *g0 = g;
        double *g1 = g0  + envs->g_size * 3;
        double *g2 = g1  + envs->g_size * 3;
        double *g3 = g2  + envs->g_size * 3;
        double *g4 = g3  + envs->g_size * 3;
        double *g5 = g4  + envs->g_size * 3;
        double *g6 = g5  + envs->g_size * 3;
        double *g7 = g6  + envs->g_size * 3;
        double *g8 = g7  + envs->g_size * 3;
        double *g9 = g8  + envs->g_size * 3;
        double *g10 = g9  + envs->g_size * 3;
        double *g11 = g10  + envs->g_size * 3;
        double *g12 = g11  + envs->g_size * 3;
        double *g13 = g12  + envs->g_size * 3;
        double *g14 = g13  + envs->g_size * 3;
        double *g15 = g14  + envs->g_size * 3;
        double s;
        G1E_R_I(g1, g0, envs->i_l+3, envs->j_l, 0);
        G1E_R_I(g3, g1, envs->i_l+2, envs->j_l, 0);
        G1E_R_I(g4, g0, envs->i_l+1, envs->j_l, 0);
        G1E_R_I(g7, g3, envs->i_l+1, envs->j_l, 0);
        G1E_R_I(g12, g4, envs->i_l+0, envs->j_l, 0);
        G1E_R_I(g15, g7, envs->i_l+0, envs->j_l, 0);
        for (n = 0; n < nf; n++) {
                ix = idx[0+n*3];
                iy = idx[1+n*3];
                iz = idx[2+n*3];
                s = g15[ix+0]*g0[iy+0]*g0[iz+0];
                s+= g12[ix+0]*g3[iy+0]*g0[iz+0] * 2;
                s+= g12[ix+0]*g0[iy+0]*g3[iz+0] * 2;
                s+= g0[ix+0]*g15[iy+0]*g0[iz+0];
                s+= g0[ix+0]*g12[iy+0]*g3[iz+0] * 2;
                s+= g0[ix+0]*g0[iy+0]*g15[iz+0];
                gout[n] += s;
        }
}
void int1e_r4_origi_optimizer(CINTOpt **opt, FINT *atm, FINT natm, FINT *bas, FINT nbas, double *env) {
        FINT ng[] = {4, 0, 0, 0, 4, 1, 1, 1};
        CINTall_1e_optimizer(opt, ng, atm, natm, bas, nbas, env);
}
FINT int1e_r4_origi_cart(double *out, FINT *dims, FINT *shls,
                FINT *atm, FINT natm, FINT *bas, FINT nbas, double *env, CINTOpt *opt, double *cache) {
        FINT ng[] = {4, 0, 0, 0, 4, 1, 1, 1};
        CINTEnvVars envs;
        CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
        envs.f_gout = &CINTgout1e_int1e_r4_origi;
        return CINT1e_drv(out, dims, &envs, cache, &c2s_cart_1e, 0);
} // int1e_r4_origi_cart
FINT int1e_r4_origi_sph(double *out, FINT *dims, FINT *shls,
                FINT *atm, FINT natm, FINT *bas, FINT nbas, double *env, CINTOpt *opt, double *cache) {
        FINT ng[] = {4, 0, 0, 0, 4, 1, 1, 1};
        CINTEnvVars envs;
        CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
        envs.f_gout = &CINTgout1e_int1e_r4_origi;
        return CINT1e_drv(out, dims, &envs, cache, &c2s_sph_1e, 0);
} // int1e_r4_origi_sph
FINT int1e_r4_origi_spinor(double complex *out, FINT *dims, FINT *shls,
                FINT *atm, FINT natm, FINT *bas, FINT nbas, double *env, CINTOpt *opt, double *cache) {
        FINT ng[] = {4, 0, 0, 0, 4, 1, 1, 1};
        CINTEnvVars envs;
        CINTinit_int1e_EnvVars(&envs, ng, shls, atm, natm, bas, nbas, env);
        envs.f_gout = &CINTgout1e_int1e_r4_origi;
        return CINT1e_spinor_drv(out, dims, &envs, cache, &c2s_sf_1e, 0);
} // int1e_r4_origi_spinor
ALL_CINT1E(int1e_r4_origi)
//ALL_CINT1E_FORTRAN_(int1e_r4_origi)