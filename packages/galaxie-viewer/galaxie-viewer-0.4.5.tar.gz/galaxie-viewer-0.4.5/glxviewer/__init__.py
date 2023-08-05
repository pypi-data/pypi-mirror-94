#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html

APPLICATION_AUTHORS = ["Tuuuux"]
APPLICATION_VERSION = '0.4.5'
APPLICATION_NAME = "Galaxie Viewer"
APPLICATION_COPYRIGHT = "2019-2021 - Galaxie Viewer Team all right reserved"
__all__ = ['Viewer', 'viewer']

from glxviewer.viewer import Viewer

viewer = Viewer()
