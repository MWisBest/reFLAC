#! /usr/bin/python3
###########################################################################
## reFLAC                                                                ##
## Copyright (C) 2017-2018, Kyle Repinski                                ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
###########################################################################
import subprocess, sys, os, platform, shlex

# Version check.
pyversion = platform.python_version_tuple()
if ( int( pyversion[0] ) < 3 ) or ( int( pyversion[0] ) == 3 and int( pyversion[1] ) < 5 ):
	print( "reFLAC is only tested on Python 3.5 and up. Proceed at your own risk!" )
	input( "Press enter to continue..." )


opts = {
	"folder" : "",
	"re-encode" : True,
	"strip-art" : True,
	"strip-tags" : True,
	"strip-padding" : True
}

stripTagList = [
	"Media", "Release Type", "Catalog",
	"ORGANIZATION", "Related",
	"Rip Date", "Retail Date",
	"comment", "COMMENT", "NOTES",
	"DESCRIPTION",
	"Language", "COPYRIGHT",
	"Encoder", "Ripping Tool"
]



for entry in sys.argv:
	if entry == "--no-strip-art":
		opts['strip-art'] = False
	elif entry == "--no-strip-tags":
		opts['strip-tags'] = False
	elif entry == "--no-strip-padding":
		opts['strip-padding'] = False
	elif entry == "--no-reencode":
		opts['re-encode'] = False
	elif entry.startswith( "--folder=" ):
		opts['folder'] = entry.partition( "=" )[2]



def escapeFilename( name ):
	ret = shlex.quote( name )
	# shlex.quote does weird things with apostrophes
	if '\'"\'"\'' in ret:
		ret = ret.replace( '\'"\'"\'', "'" )
	ret = list( ret )
	if ret[0] == "'":
		ret[0] = '"'
	if ret[-1] == "'":
		ret[-1] = '"'
	ret = "".join( ret )
	return ret



def getfilesandfolders( dir ):
	folders = os.scandir( dir )
	files = []
	for entry in folders:
		if entry.is_file():
			if entry.name.endswith( ".flac" ):
				files.append( escapeFilename( dir + os.path.sep + entry.name ) )
		elif entry.is_dir():
			files.extend( getfilesandfolders( dir + os.path.sep + entry.name ) )
	return files




if opts['folder'] != "" and os.path.isdir( opts['folder'] ):
	files = getfilesandfolders( opts['folder'] )
	workingdir = os.getcwd()
	print( str( files ) )
	if opts['strip-art']:
		baseCmd = "metaflac --remove --block-type=PICTURE "
		for file in files:
			subprocess.run( baseCmd + file, cwd=workingdir )
	if opts['strip-tags']:
		baseCmd = "metaflac "
		for tag in stripTagList:
			baseCmd += "--remove-tag=\"" + tag + "\" "
		for file in files:
			subprocess.run( baseCmd + file, cwd=workingdir )
	if opts['strip-padding']:
		baseCmd = "metaflac --remove --block-type=PADDING --dont-use-padding "
		for file in files:
			subprocess.run( baseCmd + file, cwd=workingdir )
	if opts['re-encode']:
		baseCmd = "flac -8 -f "
		if opts['strip-padding']:
			baseCmd += "--no-padding "
		for file in files:
			subprocess.run( baseCmd + file + " --output-name=" + file, cwd=workingdir )
else:
	print( "Folder not specified or is not a folder" )
