from .abc import Formatter


class TableFormatter(Formatter):

    def print_formatted(self, data, keys: list[str] | None = None):
        # Print all keys if not provided
        if keys is None:
            keys = data[0].keys() if data else []
        if len(keys) == 0:
            return

        col_widths = self._calculate_col_widths(data, keys)

        # Print header
        header = self._format_row(keys, col_widths)
        print(header)
        # Print separator
        print("-" * len(header))
        # Print each row
        for row in data:
            formatted_row = self._format_row([row[key] for key in keys], col_widths)
            print(formatted_row)

    def _calculate_col_widths(self, data, keys: list[str]) -> list[int]:
        # Widhth of each column based on the keys
        col_widths = [0] * len(keys)
        for i, item in enumerate(keys):
            col_widths[i] = max(col_widths[i], len(str(item)))

        # Maximum width for each column based on the data
        for row in data:
            for i, key in enumerate(keys):
                col_widths[i] = max(col_widths[i], len(str(row.get(key, ""))))

        return col_widths

    def _format_row(self, row, col_widths=None):
        if col_widths is None:
            formatted_row = " | ".join(str(item) for item in row)
        else:
            formatted_row = " | ".join(
                str(item).ljust(width) for item, width in zip(row, col_widths)
            )
        return formatted_row
