#!/usr/bin/python
#
# Regina - A Normal Surface Theory Calculator
# Alternate implementations of command-line utilities for the MacOS app bundle
#
# Copyright (c) 2002-2021, Ben Burton
# For further details contact Ben Burton (bab@debian.org).
#
# This implementation is designed for the Xcode bundle only - it hard-codes
# paths to the census databases that are specific to the bundle layout.
# In all other settings, you should use the standard implementations
# of these utilities from the utils/ directory of Regina's source tree.
#
# This script should not be called directly.  Instead use the symlinks
# within the MacOS folder in the app bundle (which call regutils-launch,
# which then runs this script in the correct python runtime).
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# As an exception, when this program is distributed through (i) the
# App Store by Apple Inc.; (ii) the Mac App Store by Apple Inc.; or
# (iii) Google Play by Google Inc., then that store may impose any
# digital rights management, device limits and/or redistribution
# restrictions that are required by its terms of service.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the Free
# Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston,
# MA 02110-1301, USA.

# In regfiletype we use print(..., end=''), which is a python3ism.
from __future__ import print_function

import os
import sys
import string

appName = sys.argv[1]
appDir = os.path.abspath(os.path.dirname(sys.argv[0]) + '/../..')

def globalUsage(error):
    if error:
        sys.stderr.write('ERROR: ' + error + '\n\n')
    sys.stderr.write('Please call this script through the symlinks provided in the MacOS directory.\n');
    sys.exit(1)

try:
    sys.path = [ appDir + '/MacOS/python' ] + sys.path
    import regina
except:
    globalUsage('Could not import the regina module.')

regina.GlobalDirs.setDirs('', '', appDir + '/Resources')

if appName == 'censuslookup':
    def usage(error):
        if error:
            sys.stderr.write(error + '\n\n')

        sys.stderr.write('Usage:\n')
        sys.stderr.write('    ' + sys.argv[1] + ' <isosig> ...\n')
        sys.exit(1)

    if len(sys.argv) < 3:
        usage('Please specify one or more isomorphism signatures.')

    for sig in sys.argv[2:]:
        hits = regina.Census.lookup(sig)

        n = hits.count()
        if n == 1:
            print(sig + ': 1 hit')
        else:
            print(sig + ':', n, 'hits')

        hit = hits.first()
        while hit:
            print('    ' + hit.name() + ' -- ' + hit.db().desc())
            hit = hit.next()

        print()

elif appName == 'regconcat':
    def usage(error):
        if error:
            sys.stderr.write(error + '\n\n')

        sys.stderr.write('Usage:\n')
        sys.stderr.write('    ' + sys.argv[1] + \
            ' [ -o <output-file> ] <data-file> ...\n\n')
        sys.stderr.write('    -o <output-file> : Write to the given data file (otherwise standard\n')
        sys.stderr.write('                       output is used)\n')
        sys.exit(1)

    # Parse the command line.
    files = []
    outputFile = None

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '-o':
            if i == len(sys.argv) - 1:
                usage('Option -o is missing an output filename.')
            elif outputFile:
                usage('More than one output filename has been supplied.')
            i = i + 1
            outputFile = sys.argv[i]
        elif sys.argv[i][:1] == '-':
            usage('Invalid option: ' + sys.argv[i])
        elif sys.argv[i]:
            files.append(sys.argv[i])
        else:
            usage('Empty arguments are not allowed.')

        i = i + 1

    if not files:
        usage('No data files have been supplied.')

    # Read the input files one by one.
    ans = regina.Container()
    ans.setLabel('Combined Data')

    error = False
    for f in files:
        data = regina.open(f)
        if not data:
            sys.stderr.write('File ' + f + ' could not be read.\n')
            error = True
        else:
            ans.insertChildLast(data)

    # Tidy up the final data file and write it.
    if not outputFile:
        ans.writeXMLFile()
    elif not ans.save(outputFile):
        sys.stderr.write('File ' + outputFile + ' could not be written.\n')
        error = True

    if error:
        sys.exit(1)

elif appName == 'regconvert':
    def usage(error):
        if error:
            sys.stderr.write(error + '\n\n')

        sys.stderr.write('Usage:\n')
        sys.stderr.write('    ' + sys.argv[1] + ' [ -x | -u ] <old-file> [ <new-file> ]\n\n')
        sys.stderr.write('    -x : Convert to compressed XML (default)\n')
        sys.stderr.write('    -u : Convert to uncompressed XML\n\n')
        sys.stderr.write('    <new-file> may be the same as <old-file>.\n')
        sys.stderr.write('    <new-file> defaults to standard output (implies -u).\n')
        sys.exit(1)

    oldFile = None
    newFile = None
    typeOpt = None

    for arg in sys.argv[2:]:
        if arg == '-u' or arg == '-x':
            if typeOpt:
                usage('More than one file type has been specified.')
            typeOpt = arg[1]
        elif arg[:1] == '-':
            usage('Invalid option: ' + arg)
        elif arg == '':
            usage('Empty arguments are not allowed.')
        elif not oldFile:
            oldFile = arg
        elif not newFile:
            newFile = arg
        else:
            usage('More than two files have been specified.')

    if not oldFile:
        usage('No files have been specified.')

    # Add default options.
    if not typeOpt:
        if newFile:
            typeOpt = 'x'
        else:
            typeOpt = 'u'

    # Check we're allowed to use stdout if we've asked for it.
    if (not newFile) and (typeOpt != 'u'):
        usage('Only uncompressed XML can be written to standard output.')

    # Read the old file.
    tree = regina.open(oldFile)
    if not tree:
        sys.stderr.write('File ' + oldFile + ' could not be read.\n')
        sys.exit(1)

    # Write the new file.
    if not newFile:
        tree.writeXMLFile()
    elif not tree.save(newFile, (typeOpt == 'x')):
        sys.stderr.write('File ' + newFile + ' could not be written.\n')
        sys.exit(1)

elif appName == 'regfiledump':
    def usage(error):
        if error:
            sys.stderr.write(error + '\n\n')

        sys.stderr.write('Usage:\n')
        sys.stderr.write('    ' + sys.argv[1] + ' [ -f | -l | -n ] [ -c ] <file> [ <packet-label> ... ]\n\n')
        sys.stderr.write('    -f : Display full packet details (default)\n')
        sys.stderr.write('    -l : Only display packet labels and types\n')
        sys.stderr.write("    -n : Don't display packets at all (implies -c)\n")
        sys.stderr.write('\n')
        sys.stderr.write('    -c : Finish with a count of all packets in the file\n\n')
        sys.stderr.write('    <packet-label> ... : Only display the listed packets (otherwise all\n')
        sys.stderr.write('                         packets are displayed)\n')
        sys.exit(1)

    separator = "************************************************************";

    def dumpNoPacket(label, opt):
        if opt == 'l':
            print('ERROR:', label, '-- No such packet.')
        elif opt == 'f':
            print(separator)
            print('*')
            print('* ERROR:', label)
            print('*        No such packet.')
            print('*')
            print(separator)
            print()

    def dumpPacketHeader(p):
        print(separator)
        print('*')
        print('* Label:', p.humanLabel())
        print('* Type:', p.typeName())
        if p.parent():
            print('* Parent:', p.parent().humanLabel())
        else:
            print('* Parent: (none)')
        if p.hasTags():
            print('* Tags:', ', '.join(p.tags()))
        print('*')
        print(separator)

    def dumpPacket(p, opt):
        if opt == 'l':
            print(p.fullName())
        elif opt == 'f':
            dumpPacketHeader(p)
            print()
            print(p.detail())
            print()

    filename = None
    packets = []
    opt = None
    count = False

    # Parse command line.
    for arg in sys.argv[2:]:
        if arg == '-c':
            count = True
        elif arg == '-f' or arg == '-l' or arg == '-n':
            if opt:
                usage('More than one detail level has been specified.')
            opt = arg[1]
        elif arg[:1] == '-':
            usage('Invalid option: ' + arg)
        elif not arg:
            usage('Empty arguments are not allowed.')
        elif filename:
            packets.append(arg)
        else:
            filename = arg

    if not filename:
        usage('No file has been specified.')

    # Add default options.
    if not opt:
        opt = 'f'
    if opt == 'n':
        count = True

    if opt == 'n' and packets:
        usage('You cannot specify individual packets if packets are not to be displayed.')

    # In the python implementation we will just write international characters
    # in utf8, and hope that the terminal is sufficiently modern to cope.

    # Do the actual work.
    tree = regina.open(filename)
    if not tree:
        sys.stderr.write('File ' + filename + ' could not be read.\n')
        sys.exit(1)

    if opt != 'n':
        if not packets:
            p = tree
            while p:
                dumpPacket(p, opt)
                p = p.nextTreePacket()
        else:
            for i in packets:
                p = tree.findPacketLabel(i)
                if p:
                    dumpPacket(p, opt)
                else:
                    dumpNoPacket(i, opt)

    if count:
        if opt != 'n':
            print()
        print(tree.totalTreeSize(), 'total packets in file.')

elif appName == 'regfiletype':
    def usage(error):
        if error:
            sys.stderr.write(error + '\n\n')

        sys.stderr.write('Usage:\n')
        sys.stderr.write('    ' + sys.argv[1] + ' <file> ...\n')
        sys.exit(1)

    if len(sys.argv) < 3:
        usage('Please specify one or more files.')

    for f in sys.argv[2:]:
        if len(sys.argv) > 3:
            print('[', f, ']')

        info = regina.FileInfo.identify(f)
        if info:
            print(info.detail(), end='')
        else:
            print('Unknown file format or file could not be opened.')

        if len(sys.argv) > 3:
            print()

elif appName == 'trisetcmp':
    def usage(error):
        if error:
            sys.stderr.write(error + '\n\n')

        sys.stderr.write('Usage:\n')
        sys.stderr.write('    ' + sys.argv[1] + ' [ -m | -n ] [ -s ] <file1.rga> <file2.rga>\n\n')
        sys.stderr.write('    -m : List matches, i.e., triangulations contained in both files (default)\n')
        sys.stderr.write('    -n : List non-matches, i.e., triangulations in one file but not the other\n')
        sys.stderr.write('    -s : Allow triangulations from file1.rga to be subcomplexes of\n')
        sys.stderr.write('         triangulations from file2.rga\n')
        sys.exit(1)

    subcomplexTesting = False

    def isTri(t):
        return t.type() == regina.PACKET_TRIANGULATION3 or \
            t.type() == regina.PACKET_TRIANGULATION4

    def compare(t1, t2):
        if subcomplexTesting:
            return t1.isContainedIn(t2)
        else:
            return t1.isIsomorphicTo(t2)

    def runMatches(tree1, tree2):
        if subcomplexTesting:
            print('Matching (isomorphic subcomplex) triangulations:')
            op = '<='
        else:
            print('Matching (isomorphic) triangulations:')
            op = '=='
        print()

        nMatches = 0

        p1 = tree1
        while p1:
            if isTri(p1):
                p2 = tree2
                while p2:
                    if p2.type() == p1.type():
                        if compare(p1, p2):
                            print('    ' + p1.humanLabel() + '  ' + op + \
                                '  ' + p2.humanLabel())
                            nMatches = nMatches + 1
                    p2 = p2.nextTreePacket()
            p1 = p1.nextTreePacket()

        if nMatches == 0:
            print('No matches found.')
        elif nMatches == 1:
            print()
            print('1 match.')
        else:
            print()
            print(nMatches, 'matches.')

    def runNonMatches(file1, tree1, file2, tree2):
        print('Triangulations in ' + file1 + ' but not ' + file2 + ':')
        print()

        nMissing = 0

        p1 = tree1
        while p1:
            if isTri(p1):
                matched = False
                p2 = tree2
                while p2 and not matched:
                    if p2.type() == p1.type():
                        if compare(p1, p2):
                            matched = True
                    p2 = p2.nextTreePacket()
                if not matched:
                    print('    ' + p1.humanLabel())
                    nMissing = nMissing + 1
            p1 = p1.nextTreePacket()

        if nMissing == 0:
            print('All triangulations matched.')
        elif nMissing == 1:
            print()
            print('1 non-match.')
        else:
            print()
            print(nMissing, 'non-matches.')

    # Parse command line.
    listMatches = False
    listNonMatches = False
    noMoreOpts = False
    file1 = None
    file2 = None

    for arg in sys.argv[2:]:
        if not noMoreOpts:
            if arg == '-m':
                listMatches = True
                continue
            elif arg == '-n':
                listNonMatches = True
                continue
            elif arg == '-s':
                subcomplexTesting = True
                continue
            elif arg == '--':
                noMoreOpts = True
                continue
            elif arg[:1] == '-':
                usage('Invalid option: ' + arg)
        if arg:
            noMoreOpts = True
            if not file1:
                file1 = arg
            elif not file2:
                file2 = arg
            else:
                usage('You may not pass more than two data files.')
        else:
            usage('Empty arguments are not allowed.')

    if listMatches and listNonMatches:
        usage('Options -n and -m may not be used together.')
    if not (listMatches or listNonMatches):
        # List matches by default.
        listMatches = True

    if not (file1 and file2):
        usage('Two data files must be specified.')

    # Open the two data files.
    tree1 = regina.open(file1)
    if not tree1:
        sys.stderr.write('File ' + file1 + ' could not be read.\n')
        sys.stderr.write('Please check that it exists and that it is a Regina data file.\n')
        sys.exit(1)

    tree2 = regina.open(file2)
    if not tree2:
        sys.stderr.write('File ' + file2 + ' could not be read.\n')
        sys.stderr.write('Please check that it exists and that it is a Regina data file.\n')
        sys.exit(1)

    # In the python implementation we will just write international characters
    # in utf8, and hope that the terminal is sufficiently modern to cope.

    # Run our tests.
    if listMatches:
        runMatches(tree1, tree2)
    else:
        runNonMatches(file1, tree1, file2, tree2)
        if not subcomplexTesting:
            print()
            print('--------------------')
            print()
            runNonMatches(file2, tree2, file1, tree1)

else:
    globalUsage('"' + appName + '" is not one of Regina\'s command-line utilities.')
