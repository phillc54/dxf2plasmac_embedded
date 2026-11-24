# dxf2plasmac_embedded
A basic converter from dxf to gcode embedded in a QtPlasmaC tab.

Copy add_dxf2plasmac.py and the dxf2plasmac directory into your QtPlasmaC directory.

Edit the existing inifile by adding the following to the [DISPLAY] section:

    USER_COMMAND_FILE = add_dxf2plasmac.py.

Note: If you have an existing USER_COMMAND_FILE then you will need to copy the code from add_dxf2plasmac.py into the existing file.

There are two python libraries required, ezdxf and shapely.

Bookworm requires these from PyPi as the debian packages are too old.

    pip3 install "ezdxf>=1.4" --break-system-packages
    pip3 install "shapely>=2.0<2.2" --break-system-packages

Trixie can use the debian packages (NOTE: untested as of uploading this repo)

    sudo apt install python3-ezdxf python3-shapely


