class TableFormatter:
    def __init__(self, keys):
        self._keys = keys

    def print_formatted(self, rows):

        all_rows = [self._keys]

        # Extend all rows with row values
        for row in rows:
            new_row = [row.get(column, "") for column in self._keys]
            all_rows.append(new_row)

        # Calculate the maximum width for each column
        col_widths = [0] * len(self._keys)
        for row in all_rows:
            for i, item in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(item)))

        for row in all_rows:
            formatted_row = self._format_row(row, col_widths)
            print(formatted_row)

    def _format_row(self, row, col_widths=None):
        if not row:
            return "No data available."

        if col_widths is None:
            col_widths = [max(len(str(item)) for item in row)] * len(row)

        formatted_row = " | ".join(
            str(item).ljust(width) for item, width in zip(row, col_widths)
        )
        return formatted_row
