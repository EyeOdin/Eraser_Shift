# Eraser Shift is a Krita plugin for Eraser and Brush shortcuts.
# Copyright ( C ) 2023  Ricardo Jeremias.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# ( at your option ) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Import
from .eraser_shift_extension import EraserShift_Extension

# Instantiate your class:
extension = EraserShift_Extension( Krita.instance() )
Krita.instance().addExtension( extension )
