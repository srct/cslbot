# Copyright (C) 2013-2015 Samuel Damashek, Peter Foley, James Forcier, Srijay Kasturi, Reed Koser, Christopher Reffett, and Fox Wilson
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import time
from .orm import Log


def get_chain(session, nick, limit=0):
    # Search backwards, getting previous nicks for a (optionally) limited amount of time.
    chain = []
    curr_time = time.time()
    curr = nick
    while curr is not None:
        row = session.query(Log).filter(Log.msg == curr, Log.type == 'nick', ~Log.source.startswith('Guest'), Log.time < curr_time, Log.time >= limit).order_by(Log.time.desc()).limit(1).first()
        if row is not None:
            curr = row.source
            chain.append(curr)
            curr_time = row.time
        else:
            curr = None
    if chain:
        chain.insert(0, nick)
    return list(reversed(chain))
