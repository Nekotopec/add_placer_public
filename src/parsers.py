class EmlsParser:
    """Class for emls dataframe parsing."""

    # List of columns. Change it, if you change xlsx_base format
    xlsx_emls_base_list = ['тип сделки', 'цена (тыс.руб.)', 'регион',
                           'город (район)', 'район города', 'Действие',
                           '(4) Улица', 'метро', 'номер дома', 'кол-во комнат',
                           'общая площадь', 'жилая площадь', 'пл. кухни',
                           'пл. коридора', 'высота потолка', 'этаж',
                           'этажность', 'тип дома', 'материал дома',
                           'год постройки', 'Примечание']

    def __init__(self, dataframe):
        """Initialize. dataframe: pandas.DataFrame

        Args:
            dataframe (pandas.Dataframe): Dataframe to parse
        """

        self.df = dataframe


    def get_filtered_dataframe(self):
        """Returns filtered by column 'Действие' (BS) dataframe."""

        return self.df[self.df['Действие'] == 1]

    @classmethod
    def get_filtered_row(cls, series):
        """Get required columns from pandas series.

        Args:
            series (pandas.Series): Series from pandas.Dataframe
        """

        return series.loc[cls.xlsx_emls_base_list]