import abc

class Formatter(abc.ABC):
    """
    Abstract base class for formatters.
    """

    @abc.abstractmethod
    def print_formatted(self, data, keys: list[str] = []):
        """
        Format the given data.

        :param data: The data to format.
        :return: Formatted data.
        """
        pass