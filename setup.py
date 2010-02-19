#!/usr/bin/env python

##
#   Project: gWakeOnLan - Wake up your machines using Wake on LAN.
#    Author: Fabio Castelli <muflone@vbsimple.net>
# Copyright: 2009-2010 Fabio Castelli
#   License: GPL-2+
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
# 
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
# 
# On Debian GNU/Linux systems, the full text of the GNU General Public License
# can be found in the file /usr/share/common-licenses/GPL-2.
##

from distutils.core import setup
from distutils.command.install_data import install_data
from distutils.dep_util import newer
from distutils.log import info
import glob
import os
import sys

class InstallData(install_data):
  def run (self):
    self.data_files.extend (self._compile_po_files())
    install_data.run (self)

  def _compile_po_files (self):
    data_files = []

    # Don't install language files on win32
    if sys.platform == 'win32':
      return data_files

    PO_DIR = 'po'
    for po in glob.glob (os.path.join (PO_DIR,'*.po')):
      lang = os.path.basename(po[:-3])
      mo = os.path.join('build', 'mo', lang, 'gwakeonlan.mo')

      directory = os.path.dirname(mo)
      if not os.path.exists(directory):
        info('creating %s' % directory)
        os.makedirs(directory)

      if newer(po, mo):
        # True if mo doesn't exist
        cmd = 'msgfmt -o %s %s' % (mo, po)
        info('compiling %s -> %s' % (po, mo))
        if os.system(cmd) != 0:
          raise SystemExit('Error while running msgfmt')

        dest = os.path.dirname(os.path.join('share', 'locale', lang, 'LC_MESSAGES', 'gwakeonlan.mo'))
        data_files.append((dest, [mo]))

    return data_files


setup(name='gWakeOnLan',
      version='0.4.1',
      description='Wake up your machines using Wake on LAN.',
      author='Fabio Castelli',
      author_email='muflone@vbsimple.net',
      url='http://code.google.com/p/gwakeonlan/',
      license='GPL v2',
      scripts=['gwakeonlan'],
      data_files=[
                  ('share/applications', ['data/gwakeonlan.desktop']),
                  ('share/man/man1', ['man/gwakeonlan.1']),
                  ('share/doc/gwakeonlan', ['doc/README', 'doc/changelog', 'doc/translators']),
                  ('share/gwakeonlan', ['data/gwakeonlan.glade', 'data/gwakeonlan.svg']),
                 ],
      cmdclass={'install_data': InstallData}
     )