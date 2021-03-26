import time

from datetime import datetime
from zabbix_manager import Zabbix
from influxdb_manager import InfluxDB


class DataSrc:

    rules = None

    def __init__(self, rules):
        self.rules = rules

    @staticmethod
    def zabbix_data_src():

        zabbix = Zabbix()
        zabbix.open_connection()

        zabbix.time_till = time.mktime(datetime.now().timetuple())

        while 1:
            zabbix.time_from = zabbix.time_till - zabbix.time_slot

            zabbix.get_outgoing_traffic()

            zabbix.time_till = time.mktime(datetime.now().timetuple())
            time.sleep(30)

    def influxdb_data_src(self):

        influxdb = InfluxDB()
        influxdb.open_connection()

        while 1:

            influxdb.get_data()

            # It returns/visualizes the records resultant content
            for table_result in influxdb.table_results:
                self.rules.process_command(table_result)
                print(table_result)