import csv
import sys

from .abc import Formatter


class CSVFormatter(Formatter):

    def print_formatted(self, data, keys: list[str] = []):
        # Print all keys if not provided
        if len(keys) == 0:
            keys = data[0].keys() if data else []

        writer = csv.writer(sys.stdout, quoting=csv.QUOTE_MINIMAL)

        # Print header
        writer.writerow(keys)
        # Print each row
        for row in data:
            writer.writerow([row.get(key, "") for key in keys])


class CSVNoHeaderFormatter(Formatter):

    def print_formatted(self, data, keys: list[str] = []):
        # Print all keys if not provided
        if len(keys) == 0:
            keys = data[0].keys() if data else []

        writer = csv.writer(sys.stdout, quoting=csv.QUOTE_MINIMAL)

        # Print each row
        for row in data:
            writer.writerow([row.get(key, "") for key in keys])
