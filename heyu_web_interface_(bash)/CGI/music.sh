#!/usr/bin/env bash
set -f

# Author: 	Kris Beazley
# Online: 	http://heyu.epluribusunix.net/
# Online email: http://heyu.epluribusunix.net/?contactus

echo Content-Type:Text/Html
echo

QUERY_STRING=${QUERY_STRING/heyu_music=/}


[[ $QUERY_STRING == mpgstop ]] && killall -9 mpg123
[[ $QUERY_STRING == *pls || $QUERY_STRING == *m3u || $QUERY_STRING == *:* ]] && mpg123 -@ $QUERY_STRING
[[ $QUERY_STRING == *amixer_set* ]] && amixer -q set Master ${QUERY_STRING/amixer_set_}



echo "
<html>
  <head>

   </head>
   <body bgcolor=#E5E5E5>
      <div id=content>

<a href=?heyu_music=mpgstop>Stop</a><br><br>
<a href=?heyu_music=amixer_set_0%>Volume 0%</a> | <a href=?heyu_music=amixer_set_45%>Volume 45%</a> | <a href=?heyu_music=amixer_set_55%>Volume 55%</a> |<br> 
<a href=?heyu_music=amixer_set_65%>Volume 65%</a> | <a href=?heyu_music=amixer_set_75%>Volume 75%</a> | <a href=?heyu_music=amixer_set_85%>Volume 85%</a> | 
<a href=?heyu_music=amixer_set_100%>Volume 100%</a>

<br><br>

<a href=?heyu_music=http://somafm.com/groovesalad.pls>Groove Salad</a> | <a href=?heyu_music=http://somafm.com/lush.pls>Lush</a> | <a href=?heyu_music=http://somafm.com/folkfwd.pls>Folk Forward</a>
<br><br>

<a href=?heyu_music=http://somafm.com/bagel.pls>BAGeL Radio</a> | <a href=?heyu_music=http://somafm.com/digitalis.pls>Digitalis</a> | <a href=?heyu_music=http://somafm.com/indiepop.pls>Indi Pop Rocks!</a>
<br><br>

<a href=?heyu_music=http://somafm.com/poptron.pls>PopTron</a> | <a href=?heyu_music=http://somafm.com/u80s.pls>Underground 80s</a> | <a href=?heyu_music=http://somafm.com/covers.pls>Covers</a>
<br><br>

<a href=?heyu_music=http://somafm.com/secretagent.pls>Secret Agent</a> | <a href=?heyu_music=http://somafm.com/suburbsofgoa.pls>Suburbs of Goa</a> | <a href=?heyu_music=http://somafm.com/beatblender.pls>Beat Blender</a>
<br><br>

<a href=?heyu_music=http://somafm.com/illstreet.pls>Illinois Street Lounge</a> | <a href=?heyu_music=http://somafm.com/dubstep.pls>Dub Step</a> | <a href=?heyu_music=http://somafm.com/bootliquor.pls>Boot Liquor</a>
<br><br>

<a href=?heyu_music=http://somafm.com/sxfm.pls>South of Soma</a> | 
<a href=?heyu_music=http://radioboxhd.com/streampanel/tunein.php/jsorrent/playlist.pls>Z100 #1 Pop Music</a> | 
<a href=?heyu_music=http://149.255.33.74:8104>Mega Shuffle.com</a>

<br><br>

<a href=?heyu_music=http://blackbeats.fm/listen.m3u>Black Beats.fm</a> | <a href=?heyu_music=http://www.radioparadise.com/m3u/mp3-128.m3u>Radio Paradise.com</a> | 

</body></html>"





