from pyzabbix import ZabbixAPI


class Zabbix:

    zapi = None
    time_slot = 4

    def __init__(self):
        self.ZABBIX_SERVER = 'https://ultralog.ampath.net/zabbix'
        self.ZABBIX_USER = 'apiuser'
        self.ZABBIX_PSSW = 'Ciaraapiuser*'

        # End time value considered to get the reads done
        # self.time_till = time.mktime(datetime.now().timetuple())
        self.time_till = None

        # Time slot to be considered to get information about
        self.time_slot = 60 * 3  # last 3 minutes

        # Start value considered to get the reads done
        # self.time_from = self.time_till - self.time_slot  # last 1 hours
        self.time_from = None

        self.filename = None

        self.data = dict()

    def open_connection(self):

        self.zapi = ZabbixAPI(self.ZABBIX_SERVER)
        self.zapi.login(self.ZABBIX_USER, self.ZABBIX_PSSW)
        self.zapi.timeout = 10

    def get_item_traffic(self, item_id):
        """
        Method to retrieve the historical values from some item (port) given its ID
        API connection to get item's history
        The returned values contains the item id, clock, value, and ns
        """
        result = list()

        # Query item's history (integer) data
        history = self.zapi.history.get(itemids=[item_id],
                                        time_from=self.time_from,
                                        time_till=self.time_till,
                                        output='extend',
                                        limit='5000')

        # If nothing was found, try getting it from history (float) data
        if not len(history):
            history = self.zapi.history.get(itemids=[item_id],
                                            time_from=self.time_from,
                                            time_till=self.time_till,
                                            output='extend',
                                            limit='5000',
                                            history=0)

        # Create the list with entries using each data point information
        # Point Structure {'itemid': '59532', 'clock': '1616619822', 'value': '552', 'ns': '945468991'}
        for point in history:
            result.append((int(point['clock']), int(point['value'])))

        return result

    # "MIA-MI1-SW01 100GB Eth7/2"
    def get_outgoing_traffic(self, item=59517):
        """
        Method to get the outgoing traffic

        :param item:
        :return: outgoing traffic
        """
        traffic_in = self.get_item_traffic(item)

        print(self.time_from)
        print(self.time_till)
        print(traffic_in)
        print("\n")