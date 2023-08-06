
/**************************************************************************
 *                                                                        *
 *  Regina - A Normal Surface Theory Calculator                           *
 *  Python Interface                                                      *
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

#include "../pybind11/pybind11.h"
#include "split/signature.h"
#include "triangulation/dim3.h"
#include "../helpers.h"

using regina::Signature;

void addSignature(pybind11::module_& m) {
    auto c = pybind11::class_<Signature>(m, "Signature")
        .def(pybind11::init<const Signature&>())
        .def("order", &Signature::order)
        .def_static("parse", &Signature::parse)
        .def("triangulate", &Signature::triangulate)
        .def("writeCycles", [](const Signature& sig,
                const std::string& cycleOpen, const std::string& cycleClose,
                const std::string& cycleJoin) {
            sig.writeCycles(std::cout, cycleOpen, cycleClose, cycleJoin);
        })
    ;
    regina::python::add_output(c);
    regina::python::add_eq_operators(c);

    m.attr("NSignature") = m.attr("Signature");
}

