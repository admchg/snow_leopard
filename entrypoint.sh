# Start the run once job.
echo "Docker container has been started!"

# Setup a cron schedule
echo "21 * * * * /usr/local/bin/python3.8 /home/snow/inventory.py >> /var/log/cron.log 2>&1
20 * * * * killall -g python3 >> /var/log/cron.log 2>&1
# This extra line makes it a valid cron" > scheduler.txt

crontab scheduler.txt
cron -f
