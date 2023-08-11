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


#region Import Modules #############################################################

# Krita Modules
from krita import *
# PyQt5 Modules
from PyQt5 import QtWidgets, QtCore, QtGui, uic

#endregion
#region Global Variables ###########################################################

# Plugin
EXTENSION_ID = 'pykrita_eraser_shift'
MENU_ENTRY = 'Eraser Shift'
eraser_shift_version = "2023_08_11"
# Variables
check_timer = 200
print_state = False

#endregion


class EraserShift_Extension( Extension ):
    """
    Eraser and Brush shortcuts
    """

    #region Initialize #############################################################
    def __init__( self, parent ):
        super().__init__( parent )
    def setup( self ):
        # Variables
        self.update = True
        self.mode = "BRUSH" # "BRUSH" "ERASER"

        # Brush
        self.brush_name = None
        self.brush_preset = None
        # Eraser
        self.eraser_name = None
        self.eraser_preset = None

        # Timer
        self.Timer()
    def Timer( self ):
        self.timer_pulse = QtCore.QTimer( self )
        self.timer_pulse.timeout.connect( self.Preset_Updater )
        self.timer_pulse.start( check_timer )
    def Preset_Updater( self ):
        if self.update == True:
            try:
                # Variables
                view = Krita.instance().activeWindow().activeView()
                name = view.currentBrushPreset().name()
                eraser = Krita.instance().action( "erase_action" ).isChecked()
                # Logic
                if self.mode == "BRUSH" and self.brush_name != name:
                    # Variables
                    self.brush_name = name
                    self.brush_preset = Application.resources( "preset" )[self.brush_name]
                    # Update
                    self.Eraser_State( eraser, False )
                    self.Print_State()
                elif self.mode == "ERASER" and self.eraser_name != name:
                    # Variables
                    self.eraser_name = name
                    self.eraser_preset = Application.resources( "preset" )[self.eraser_name]
                    # Update
                    self.Eraser_State( eraser, True )
                    self.Print_State()
            except:
                pass
    def Mode_Display( self, mode ):
        if mode == "BRUSH":
            Krita.instance().activeWindow().activeView().showFloatingMessage( "Brush Mode", Krita.instance().icon( "draw-freehand" ), 1000, 0 )
        if mode == "ERASER":
            Krita.instance().activeWindow().activeView().showFloatingMessage( "Eraser Mode", Krita.instance().icon( "draw-eraser" ), 1000, 0 )
    def Eraser_State( self, mode, state ):
        if mode != state:
            Krita.instance().action( "erase_action" ).setChecked( state )
    def Print_State( self ):
        if print_state == True:
            try:QtCore.qDebug( f"Eraser Shift | mode={self.mode} | brush={self.brush_name} | eraser={self.eraser_name}" )
            except:pass

    #endregion
    #region Actions ################################################################

    def createActions( self, window ):
       # Create Menu
        action_eraser_shift = window.createAction( "eraser_shift_menu", "Eraser Shift", "tools/scripts" )
        menu_eraser_shift = QtWidgets.QMenu( "eraser_shift_menu", window.qwindow() )
        action_eraser_shift.setMenu(menu_eraser_shift)
        # Create Action
        action_brush = window.createAction( EXTENSION_ID + "_brush_key", "Brush", "tools/scripts/eraser_shift_menu")
        action_eraser = window.createAction( EXTENSION_ID + "_eraser_key", "Eraser", "tools/scripts/eraser_shift_menu")
        # Connect
        action_brush.triggered.connect( self.BRUSH_MODE )
        action_eraser.triggered.connect( self.ERASER_MODE )

    #endregion
    #region Functions ##############################################################

    def BRUSH_MODE( self ):
        # Variables
        self.update = False
        self.mode = "BRUSH"
        # Presets
        Krita.instance().activeWindow().activeView().setCurrentBrushPreset( self.brush_preset )
        Krita.instance().action( "KritaShape/KisToolBrush" ).trigger()
        Krita.instance().action( "erase_action" ).setChecked( False )
        # Variables
        self.update = True
        self.Mode_Display( self.mode )

    def ERASER_MODE( self ):
        # Variables
        self.update = False
        self.mode = "ERASER"
        # Presets
        Krita.instance().activeWindow().activeView().setCurrentBrushPreset( self.eraser_preset )
        Krita.instance().action( "KritaShape/KisToolBrush" ).trigger()
        Krita.instance().action( "erase_action" ).setChecked( True )
        # Variables
        self.update = True
        self.Mode_Display( self.mode )

    #endregion