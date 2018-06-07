# reFLAC
Program to re-encode FLAC files to reduce file size.

## What this does
This program runs metaflac and flac on a folder of FLAC files to re-encode them with the newest FLAC, as well as (optionally) strip unnecessary tags, album art, and padding.

### Requirements
The metaflac and flac programs are expected to be in your environment path.

### Options
- "--folder=...": Specify the folder to search for FLAC files to process.
- "--no-strip-art": Disable stripping album art from metadata. Not recommended; simply use a single cover.jpg, folder.jpg, etc to cover all the files in the folder.
- "--no-strip-tags": Disable stripping tags deemed useless, such as "COMMENT".
- "--no-strip-padding": Disable stripping extra padding in the file. Not recommended unless you plan on adding new tags in the future for some reason.
- "--no-reencode": Disable re-encoding all files. Generally you should only use this if you know the files you're modifying were already encoded with the newest version of FLAC.
