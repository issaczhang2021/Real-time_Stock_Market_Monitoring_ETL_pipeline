#!/bin/sh

# NAME="Issac"

# mkdir test_folder
# cd test_folder
# touch test.txt
# echo "Hello $NAME" >> test.txt

cd /opt/spark/work-dir

echo "Initializing delta table..."
python3 ./godata2023/delta_tables/create_bronze_layer.py

# Tail the log file to keep the container running
tail -f /var/log/cron.log