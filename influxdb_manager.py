import copy
import json

from influxdb import InfluxDBClient


class InfluxDB:

    db_client = None
    params = None
    table_results = None
    my_time = None

    def __init__(self,):
        self.params = {"my_time": self.my_time}

    def open_connection(self):
        self.db_client = InfluxDBClient(host='127.0.0.1', port=8086, database='telemetry_summary')

    def get_data(self):

        if self.my_time is not None:
            select_clause = 'SELECT * FROM telemetry_summary.autogen.telemetry_summary ' \
                            'WHERE time > $my_time ' \
                            'ORDER BY time ASC LIMIT 10'

            table_results = self.db_client.query(select_clause, params={"params": json.dumps(self.params)})
        else:
            select_clause = "SELECT * FROM telemetry_summary.autogen.telemetry_summary " \
                            "ORDER BY time ASC LIMIT 10"

            table_results = self.db_client.query(select_clause)

        if not isinstance(table_results, list):
            # It creates a list based on the content retrieved from the database
            self.table_results = list(table_results.get_points(measurement='telemetry_summary'))

            # InfluxDB uses its tags as keys on its built-in sorting process
            # Switch ID tag is a string and intervenes on this process.
            # In order to get the records in a proper order based on their
            # insertion, we have to sort them based on the meta sequence number.
            self.table_results = sorted(self.table_results, key=lambda val: (val['time'], val['service_id']))
        else:
            # It creates a list based on the content retrieved from the database
            tmp = list()
            for result in table_results:
                tmp.append(list(result.get_points(measurement='telemetry_summary')))

            self.table_results = copy.deepcopy(tmp)
            tmp.clear()

        if len(self.table_results):
            self.my_time = self.table_results[len(self.table_results) - 1]['time']
            self.params["my_time"] = self.my_time
