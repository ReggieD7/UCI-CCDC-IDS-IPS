import EventViewer as ev
import re
import def

class EventEntity:

    def __init__(self, info):
        self.time_created = None
        self.date_created = None
        self.message = None
        self.id = None
        self.account_domain = None
        self.account_name = None
        for i in ev.gen(info):
            if 'TimeCreated' in i:
                pattern_date = r'[0-9]*[0-9]+/[0-9]+[0-9]+/[0-9]+[0-9]+'
                pattern_time = r'[0-9]{2}:[0-9]{2}:[0-9]{2} [AP]M'
                search_date = re.search(pattern_date, i)
                search_time = re.search(pattern_time, i)
                self.date_created = search_date.group()
                self.time_created = search_time.group()
                # print(self.time_created, self.date_created)
            elif 'Id' in i:
                pattern_id = r'[0-9]{4}'
                search_id = re.search(pattern_id, i)
                self.id = search_id.group()
            elif 'Message' in i:
                message = i.split(":", 1)[1]
                self.message = message.strip()
            elif ('Account Name' in i) and (len(i) > 41) and ('Network' not in i):
                account_name = i.split(":", 1)[1]
                self.account_name = account_name.strip()
            elif ('Account Domain' in i) and (len(i) > 41) and ('Network' not in i):
                account_domain = i.split(":", 1)[1]
                self.account_domain = account_domain.strip()

    def __repr__(self):
        return "EventEntity(DateCreated=%s, TimeCreated=%s ID=%s, Message=%s, Account Name=%s, Account Domain=%s)" \
               % (self.time_created if self.time_created is not None else "None",
                  self.date_created if self.date_created is not None else "None",
                  self.id if self.id is not None else "None",
                  self.message if self.message is not None else "None",
                  self.account_name if self.account_name is not None else "None",
                  self.account_domain if self.account_domain is not None else "None")

    def __str__(self):
        return self.__repr__()

class EventEntityManager:

    pass
