#!/usr/bin/env python

# matchline: Comparing sequences of points in 2 dimensions.
# Copyright (C) 2009-2012 Specific Purpose Software GmbH
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; NO OTHER VERSION than version 2.0 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from ZSI import dispatch
import zsiTools
import zsiServer

import server_include
#: This will launch a SOAP server.
def run(port=server_include.server_port):
    dispatch.AsServer(port,modules=(zsiServer,),typesmodule=zsiTools,rpc=True)
    """ Default port can be found in server_include or supplied in run command """

if __name__ == "__main__":
    run()
