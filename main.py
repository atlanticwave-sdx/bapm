import sys
from argparse import ArgumentParser, ArgumentError
from sys import argv

from datasource_manager import DataSrc
from behavior_manager import Rules


if __name__ == '__main__':

    opts = ArgumentParser()
    rules = Rules()
    data_src = DataSrc(rules)

    try:
        opts.add_argument("--zabbix_ds", dest="is_zabbix", action='store_true',
                          help="Use Zabbix as a Datasource")

        opts.add_argument("--influxdb_ds", dest="is_influxdb", action='store_true',
                          help="Use InfluxDB as a Datasource")

        arguments = opts.parse_args(argv[1:])

        if arguments.is_zabbix and arguments.is_influxdb:
            raise ArgumentError(None, "You must specify a unique datasource")

        if arguments.is_zabbix:
            DataSrc.zabbix_data_src()

        elif arguments.is_influxdb:
            data_src.influxdb_data_src()

    except KeyboardInterrupt as err:
        print(err)

    except ArgumentError as err:
        print(err)
        opts.parse_args(args=['--help'])

    except TypeError as err:
        print(err)

    except ValueError as err:
        print(err.args[0])

    except NameError as err:
        print(err)

    except KeyError as err:
        print(err)

    # except Exception as inst:
    #     print(type(inst))
    #     print(inst.args)
    #     print(inst)

    finally:
        sys.exit(0)
