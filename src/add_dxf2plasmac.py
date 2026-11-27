# add_dxf2plasmac.py

''' customize QtPlasmaC to add dxf2plasmac as a tab

    requires ezdxf and shapely python libraries

    Bookworm requires these from PyPi as the debian packages are too old:
        pip3 install "ezdxf>=1.4" --break-system-packages
        pip3 install "shapely>=2.0<2.2" --break-system-packages --no-deps
    Trixie can use the debian packages (NOTE: untested so far)
        sudo apt install python3-ezdxf python3-shapely
'''

# only run this code for the gui handler file
if hasattr(self.w, 'main_tab_widget'):
    # check dependencies
    from importlib.metadata import PackageNotFoundError, version
    try:
        ezdxf = version('ezdxf')
    except PackageNotFoundError:
        ezdxf = None
    try:
        shapely = version('shapely')
    except PackageNotFoundError:
        shapely = None
    if not ezdxf:
        print('ezdxf module not installed, dxf2plasmac cannot be embedded')
    if not shapely:
        print('shapely module not installed, dxf2plasmac cannot be embedded')
    # dependencies satistied so continue
    if ezdxf and shapely:
        # import the handlerfile to get access to the base classes
        # import hal for hal pin creation
        import qtplasmac_handler as HANDLER
        from qtplasmac_handler import hal as HAL

        # import import the base gui file
        from dxf2plasmac.dxf2plasmac_qt5 import DXFGUI
        # units needed to instantiate dxf2plasmac
        units = 'imperial' if self.units in ['in', 'inch'] else 'metric'
        # instantiate dxf2plasmac with units and icon color
        self.dxf_gui = DXFGUI(units, '#ffee06')
        # insert tab at index #2 containing dxf2plasmac
        self.w.main_tab_widget.insertTab(2, self.dxf_gui, 'DXF CONVERTER')
        # redo main_tab_widget tab indexes
        self.MAIN = 0
        self.CONVERSATIONAL = 1
        self.DXF_CONVERTER = 2
        self.PARAMETERS = 3
        self.SETTINGS = 4
        self.STATISTICS = 5
        # load the material file
        self.dxf_gui.load_material_file(self.materialFile)
        # set default parameters
        self.dxf_gui.D2P.lead_type = 'arc'
        self.dxf_gui.D2P.lead_length = self.PREFS.getpref('Leadin', 0, float, 'CONVERSATIONAL')
        self.dxf_gui.D2P.last_cut = (0.0, 0.0)
        self.dxf_gui.D2P.flattening_distance = 0.025
        self.dxf_gui.D2P.gap_tolerance = 0.001
        self.dxf_gui.D2P.lead_angle = 45
        self.dxf_gui.D2P.precision = 2
        self.dxf_gui.shape_color = '#808000'
        # tickle conversational so we can get the small hole diameter
        self.CONV.conv_setup(self, self.w)
        self.dxf_gui.D2P.small_hole = self.PREFS.getpref('Hole diameter', self.unitCode[2], float, 'CONVERSATIONAL')
        # widen these two as QtPlasmaC styles make the child widgets quite a bit larger than standard
        self.dxf_gui.sidebar_container.setFixedWidth(220)
        self.dxf_gui.menu_width = 190
        # set up the disabling hal pin
        # not sure why I added these after all the work to add the tab
        # but it makes the tab consistant with conversational
        self.dxfTabDisable = self.h.newpin('dxf_disable', HAL.HAL_BOOL, HAL.HAL_IN)
        self.dxfTabDisable.value_changed.connect(lambda v: self.w.main_tab_widget.setTabVisible(self.DXF_CONVERTER, not v))

        # patch handler file main_tab_changed method so the dxf2plasmac tab gets processed
        old_main_tab_changed = self.main_tab_changed
        def main_tab_changed(tab):
            old_main_tab_changed(tab)
            if tab == self.DXF_CONVERTER:
                self.vkb_show(True)
                self.autorepeat_keys(True)
        self.main_tab_changed = main_tab_changed
        # show main page
        self.w.main_tab_widget.setCurrentIndex(self.MAIN)

        # add dxf2plasmac to index-name map for interlock rules
        self.tabNames[self.DXF_CONVERTER] = 'dxf_converter_tab'
        # add dxf2plasmac tab to interlock rules
        HANDLER.INTERLOCK_RULES['dxf_converter_tab'] = {
            'all': {
                'interp_idle': True,
                'manual_cut_active': False,
                'offsets_active': False,
                'probe_test': False
            }
        }
        self.interlockRules = HANDLER.INTERLOCK_RULES.copy()

        # load gcode file in linuxcnc after saving
        def export_gcode():
            self.dxf_gui.export_gcode()
            self.new_load(self.dxf_gui.gcode_file)

        export_btn = self.dxf_gui.toolbar.itemAt(1).widget()
        export_btn.clicked.disconnect()
        export_btn.clicked.connect(export_gcode)
        export_btn.setToolTip('Export Gcode file and open in LinuxCNC')
