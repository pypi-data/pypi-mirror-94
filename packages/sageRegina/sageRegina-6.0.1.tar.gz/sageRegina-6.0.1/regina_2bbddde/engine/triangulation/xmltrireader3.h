
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

/*! \file triangulation/xmltrireader3.h
 *  \brief Deals with parsing XML data for 3-dimensional triangulation packets.
 */

#ifndef __XMLTRIREADER3_H
#ifndef __DOXYGEN
#define __XMLTRIREADER3_H
#endif

#include "regina-core.h"
#include "triangulation/xmltrireader.h"

namespace regina {

/**
 * \weakgroup triangulation
 * @{
 */

/**
 * An XML packet reader that reads a single 3-dimensional triangulation.
 *
 * This is a specialisation of the generic XMLTriangulationReader class
 * template; see the XMLTriangulationReader documentation for an
 * overview of how this class works.
 *
 * This 3-dimensional specialisation contains extra functionality for
 * reading optional properties specific to 3-dimensional triangulations.
 */
template <>
class REGINA_API XMLTriangulationReader<3> :
        public detail::XMLTriangulationReaderBase<3> {
    public:
        /**
         * Creates a new triangulation reader.
         *
         * @param resolver the master resolver that will be used to fix
         * dangling packet references after the entire XML file has been read.
         */
        XMLTriangulationReader(XMLTreeResolver& resolver);

        /**
         * Returns an XML element reader for the given optional property of a
         * <i>dim</i>-dimensional triangulation.
         *
         * If \a subTagName names an XML element that describes an optional
         * property of a triangulation (such as \c H1 or \c fundgroup for
         * 3-manifold triangulations), then this function should return
         * a corresponding element reader.
         *
         * Otherwise this function should return a new XMLElementReader,
         * which will cause the XML element to be ignored.
         *
         * @param subTagName the name of the XML subelement opening tag.
         * @param subTagProps the properties associated with the
         * subelement opening tag.
         * @return a newly created element reader that will be used to
         * parse the subelement.  This class should not take care of the
         * new reader's destruction; that will be done by the parser.
         */
        XMLElementReader* startPropertySubElement(
            const std::string& subTagName,
            const regina::xml::XMLPropertyDict& subTagProps);
};

/*@}*/

// Inline functions for XMLTriangulationReader<3>

inline XMLTriangulationReader<3>::XMLTriangulationReader(
        XMLTreeResolver& resolver) :
        detail::XMLTriangulationReaderBase<3>(resolver) {
}

} // namespace regina

#endif

