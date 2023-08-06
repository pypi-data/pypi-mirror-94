
/**************************************************************************
 *                                                                        *
 *  Regina - A Normal Surface Theory Calculator                           *
 *  Computational Engine                                                  *
 *                                                                        *
 *  Copyright (c) 1999-2021, Ben Burton                                   *
 *  For further details contact Ben Burton (bab@debian.org).              *
 *                                                                        *
 *  This program is free software; you can redistribute it and/or         *
 *  modify it under the terms of the GNU General Public License as        *
 *  published by the Free Software Foundation; either version 2 of the    *
 *  License, or (at your option) any later version.                       *
 *                                                                        *
 *  As an exception, when this program is distributed through (i) the     *
 *  App Store by Apple Inc.; (ii) the Mac App Store by Apple Inc.; or     *
 *  (iii) Google Play by Google Inc., then that store may impose any      *
 *  digital rights management, device limits and/or redistribution        *
 *  restrictions that are required by its terms of service.               *
 *                                                                        *
 *  This program is distributed in the hope that it will be useful, but   *
 *  WITHOUT ANY WARRANTY; without even the implied warranty of            *
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU     *
 *  General Public License for more details.                              *
 *                                                                        *
 *  You should have received a copy of the GNU General Public             *
 *  License along with this program; if not, write to the Free            *
 *  Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston,       *
 *  MA 02110-1301, USA.                                                   *
 *                                                                        *
 **************************************************************************/

#include "maths/binom.h"

namespace {
    const int choose0[1]   = { 1 };
    const int choose1[2]   = { 1,1 };
    const int choose2[3]   = { 1,2,1 };
    const int choose3[4]   = { 1,3,3,1 };
    const int choose4[5]   = { 1,4,6,4,1 };
    const int choose5[6]   = { 1,5,10,10,5,1 };
    const int choose6[7]   = { 1,6,15,20,15,6,1 };
    const int choose7[8]   = { 1,7,21,35,35,21,7,1 };
    const int choose8[9]   = { 1,8,28,56,70,56,28,8,1 };
    const int choose9[10]  = { 1,9,36,84,126,126,84,36,9,1 };
    const int choose10[11] = { 1,10,45,120,210,252,210,120,45,10,1 };
    const int choose11[12] = { 1,11,55,165,330,462,462,330,165,55,11,1 };
    const int choose12[13] = { 1,12,66,220,495,792,924,792,495,220,66,12,1 };
    const int choose13[14] = { 1,13,78,286,715,1287,1716,1716,1287,715,286,78,13,1 };
    const int choose14[15] = { 1,14,91,364,1001,2002,3003,3432,3003,2002,1001,364,91,14,1 };
    const int choose15[16] = { 1,15,105,455,1365,3003,5005,6435,6435,5005,3003,1365,455,105,15,1 };
    const int choose16[17] = { 1,16,120,560,1820,4368,8008,11440,12870,11440,8008,4368,1820,560,120,16,1 };
}

namespace regina {
namespace detail {

    const int* const binomSmall_[17] = {
        choose0, choose1, choose2, choose3, choose4, choose5, choose6, choose7,
        choose8, choose9, choose10, choose11, choose12, choose13, choose14,
        choose15, choose16
    };

} // namespace regina::detail

long binomMedium(int n, int k) {
    if (n <= 16)
        return binomSmall(n, k);

    if (k + k > n)
        k = n - k;

    long ans = 1;
    for (int i = 1; i <= k; ++i) {
        ans *= (n + 1 - i);
        ans /= i;
    }
    return ans;
}

} // namespace regina

