from bs4 import BeautifulSoup


class EmlsParamsGetter:
    """Class for parsing add form on emls.ru."""

    selector_ajax = {
        'id_reg_dept': ('id_reg',
                        'https://www.emls.ru/ajax/getdept2/'),
        'id_reg_dept_dist': ('id_reg_dept',
                             'https://www.emls.ru/ajax/getdist2/'),
        'id_metro': ('id_reg_dept',
                     'https://www.emls.ru/ajax/getstation/'),
        'id_street': ('id_reg_dept_dist',
                      'https://www.emls.ru/ajax/getstreet2/'),
    }

    select_ids = ['id_type_deal', 'id_reg', 'id_reg_dept', 'id_reg_dept_dist',
                  'id_street', 'id_metro', 'id_amount_room', 'typeHouse',
                  'houseMaterial']

    # ids = ['price', 'idHouseNumber', 'sAll',
    # 'sLife', 'sKitchen', 'sCorridor',
    #        'floor', 'floorAll', 'yearBuild', 'commentForClients']

    index_map = {
        'цена (тыс.руб.)': 'price',
        'регион': 'id_reg',
        'город (район)': 'id_reg_dept',
        'район города': 'id_reg_dept_dist',
        '(4) Улица': 'id_street',
        'метро': 'id_metro',
        'номер дома': 'object_address_house_number',
        'кол-во комнат': 'id_amount_room',
        'общая площадь': 'sAll',
        'жилая площадь': 'sLife',
        'пл. кухни': 'sKitchen',
        'пл. коридора': 'sCorridor',
        'высота потолка': 'sCeiling',
        'этаж': 'floor',
        'этажность': 'floorAll',
        'материал дома': 'typeHouse',
        'год постройки': 'yearBuild',
        'Примечание': 'commentForClients',
        'тип дома': 'houseMaterial'
    }

    # Сделано так, потому что нет id у данного тега.
    # params_house_material = {
    #     'не указано': '0',
    #     'Кирпичный': '2',
    #     'Крупно-панельн.': '3',
    #     'Деревянный': '4',
    #     'Блочный': '5',
    #     'Монолитный': '6'
    # }

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
                # print(ajax_link)
                # print(ajax_key)
                # print(ajax_key in params)
                # print(params[ajax_key])
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
                else:
                    params[value] = ''

            elif value in self.select_ids:
                params[value] = self._get_param(key, value, row)

            elif row[key] !=row[key]:
                print(row[key])
                params[value] = ''
            else:
                params[value] = row[key]

        return params

    def _get_param(self, key, param, row):
        """ Returns value from emls."""
        tag = self.soup.find(attrs={"name": param})
        # print(tag)
        for child in tag.findChildren(name='option'):
            # print(child.text)
            if row[key] in child.text:
                return child['value']
