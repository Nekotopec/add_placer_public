from bs4 import BeautifulSoup


class EmlsParamsGetter:
    """Class for parsing add form on emls.ru."""

    selector_ajax = {
        'idRegDept': ('idReg', 'https://www.emls.ru/ajax/getdept2/'),
        'idRegDeptDist': ('idRegDept', 'https://www.emls.ru/ajax/getdist2/'),
        'idMetro': ('idRegDept', 'https://www.emls.ru/ajax/getstation/'),
        'idStreet': ('idRegDeptDist', 'https://www.emls.ru/ajax/getstreet2/'),
    }

    select_ids = ['id_type_deal', 'idReg', 'idRegDept', 'idRegDeptDist',
                  'idStreet', 'idMetro', 'id_amount_room', 'typeHouse',
                  'houseMaterial']

    # ids = ['price', 'idHouseNumber', 'sAll',
    # 'sLife', 'sKitchen', 'sCorridor',
    #        'floor', 'floorAll', 'yearBuild', 'commentForClients']

    index_map = {
        'цена (тыс.руб.)': 'price',
        'регион': 'idReg',
        'город (район)': 'idRegDept',
        'район города': 'idRegDeptDist',
        '(4) Улица': 'idStreet',
        'номер дома': 'idHouseNumber',
        'кол-во комнат': 'id_amount_room',
        'общая площадь': 'sAll',
        'жилая площадь': 'sLife',
        'пл. кухни': 'sKitchen',
        'пл. коридора': 'sCorridor',
        'высота потолка': 'sCeiling',
        'этаж': 'floor',
        'этажность': 'floorAll',
        'тип дома': 'typeHouse',
        'год постройки': 'yearBuild',
        'Примечание': 'commentForClients'
    }

    # Сделано так, потому что нет id у данного селектора.
    params_house_material = {
        'не указано': '0',
        'Кирпичный': '2',
        'Крупно-панельн.': '3',
        'Деревянный': '4',
        'Блочный': '5',
        'Монолитный': '6'
    }

    def __init__(self, page, session):
        """
        Args:
            page (str): Page to parse response.text
            session (requests.Session): Session from requester
        """

        self.page = page
        self.session = session
        self.soup = self._get_soup()

    def _get_soup(self):
        """Create BeautifulSoup object to processing."""

        soup = BeautifulSoup(self.page, 'lxml')
        return soup

    def get_parameters(self, row):
        """Return list of dictionaries, that consist parameters, that you need
        to post add.

        Args:
            row (pandas.Series)
        """

        params = dict()

        # Разделение на переуступку и остальные типы сделок.
        if row['тип сделки'] == 'Переуступка в сданном доме':
            return None
        else:
            params['id_type_deal'] = self._get_param('тип сделки',
                                                     'id_type_deal', row)

        for key, value in self.index_map.items():
            if value in self.selector_ajax:
                ajax_key, ajax_link = self.selector_ajax[value]
                print(ajax_link)
                print(ajax_key)
                print(ajax_key in params)
                print(params[ajax_key])
                url = ajax_link + params[ajax_key] + '.html'
                page = self.session.get(url)
                lines_list = page.text.splitlines()
                value_param = None
                for line in lines_list:

                    if row[key] in line:
                        value_param, key_param = line.split(';')
                        break

                if value_param:
                    params[value] = value_param

            elif value in self.select_ids:
                params[value] = self._get_param(key, value, row)

            else:
                params[value] = row[key]

        for key, value in self.params_house_material.items():
            if row['тип дома'] in key:
                params['houseMaterial'] = value
        return params

    def _get_param(self, key, param, row):
        """ Returns value from emls."""
        tag = self.soup.find(id=param)
        for child in tag.findChildren(name='option'):
            print(child.text)
            if row[key] in child.text:
                return child['value']
