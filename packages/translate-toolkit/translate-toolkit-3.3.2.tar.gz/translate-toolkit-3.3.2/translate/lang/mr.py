#
# Copyright 2010, 2016 Zuza Software Foundation
#
# This file is part of translate.
#
# translate is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# translate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

"""This module represents the Marathi language.

.. seealso:: http://en.wikipedia.org/wiki/Marathi_language
"""


from translate.lang import common


class mr(common.Common):
    """This class represents Marathi."""

    ignoretests = {
        "all": ["simplecaps", "startcaps"],
    }
