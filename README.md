# dxf2plasmac_embedded
A basic converter from dxf to gcode embedded in a QtPlasmaC tab.

Copy add_dxf2plasmac.py and the dxf2plasmac directory from the src directory into your QtPlasmaC directory.

Edit the existing inifile by adding the following to the [DISPLAY] section:

    USER_COMMAND_FILE = add_dxf2plasmac.py.

Note: If you have an existing USER_COMMAND_FILE then you will need to copy the code from add_dxf2plasmac.py into the existing file.

There are two python libraries required, ezdxf and shapely, these can be installed as follows:

    pip3 install ezdxf==1.4.0 --break-system-packages
    pip3 install shapely==2.0.7 --break-system-packages --no-deps

These version are not the latest but are used to keep compatibility with Debian Bookworm.

If you are using Debian Trixie then you could use the versions that install via apt but you will not be able to share saved projects with a Bookworm installation.

    sudo apt install python3-ezdxf
    sudo apt install python3-shapely
