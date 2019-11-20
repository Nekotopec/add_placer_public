import os
import sys

from src.managers import XlsxManager
from src.parsers import EmlsParser
from src.requester import EmlsRequester
from src.loggers import DfLogger


def main():
    # Initializing a base directory
    base_dir = os.path.dirname(os.path.dirname(__file__))

    # If there is filename in parameters read it,
    # else dont read it, and use default filename.
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'try.xlsx'

    # Opening xlsx file.
    path = os.path.join(base_dir, filename)
    xlsx_file = XlsxManager(path)

    # Creating object to parse dataframe.
    emls_df = EmlsParser(xlsx_file.df)

    # Initialization of a poster
    # TODO: Сделать постер
    requester = EmlsRequester()

    # Filter df by column BS
    filtered_df = emls_df.get_filtered_dataframe()

    for row in filtered_df.iterrows():
        print('=' * 30)
        row_f = EmlsParser.get_filtered_row(row[1])
        print(row_f)
        # Posting
        # TODO: Должен вернуть None, если запрос не пройдет
        #  или будет херовый статус код
        href = requester.post_add(row_f)
        logger = DfLogger('log.txt')
        if href:
            # Логгирование на всякий случай
            logger.log(row[1].name)
            # Updating information in dataframe
            # Если в действии 3 значит запосщено объявление
            column_1 = 'Действие'
            emls_df.df.loc[row[1].name, column_1] = 3
            column_2 = 'Ссылка на размещенное объявление'
            emls_df.df.loc[row[1].name, column_2] = href

    xlsx_file.save(emls_df.df)


if __name__ == '__main__':
    main()
