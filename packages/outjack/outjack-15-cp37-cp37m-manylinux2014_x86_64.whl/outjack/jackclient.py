# Copyright 2017, 2020 Andrzej Cichocki

# This file is part of outjack.
#
# outjack is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# outjack is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with outjack.  If not, see <http://www.gnu.org/licenses/>.

from . import cjack
from lagoon import jack_control
from lagoon.program import partial
import sys

jackctl = jack_control[partial](stdout = sys.stderr)

class JackClient:

    def __init__(self, clientname, chancount, ringsize, coupling):
        self.clientname = clientname
        self.chancount = chancount
        self.ringsize = ringsize
        self.coupling = coupling

    def start(self):
        self.startjack = jackctl.status(check = False)
        if self.startjack:
            jackctl.start()
        # XXX: Use an explicit character encoding?
        self.jack = cjack.Client(self.clientname.encode(), self.chancount, self.ringsize, self.coupling)
        # Your app should tune itself to satisfy these values:
        self.outputrate = self.jack.get_sample_rate()
        self.buffersize = self.jack.get_buffer_size()

    def port_register_output(self, port_name):
        self.jack.port_register_output(port_name.encode())

    def activate(self):
        self.jack.activate()

    def connect(self, source_port_name, destination_port_name):
        self.jack.connect(source_port_name.encode(), destination_port_name.encode())

    def current_output_buffer(self):
        return self.jack.current_output_buffer()

    def send_and_get_output_buffer(self):
        return self.jack.send_and_get_output_buffer()

    def deactivate(self):
        self.jack.deactivate()

    def stop(self):
        self.jack.dispose()
        if self.startjack:
            jackctl.stop()
