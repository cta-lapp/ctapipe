from ctapipe.core import Component
from traitlets import Unicode
from time import sleep

EXPECTED = 'expected'
class WaitAndTotal(Component):

    """`WaitAndTotal` class represents a Stage or a Consumer for pipeline.
        It stock the values received and sum them once it had receive all values
    """
    filename = Unicode('/tmp/WaitAndTotal.txt', help='output filename').tag(
        config=True)
    received_values = list()
    expected_number_of_input = 0
    file = None

    def init(self):
        self.file = open(self.filename, 'w')
        self.log.info("--- WaitAndTotal init filename {}---".format(self.filename))
        return True

    def run(self, value):
        if isinstance(value, tuple):
            if value[0] == EXPECTED:
                self.expected_number_of_input = value [1]
        else:
            self.received_values.append(value)

    def finish(self):
        if self.expected_number_of_input == len(self.received_values):
            self.log.info('WaitAndTotal receive {}/{}'
                          .format(len(self.received_values), self.expected_number_of_input))
            total = 0
            for val in self.received_values:
                total += val

            self.file.write("total number of caracters: {}\n".format(total))
            self.log.info("total number of caracters: {}".format(total))

        else:
            self.log.info("WaitAndTotal did not receive all expected input: {}/{}"
                          .format(len(self.received_values), self.expected_number_of_input))
        self.file.close()
        self.log.debug("--- WaitAndTotal finish---")
