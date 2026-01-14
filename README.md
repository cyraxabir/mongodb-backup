# mysql-backup
##
Routine backup of mysql and routine cleanup scripts
##
#Backup Script do:
##
Dumps the entire collection
Reads every document from the
Converts MongoDB BSON → valid JSON
Writes everything into one JSON file
<collection-name>_dump_YYYYMMDD_HHMMSS.json
Reads file size from disk
Sends Discord notification
##
#Delete script do:
read .json extension file list in ascending date.
always keep last 2(adjustable) and delete all.
if new backup is off, still it will keep last 2 backup files.

