#!/usr/bin/env bash
set -f

# Author: 	Kris Beazley
# Copyright     2014 
# Online: 	http://heyu.epluribusunix.net/
# Online email: http://heyu.epluribusunix.net/?contactus
# Licensed under the Apache License, Version 2.0 http://www.apache.org/licenses/LICENSE-2.0

# Define player to use.

player="mpg123 -@"

### If True will send stderr to stdout.  Helpful for not filling up the httpd error logs.  
debug() { exec 2>&1 ; }
dubug="True"

echo Content-Type:Text/Html
echo
[[ ${dubug^^} == TRUE ]] && debug



echo "
<html>
  <head>
  <style type=text/css>
@import url(../heyu_style.css);
</style>
   </head>
      <script type=text/javascript src=/heyu_javascripts/update.js></script>
     <body onload=ajax_update()>

      <div id=content>
      
	<table class=mainplayerbutton><tr><td><table class=control_panel_music><tr>
        <td><B><center>Heyu Web Interface Internet Radio Player (Beta)</B>
        <tr>
        <td><table class=mainplayerbutton><tr><td>"
[[ ! -e currently_playing ]] && touch currently_playing
mapfile data <currently_playing

    while [[ x -lt ${#data[*]} ]]
	do
	if [[ ${data[$x]} == *ICY-URL* ]];then
	  p=${data[$x]}
	  p=${p//ICY-URL: }
	  m=($p)
	  url=${m[0]}	  	  
	fi
	if [[ ${data[$x]} == *ICY-NAME* ]];then
	  p=${data[$x]}
	  p=${p//ICY-NAME: }
	  p=${p//=\'/}
	  p=${p// /_}
	  p=${p//\';/ }
	  m=($p)
	  name=${m[0]}
	  name=${name//_/ }
	fi
        if [[ ${data[$x]} == *Directory* ]];then
	  p=${data[$x]}
	  p=${p//Directory:  }
	  p=${p//=\'/}
	  p=${p// /_}
	  p=${p//\';/ }
	  m=($p)
	  Directory=${m[0]}
	  Directory=${Directory//_/ }
	  Directory=${Directory//Directory: }
	 
	fi
	if [[ ${data[$x]} == *ICY-META* ]];then
	  p=${data[$x]}
	  p=${p//ICY-META: }
	  p=${p/StreamTitle/}
	  p=${p/StreamUrl/}
	  p=${p//=\'/}
	  p=${p// /_}
	  p=${p//\';/ }
	  m=($p)
          title=${m[0]}
	  title=${title//_/ }
	  if [[ -z $url ]];then
	    url=${m[1]}
	    url=${url//_/ }
	  fi
	 fi
	 if [[ ${data[$x]} == *error:* ]];then
	  p=${data[$x]}
	  p=${p// /_}
	  m=($p)
	  error=${m[0]}
	  error=${error//_/ }
	fi
	((x++))
    done  
    
    
vol() {
for l in "$(amixer get Master)"
do
  l=${l// /_}  
  l=${l/_[/ }
  l=${l/]_/ }
  l=($l)
  s="${l[5]}"
  
  #Fix for raspberry pi 
  [[ ${#s} -gt 3 ]] && s="${l[6]}"
  

  soundlevel=${s//%/}
  inc_sound=$(($soundlevel + 5))
  dec_sound=$(($soundlevel - 5))
  echo "<table class=volbutton><tr><td >Vol: ${s}<a href=?heyu_music=amixer_set_$dec_sound%><img src=/imgs/down.png width=25 heigth=25 align=center></a>
  <progress value=\"$soundlevel\" max=100></progress><a href=?heyu_music=amixer_set_$inc_sound%><img src=/imgs/up.png width=25 heigth=25 align=center></a></table>" 

done
}    
if [[ $title ]];then 
echo "<table class=music_fontz1><tr><td><a href=\"https://play.google.com/store/search?q=${title}&c=music\" title=\"Search this artist on Google Play\" target=_BLANK><b>${title}</b></a> 
<br><br>$name - <a href=$url target=_BLANK><b>$url</b></a></font><br><br></table></table>
"
else
echo "<br>"

[[ -s currently_playing ]] && echo "<tr><td align=center>Retrieving Audio Data. Please Wait...<br><br></table>"

fi
if [[ $error ]];then
  echo "<tr><td align=center><br>Audio Failed To Start ~ Please Click The Stop Button And Try Again.<br>"
  #echo "$Directory"
  #echo > currently_playing
  #($player $Directory)>&currently_playing &
  #echo "<meta http-equiv=\"refresh\" content=\"0;url=/?heyu_music=$Directory\""

fi
echo ""
echo "<br></table>"
echo "
<form method=post action=?heyu_music=mpgstop>
  <table class=control_panel_music2><tr>
        <td>
        $(vol) 
        </td>
	<td>
	    <button type=submit class=stop_button><img src=../imgs/alloff.png class=stop_button_img></button></form>
	 </td>
	 </tr>

</table>
</table>"




QUERY_STRING=${QUERY_STRING/heyu_music=/}





[[ -n $QUERY_STRING ]] && [[ $QUERY_STRING != *amixer_set* ]] && [[ $QUERY_STRING != *current_song* ]] && echo > currently_playing



if  [[ -n $QUERY_STRING ]] && [[ $QUERY_STRING != *amixer_set* ]] && [[ $QUERY_STRING != *current_song* ]];then
	(killall -9 ${player% -@})
	### Wait for thread to close.
	wait
	
        echo > currently_playing
	
	([[ $QUERY_STRING == *pls || $QUERY_STRING == *m3u || $QUERY_STRING == *:* ]] && $player $QUERY_STRING)>&currently_playing &
fi

if [[ $QUERY_STRING == *amixer_set* ]];then  
  amixer -q set Master ${QUERY_STRING/amixer_set_}
fi


for line in $(</etc/group); 
  do 
    [[ "$line" == *:$UID:* ]] && USER=${line/:x:$UID:};
done

for line in $(</etc/group); 
  do 

    if [[ "$line" == *audio* ]] && [[ "$line" != *$USER* ]];then
      echo "User \"$USER\" must be added to group Audio. <br> In terminal type command \"sudo usermod -G audio $USER\" to add $USER to group audio.<BR>
      Then restart apache to have the new user settings updated.<br><br>";
    fi

done

is_player_installed=($(${player% -@} --version))
if [[ -z ${is_player_installed[0]} ]];then
  echo "${player% -@} not installed.  Please install it to play music.<br><br>"
fi

echo "  <table class=music_fontz1 width=200><tr><td align=center><b>Playlist</b><tr><td class=playlistbutton>"
while read -r playlist
 do
     p=${playlist//#/ }
     p=($p)
     echo "<a href=\"?heyu_music=$playlist\">${p[*]:1:9}</a><br>"
done <./playlist
echo "</table></table>"


#Debug stream info
#echo "<pre>${data[*]}"

echo "<br>"

echo "</table></div></body></html>"






