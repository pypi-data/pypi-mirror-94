#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2019  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with damejson; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

import unittest
import json
import pandas as pd
from xml.dom import minidom

import xml.etree.ElementTree as ET

class TestDameJson(unittest.TestCase):

    def test_damexml_getelementsbytagname(self):
        # using read and loads to open
        xmldoc = minidom.parse('files/items.xml')
        itemlist = xmldoc.getElementsByTagName('item')
        self.assertEqual(len(itemlist), 4)
        l = []
        for s in itemlist:
            l.append(s.attributes['name'].value)
        self.assertEqual(l, ['item1', 'item2', 'item3', 'item4'])

    def test_damexml_rss_titles(self):
        tree = ET.parse('files/rss.xml')
        l = []
        for elem in tree.iter():
            if (elem.tag == "title"):
                l.append(elem.text)
        self.assertEqual(l[0:2], ["Richard Stallman's Political Notes", 'Economic growth and fossil fuels'])


if __name__ == '__main__':
    unittest.main()
