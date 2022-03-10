from pywikibot.comms.eventstreams import EventStreams
from collections import Counter
from datetime import datetime
from datetime import timedelta
import json

RECORD_INTERVAL = 5 # time interval for which to record updates from stream, 5 minutes
PRINT_INTERVAL = 1 # time interval after which to print reports, 1 minute

record_start_time = starting_time = datetime.now()

try:

    while True:

        domains_report = []
        users = {}
        record_start_time_s = record_start_time.strftime("%Y%m%d%H%M%S")
        stream = EventStreams(streams=['revision-create'], since=record_start_time_s)

        for change in iter(stream):

            try:

                domain = change['meta']['domain']
                domains_report.append(domain)

                if domain == 'en.wikipedia.org' and not(change['performer']['user_is_bot']):

                    user_id = change['performer']['user_id']
                    if not user_id in users:

                        users[user_id] = [change['performer']['user_text'], change['performer']['user_edit_count']]
                    else:
                        
                        users[user_id] = [change['performer']['user_text'], max(users[user_id][1], change['performer']['user_edit_count'])]
            except:

                pass

            if (datetime.now() - starting_time).seconds / 60 >= PRINT_INTERVAL:
                # time to print report and reset starting time

                starting_time = datetime.now()
                break

        domains_report = dict(Counter(domains_report))
        print("=================================")
        print("Domains Report")
        print("Total number of Wikipedia Domains Updated: %i"%len(domains_report.keys()))
        for domain in domains_report:

            print("%s: %i pages updated"%(domain, domains_report[domain]))

        print("Users Report")
        print("Users who made changes to en.wikipedia.org")
        for k, v in sorted(users.items(), key=lambda item: item[1][1]):
            # sort on the basis of user_edit_count

            print("%s: %i"%(v[0],k))
        print("=================================")

        if (datetime.now() - record_start_time).seconds / 60 >= RECORD_INTERVAL:

            record_start_time += timedelta(minutes=1)

except KeyboardInterrupt:

    pass