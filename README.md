# mysql-backup
##
Routine backup of mysql and routine cleanup scripts
##
#Backup Script do:
##
Dumps the entire collection /n
Reads every document from the /n
Converts MongoDB BSON → valid JSON /n
Writes everything into one JSON file /n
<collection-name>_dump_YYYYMMDD_HHMMSS.json /n
Reads file size from disk /n
Sends Discord notification
##
Delete script do: /n
read .json extension file list in ascending date. /n
always keep last 2(adjustable) and delete all. /n
if new backup is off, still it will keep last 2 backup files.

