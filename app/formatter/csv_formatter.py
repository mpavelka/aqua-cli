import csv
import sys

from .abc import Formatter


class CSVFormatter(Formatter):

    def print_formatted(self, data, keys: list[str] | None = None):
        # Print all keys if not provided
        if keys is None:
            keys = data[0].keys() if data else []
        if len(keys) == 0:
            return

        writer = csv.writer(sys.stdout, quoting=csv.QUOTE_MINIMAL)

        # Print header
        writer.writerow(keys)
        # Print each row
        for row in data:
            writer.writerow([row.get(key, "") for key in keys])


class CSVNoHeaderFormatter(Formatter):

    def print_formatted(self, data, keys: list[str] | None = None):
        # Print all keys if not provided
        if keys is None:
            keys = data[0].keys() if data else []
        if len(keys) == 0:
            return

        writer = csv.writer(sys.stdout, quoting=csv.QUOTE_MINIMAL)

        # Print each row
        for row in data:
            writer.writerow([row.get(key, "") for key in keys])
