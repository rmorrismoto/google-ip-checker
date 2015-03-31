# coding: utf-8
import os
import subprocess
import re
import json
import datetime

from send_email import send_mail

FROM_ADDR = "" ## FROM email address here
TO_ADDRS = [] ## TO email addresses here
CC_ADDRS = [] ## CC email addresses here
ADMIN_ADDRS = [] ## Admin emails in case of error

LOGFILE = "log.txt"

SERVICES = [
    {'title': 'mail_spf', 'description': 'Google IP Blocks', 'netblocksUrl': '_spf.google.com'},
    {'title': 'cloud_ips', 'description': 'Google Cloud Platform IP Blocks', 'netblocksUrl': '_cloud-netblocks.googleusercontent.com'},
]

def main():
    log_entry = ""
    for service in SERVICES:
        print "Running the  script for %s . . . " % service.get('description')
        try:
            r_file_title = '%s_results.txt' % service.get('title')
            if r_file_title not in os.listdir('.'):
                results = {'ip4':[], 'ip6': []}
            else:
                results_file = open(r_file_title, 'r')
                results = json.loads(results_file.read())
                results_file.close()
            cmdCall = 'nslookup -q=TXT %s' % service.get('netblocksUrl')
            sample = subprocess.check_output(cmdCall.split(" "))
            regex = re.compile("include:([\w\.\_\-]+)")

            nbUrls = regex.findall(sample)
            new = False

            all_these_ips = set()
            for url in nbUrls:
                cmdCall = 'nslookup -q=TXT %s' % url
                this_sample = subprocess.check_output(cmdCall.split(" "))
                for k in results.keys():
                    thisRegex = re.compile("(\w+):([\w\.\_\/\:]+)")
                    theseResults = thisRegex.findall(this_sample)
                    for k, ip in theseResults:
                        if ip not in results[k]:
                            print "New IP - %s" % ip
                            results[k].append(ip)
                            new = True
                        all_these_ips.add(ip)
            removed = []
            for k,v in results.iteritems():
                for ip in v:
                    if ip not in all_these_ips:
                        results[k].remove(ip)
                        removed.append(ip)
            if len(removed) < 1:
                print "No IPs removed.."
            else:
                print "Removed the following IPs: %s" % ", ".join(removed)
                new = True
            if new is True:
                print "We have a change in the entries.. lets send an email!"
                bodyStr = "There has been a change in the %s.\n\n" % service.get('description')

                for k,v in results.iteritems():
                    if len(v) < 1: continue
                    bodyStr += "%s:\n" % k.upper()
                    for ip in v:
                        bodyStr += "\t%s\n" % ip
                    bodyStr += "\n"
                if len(removed) > 0:
                    bodyStr += "Removed IPs:\n"
                    for ip in removed:
                        bodyStr += "\t%s\n" % ip
                curr_time = datetime.datetime.now().strftime("%d %b %Y %H:%M CT")
                subject = "%s Change - %s" % (service.get('description'), curr_time)
                send_mail(FROM_ADDR, TO_ADDRS, subject, text=bodyStr, cc=CC_ADDRS)
                log_entry = "Observed a change"
            else:
                print "No changes observed!"
                log_entry = "No Changes observed."


            results_file = open(r_file_title,'w')
            results_file.write(json.dumps(results))

        except Exception as e:
            msg = "Error Running the script: %s" % e
            print msg
            send_mail(FROM_ADDR, ADMIN_ADDRS,
                "Error running IP Check Script", "Please see log for details.")
            log_entry = msg

    if LOGFILE not in os.listdir('.'):
        lf = open(LOGFILE,'w')
        lf.close()
    with open(LOGFILE,'a') as logfile:
        now = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S CT")
        logfile.write("%s\t%s\n" % (now, log_entry))
    print "Process finished..."

if __name__ == '__main__':
    main()
