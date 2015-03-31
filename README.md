#google-ip-checker

This script checks the Google SPF records and Google Cloud SPF records for changes in IP blocks.

When a change is detected - whether a block is added or removed, or a combination of both - an email is sent to addresses defined in the script with the information.

sendmail must be enabled on the machine to work. SMTP options could be changed to use a Google Account.

The script just stores the results in text files as JSON, and also creates a log file.

To run the script ad-hoc...
```bash
$ python google_ip_check.py
```

We put the following task to be run by cron.
```bash
00 * * * * python google_ip_check/google_ip_check.py
```
