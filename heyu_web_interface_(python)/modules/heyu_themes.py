#! /usr/bin/env python
#
#   Author: 	Kris Beazley
#   Copyright 2012 Kris Beazley

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#       http://www.apache.org/licenses/LICENSE-2.0

#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#   Apache License, Version 2.0 http://www.apache.org/licenses/LICENSE-2.0

import cgitb, sys, subprocess, urllib2
cgitb.enable()
sys.path.append('./modules')
import heyu

def theme_default(data, x10config, x10sched, x10report, heyu_path, HC, auto_refresh):
    print("""

    <table><tr><td>
    <h4 style=\"font-family:Tahoma\">HEYU WEB INTERFACE </h4>

    <!-- Begin Form For Control Panel, Show All Modules, and Auto Refresh Buttons -->

    <form method="post">
    <button type=button class=scene_button onclick=\"Status(); show('control_panel_@{x10_config}')\">
    <table class=scene_button><tr><td class=scene_button>
    <img src=\"imgs/tool.png\" alt=none class=icons>
    Control Panel</table></button>

    <button type=submit name=Button2 value=show_all_modules class=scene_button onclick=\"Status(); show('')\">
    <table class=scene_button><tr><td class=scene_button>
    <img src=\"imgs/horizon.png\" alt=none class=icons>
    Show All Modules</table></button>

    <button id=refresh type=submit name=Button3 value=auto_refresh class=scene_button onclick=\"Status(); show('auto_refresh')\">
    <table class=scene_button><tr><td class=scene_button>
    <img src=\"imgs/reload.png\" alt=none class=icons>
    Auto Refresh
    """)
    
    def _refresh_():
        try:
            if heyu.sub_refresh():
                return heyu.sub_refresh()
        except:
            return "10"
            
    auto_refresh = auto_refresh.replace("False","")
    auto_refresh = auto_refresh.replace("True", _refresh_() + "s")
    print auto_refresh
    print("""
            </table></button>
            <!-- Close form -->
            </form>
            </table>
            <br>""")
    ### Start Scenes and UserSyns
    print("""
         <!-- Begin Form For Scenes and Aliases -->
         <form method=\"post\">
         <h4 style=\"font-family:Tahoma\">SCENES</h4>""")

    
    i = subprocess.Popen([heyu_path, '-c', x10config, 'webhook', 'config_dump'], stdout=subprocess.PIPE)
    i = i.communicate()
    i = i[0]
    i = i.split('\n')
    for x in i:
        if 'usersyn' in x or 'scene' in x:
            x = x.split(None, 2)
            name = x[1]
            name = name.replace("_"," ")
            cmds = x[2]
            print "<button type=button class=scene_button onclick=\"Status(); show('heyu_do_cmd " + cmds + "')\">"
            print "<table class=scene_button><tr><td class=scene_button><img src=\"imgs/scenes.png\" alt=none class=icons>"
            print name, "<br></table></button>"
 
    ### Aliases
    ### Use _addr_ for multiple units / alias
    ### Try modtype object because it is not an obsolute.
    ### Test if ',' is in object because it would mean a multiple unit object and should be sliced to show info like dimelevel and timestamps
    

    print("""
            <br><h4 style=\"font-family:Tahoma\">ALIASES</h4>""")
    
    # Set z for formating HTML rows/columns
    z = 0
    
    i = subprocess.Popen([heyu_path, '-c', x10config, 'webhook', 'config_dump'], stdout=subprocess.PIPE)
    i = i.communicate()
    i = i[0]
    i = i.split('\n')   
   
    for x in i:
        if 'alias' in x:
            x = x.split()
            unit = x[1]
            unit = unit.replace("_"," ")
            addr = x[2]
            _addr_ = x[2]
            
            addr = addr.replace("_"," ")            

            try:
                modtype  = x[3]
                modtype  = modtype.lower()
            except:
                modtype = ""  
            

            if ',' in addr:
                addr = addr[:3]              

     
            ### Call heyu and get on/off status and slice strings
                       
            process = subprocess.Popen([heyu_path, '-c', x10config, 'onstate', addr], stdout=subprocess.PIPE)
            status = process.communicate()
            status = status[0]        
            on_icon = status.replace("1","<img src=\"imgs/on2.png\" class=icons>")
            on_icon = on_icon.replace("0","")        
            xstatus = status.replace("1","off")
            xstatus = xstatus.replace("0","on")
            xstatus = xstatus.rstrip() 
            status = status.replace("1","<font class=info_on_color>On,</font>")
            status = status.replace("0","<font class=info_off_color>Off</font>")
        
            # Call heyu and get dimlevel.
            dimlevel = subprocess.Popen([heyu_path, '-c', x10config, 'dimlevel', addr], stdout=subprocess.PIPE)
            dimlevel = dimlevel.communicate()
            dimlevel = dimlevel[0]
            dimlevel = dimlevel.rstrip()
        
            # Call heyu and get time stamp and slice strings.
            timestamp = subprocess.Popen([heyu_path, '-c', x10config , 'show', 'tstamp', addr], stdout=subprocess.PIPE)
            timestamp = timestamp.communicate()
            try:
                timestamp = timestamp[0]
                timestamp = timestamp.split(' ')
                day = timestamp[1]
                time = timestamp[3]
                month = timestamp[5]
                mday = timestamp[6]
                year = timestamp[7]
                
                print "<table class=button align=left><tr><td class=button>"
                    
                
                print "<button type=button class=scene_button onclick=\"Status(); show('heyu_do_cmd " + xstatus, _addr_ + "')\">"
                print "<table class=button><tr><td class=button>" + on_icon + unit
        
                # Info part of the button
                print "<td class=info>", _addr_, status, dimlevel + "&#37; Power", "<br>", month, mday + ",", time, "<br></table></button>"
                
                try: 
                    if modtype == 'stdlm':
                        rawlevel = subprocess.Popen([heyu_path, '-c', x10config , 'rawlevel', addr], stdout=subprocess.PIPE) 
                        rawlevel = rawlevel.communicate()
                        rawlevel = rawlevel[0]
                        rawlevel = rawlevel.strip()
                        # removing the last integer is the same as dividing by 10
                        rawlevel = rawlevel[:-1]                    
                        if rawlevel == "":
                                rawlevel = '0'
                        if 'html_range=True' in heyu.cookies():
                            print "<tr><td class=button><input type=range min=0 max=21 class=sliderfx value=\"" + rawlevel  + "\" step=1 onclick=\"Status(); show('heyu_do_cmd rheo", addr, "' + value + '", rawlevel + "')\"></table>" 
                        else:
                            r1 = int(rawlevel) - 3
                            r2 = int(rawlevel) + 3
                            print "<tr><td class=button><img src=./imgs/down.png class=pbi onclick=\"Status(); show('heyu_do_cmd rheo", addr, r1, rawlevel + "')\"><progress class=pb value=\"" + rawlevel  + "\" max=21></progress><img src=./imgs/up.png class=pbi onclick=\"Status(); show('heyu_do_cmd rheo", addr, r2, rawlevel + "')\"></table>"
            
                    else:
                        z = z+1
                        print "<tr><td class=button></table>"
                except:
                    print "<tr><td class=button></table>"
                # For html formatting rows/columns
                z = z+1
                
                if z == 3:
                    print "&nbsp; "
                    z = 0
                

                                                                                                                                  

                    

            except:
                z = "error"
    if 'error' == z:
        print("<pre>Error: The script ran into a problem.")
        print("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Check your error.log for additonal information.</pre>")
        print("<form method=POST><input type=submit value=Retry>")
        del z
         
    
    print("""
                <!-- Close Form and Div -->
                </form>
                    </table>
                </table>
            </div>
        </body>
    </html>""")
    



def compact_theme1(x10config, x10sched, heyu_path, HC):

    print("""
            <form method=post><select name=states onChange=\"goPage(this.options[this.selectedIndex].value)\" size=1>
            <option value=#>Heyu
            <optgroup label=SCENES>""")

    print("""
            <!-- Begin Form For Scenes and Aliases -->
            <form method=post>
            <h4 style=\"font-family:Tahoma\">SCENES</h4>""")
            
    i = subprocess.Popen([heyu_path, '-c', x10config, 'webhook', 'config_dump'], stdout=subprocess.PIPE)
    i = i.communicate()
    i = i[0]
    i = i.split('\n')
    for x in i:
        if 'usersyn' in x or 'scene' in x:
            x = x.split(None, 2)
            name = x[1]
            name = name.replace("_"," ")
            cmds = x[2]
            print "<option value=\"?heyu_do_cmd " + cmds + "\"> " + name
 
       
    print "</optgroup><optgroup label=ALIASES>"
    

    i = subprocess.Popen([heyu_path, '-c', x10config, 'webhook', 'config_dump'], stdout=subprocess.PIPE)
    i = i.communicate()
    i = i[0]
    i = i.split('\n')   
   
    for x in i:
        if 'alias' in x:
            x = x.split()
            unit = x[1]
            unit = unit.replace("_"," ")
            addr = x[2]
            _addr_ = x[2]
            addr = addr.replace("_"," ")
            
            # Test for multiple addresses
            if ',' in addr:		
	            addr = addr[:3] 

            # Call heyu and get on/off status and slice strings
            process = subprocess.Popen([heyu_path, '-c', x10config, 'onstate', addr], stdout=subprocess.PIPE)
            status = process.communicate()
            status = status[0]        
            xstatus = status.replace("1","off")
            xstatus = xstatus.replace("0","on")
            xstatus = xstatus.rstrip() 
            status = status.replace("1","- On")
            status = status.replace("0","- Off")
            print "<option value=\"?heyu_do_cmd " + xstatus, _addr_ + "\">" + unit, status

   
    
    print(""" </optgroup>
			<optgroup label=CONFIG>
			<option value=?control_panel_@{x10_config}>Control Panel""")

    print "<option value=?heyu_do_cmd%20allon%20" + HC + ">All Units On"
    print "<option value=?heyu_do_cmd%20alloff%20" + HC + ">All Units Off"
    print "<option value=?heyu_do_cmd%20kill_all_hc>All Units Off A-P"
    print "</optgroup></select></form>"
    print "<form method=post><button class=userconfigbutton type=button onclick=\"Status(); show('heyu_theme')\"> Change Theme</button></form>"
    
    
