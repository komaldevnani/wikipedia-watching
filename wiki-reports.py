from pywikibot.comms.eventstreams import EventStreams
from collections import Counter
from datetime import datetime
import time

starting_time = datetime.now()

starting_time_str = starting_time.strftime("%Y%m%d%H%M%S")

domains_report = []
stream = EventStreams(streams=['revision-create'])

for change in iter(stream):
    domains_report.append(change['meta']['domain'])

    if (datetime.now() - starting_time).seconds / 10 >= 1:
        starting_time = datetime.now()

        domains_report = dict(Counter(domains_report))
        print("=================================")
        print("Total number of Wikipedia Domains Updated: %i"%len(domains_report.keys()))
        for domain in domains_report:
            print("%s: %i pages updated"%(domain, domains_report[domain]))

        domains_report = []
