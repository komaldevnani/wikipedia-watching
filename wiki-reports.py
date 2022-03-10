from pywikibot.comms.eventstreams import EventStreams
from collections import Counter
from datetime import datetime
import time
import json

starting_time = datetime.now()

starting_time_str = starting_time.strftime("%Y%m%d%H%M%S")

domains_report = []
users = {}
stream = EventStreams(streams=['revision-create'])

for change in iter(stream):
    domain = ''
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

    if (datetime.now() - starting_time).seconds / 60 >= 1:
        starting_time = datetime.now()

        domains_report = dict(Counter(domains_report))
        print("=================================")
        print("Domains Report")
        print("Total number of Wikipedia Domains Updated: %i"%len(domains_report.keys()))
        for domain in domains_report:
            print("%s: %i pages updated"%(domain, domains_report[domain]))

        domains_report = []

        print("Users Report")
        print("Users who made changes to en.wikipedia.org")
        for k, v in sorted(users.items(), key=lambda item: item[1][1]):
            print("%s: %i"%(v[0],k))
        print("=================================")

        users = {}