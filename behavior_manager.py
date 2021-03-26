from math import sqrt


class Rules:
    dispatch = None
    arg = None
    task_a = dict()
    task_f = dict()

    def __init__(self):
        self.dispatch = {
            'task_a': 'do_task_a',
            'task_b': 'do_task_b',
            'task_c': 'do_task_c',
            'task_d': 'do_task_d',
            'task_e': 'do_task_e',
            'task_f': 'do_task_f'
        }
        self.task_a["min_total_delay"] = 0
        self.task_f["path_changes_counter"] = 0

    # min_total_delay greater than 150 millisecond
    def do_task_a(self, arg):
        if abs(arg['min_total_delay'] - self.task_a["min_total_delay"]) > 150:
            print('min_total_delay greater than 150 millisecond')
        self.task_a["min_total_delay"] = arg['min_total_delay']

    # min_total_delay greater than 150 millisecond for 1 minute
    @staticmethod
    def do_task_b(arg):
        pass
    # save the time
    # compare the time with the one save if it is > that 0
    # if the time is greater that 150 milliseconds and something else is happening, print out what is happening
    # and set variable to 0
    # else if time is

    # in packet is pair
    @staticmethod
    def do_task_c(arg):
        if arg['in_packets'] % 2 == 0:
            print('in packet is pair')

    # out packet is prime
    @staticmethod
    def do_task_d(arg):
        count = 0
        for i in range(1, int(sqrt(arg['out_packets']))):
            if arg['out_packets'] % i == 0:
                count = count + 1

        if count == 1:
            print('out packet is prime')

    # difference between out packets and in packets is greater than 20
    @staticmethod
    def do_task_e(arg):
        if abs(arg['out_packets'] - arg['in_packets']) > 20:
            print('difference between out packets and in packets is greater than 20')

    # path change counter difference between two consecutive flows is greater than 3
    def do_task_f(self, arg):
        if abs(arg['path_changes_counter'] - self.task_f["path_changes_counter"]) > 150:
            print('path change counter difference between two consecutive flows is greater than 3')
        self.task_f["path_changes_counter"] = arg['path_changes_counter']

    def process_command(self, arg):
        for command in self.dispatch:
            method_name = self.dispatch[command]
            method = getattr(self, method_name)
            method(arg)
