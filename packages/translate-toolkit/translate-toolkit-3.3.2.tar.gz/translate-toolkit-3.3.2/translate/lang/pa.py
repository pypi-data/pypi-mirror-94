#
# Copyright 2010 Zuza Software Foundation
#
# This file is part of the Translate Toolkit.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

"""This module represents the Punjabi language.

.. seealso:: http://en.wikipedia.org/wiki/Punjabi_language
"""


import re

from translate.lang import common


class pa(common.Common):
    """This class represents Punjabi."""

    sentenceend = "।!?…"

    sentencere = re.compile(
        r"""(?s)    # make . also match newlines
                            .*?         # anything, but match non-greedy
                            [%s]        # the puntuation for sentence ending
                            \s+         # the spacing after the puntuation
                            (?=[^a-z\d])# lookahead that next part starts with
                                        # caps
                            """
        % sentenceend,
        re.VERBOSE,
    )

    puncdict = {
        ". ": "। ",
        ".\n": "।\n",
    }

    ignoretests = {
        "all": ["simplecaps", "startcaps"],
    }
