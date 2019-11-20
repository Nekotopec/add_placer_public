import pandas as pd


class XlsxManager:

    def __init__(self, filename):
        """
        Args:
            filename (str): Filename of xlsx file
        """

        self.filename = filename
        self.df = self._read_xlsx()

    def _read_xlsx(self):
        """Read xlsx file and create pandas dataframe."""

        df = pd.read_excel(self.filename)
        return df

    def save(self, df):
        """Save dataframe to xlsx file with current filename. df:
        pandas.Dataframe

        Args:
            df (pandas.Dataframe): Dataframe to save
        """

        df.to_excel(self.filename)

    @staticmethod
    def save_as(filename, df):
        """Save dataframe to xlsx file with new name. filename: str df:
        pandas.Dataframe

        Args:
            filename (str): Filename to save. Use format 'filename.xlsx'
            df (pandas.Dataframe): Dataframe to save
        """

        df.to_excel(filename)
