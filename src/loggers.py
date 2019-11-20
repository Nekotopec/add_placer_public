import os


class DfLogger:
    """Class for logging post activity."""

    def __init__(self, filename):
        """
        Args:
            filename (str): Filename
        """

        sub_path = os.path.dirname(__file__)
        path = os.path.dirname(sub_path)
        filename = os.path.join(path, filename)
        self.filename = filename

    def log(self, row):
        """
        Args:
            row (int): Number of row
        """

        with open(self.filename, 'a') as f:
            f.write('{} \n'.format(row))

    def synchronize(self, df):
        """Synchronize dataframe with log file.

        Args:
            df (pandas.Dataframe): Dataframe to synchronize
        """

        with open(self.filename, 'r') as f:
            data = f.readlines()
        data_int = [int(i) for i in data]
        column = 'Действие'
        for row in data_int:
            df.loc[row, column] = 3
