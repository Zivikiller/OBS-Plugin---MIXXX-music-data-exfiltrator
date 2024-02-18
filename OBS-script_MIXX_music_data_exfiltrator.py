# OBS-Studio python script "MIXXX now playing data exfiltrator"
# Copyright (C) 2018 IBM
# Copyright (C) 2018 Jim

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# This scripts only works in combination with an installed DJ software named MIXXX. BTW very cooooool project.
# This simple script extract the data of the window title of MIXXX and copy it into 2 different text objects you have to prepare.
# The sign "-" in the window title works as a separator.
# This window title will be updated by MIXXX automaticly for eample when you use the cross fade - try it ;-)
# Combine this script with loop videos and pictures and nice font settings to have a nice look and feel.
# You shoud try and add the OBS "spectalizer"-Pluigin additionaly - this will blow your mind.
# The script was created with the hello world example from OBS-Plugin tutorial. Try to create your own plugins, too. Makes fun!!

# Have a lot of fun and greetings from Dortmund (Germany) where brew companies are older than the united states... prost! :-D 

import obspython as obs

source_name_title = ""
source_name_artist = ""

### For MIXXX windows text data exfiltration
import os
import time


# ------------------------------------------------------------

def script_description():
	return "This plugin extract the title and artist meta data from MIXXX.\r\n\r\n" \
"MIXXX is a very cool DJ mixxer based on open source.\r\n\r\n" \
"I created this plug in to provide current music data for my guest on my DJ parties." \
"In combination with half transperent loop videos and nice pic backgrounds and\r\n\r\n" \
"the cool obs-spectralizer plug in you can create realy cool scence for a separated TV or monitor."


def refresh_pressed(props, prop):
    """
    Called when the 'refresh' button defined below is pressed
    """
    print("Refresh Pressed")
    update_text()


def update_text():
    global source_name_title, source_name_artist

    source_title = obs.obs_get_source_by_name(source_name_title)
    source_artist = obs.obs_get_source_by_name(source_name_artist)
    
    #Extract data from MIXXX
    sCommand = "xdotool search --name \"\| Mixxx\" getwindowname | cut -d\| -f1 | sed 's/,/ -/' | awk '{ print tolower($0) }' | ascii2uni -aU -q|awk '{ print toupper($0) }' | sed 's/$/          /'"
    stream = os.popen(sCommand)
    output = stream.read()
   
    einzeldaten = output.split("-", 1)

    
    if source_title is not None:
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", einzeldaten[1])
        obs.obs_source_update(source_title, settings)
        obs.obs_data_release(settings)
        obs.obs_source_release(source_title)

    if source_artist is not None:
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", einzeldaten[0])
        obs.obs_source_update(source_artist, settings)
        obs.obs_data_release(settings)
        obs.obs_source_release(source_artist)


# ------------------------------------------------------------


def script_properties():
    """
    Called to define user properties associated with the script. These
    properties are used to define how to show settings properties to a user.
    """
    props = obs.obs_properties_create()
    p_title = obs.obs_properties_add_list(props, "source_title", "Text object for title",
                                    obs.OBS_COMBO_TYPE_EDITABLE,
                                    obs.OBS_COMBO_FORMAT_STRING)
                                    
    p_artist = obs.obs_properties_add_list(props, "source_artist", "Text object for artist",
                                    obs.OBS_COMBO_TYPE_EDITABLE,
                                    obs.OBS_COMBO_FORMAT_STRING)
                                    
    sources = obs.obs_enum_sources()
    
    # Loop for Title
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_id(source)
            if source_id == "text_gdiplus" or source_id == "text_ft2_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p_title, name, name)

        obs.source_list_release(sources)

    obs.obs_properties_add_button(props, "button", "Refresh", refresh_pressed)
       
    return props


def script_update(settings):
    """
    Called when the script’s settings (if any) have been changed by the user.
    """
    global source_name_title, source_name_artist

    source_name_title = obs.obs_data_get_string(settings, "source_title")
    source_name_artist = obs.obs_data_get_string(settings, "source_artist")

    print("Script Update wurde gedrückt")

    obs.timer_remove(update_text)
    obs.timer_add(update_text, 2 * 1000) # Every 2 seconds artist and title information will be updated
