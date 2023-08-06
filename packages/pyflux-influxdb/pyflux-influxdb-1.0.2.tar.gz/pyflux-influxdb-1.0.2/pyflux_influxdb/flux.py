import copy
import re
from typing import Optional, Union, List


class NoBucketError(Exception):
    pass


class FluxSyntaxError(Exception):
    pass


class FluxR:

    def __init__(self):
        self.__measurement__ = 'r._measurement'
        self.__filed__ = 'r._field'
        self.__time__ = 'r._time'
        self.__value__ = 'r._value'

        self.default_attrs = {
            '__measurement__': self.__measurement__,
            '__filed__': self.__filed__,
            '__time__': self.__time__,
            '__value__': self.__value__
        }

    def __getattr__(self, item):
        if item in self.default_attrs.keys():
            return self.default_attrs[item]
        return f'r.{item}'


class FluxQ:
    connector = '=='
    AND = 'and'
    OR = 'or'

    def __init__(self, key: str, value, no_quotation=False):
        self.key = key
        self.value = value
        if no_quotation:
            self.flux_string = f'''{self.key} {self.connector} {self.value}'''
        else:
            if isinstance(self.value, str):
                self.flux_string = f'''{self.key} {self.connector} "{self.value}"'''
            else:
                self.flux_string = f'''{self.key} {self.connector} {self.value}'''

    def __str__(self):
        return self.flux_string

    def __repr__(self):
        return f'<{self.__class__.__name__}: ({self.flux_string})>'

    def __and__(self, other):
        return FluxCombinedQ(f'{self} {self.AND} {other}')

    def __or__(self, other):
        return FluxCombinedQ(f'{self} {self.OR} {other}')


class FluxCombinedQ:
    AND = 'and'
    OR = 'or'

    def __init__(self, combine_string):
        self.combine_string = combine_string

    def __repr__(self):
        return f'<{self.__class__.__name__}: ({self.combine_string})>'

    def __str__(self):
        return self.combine_string

    def __and__(self, other):
        return FluxCombinedQ(f'{self} {self.AND} {other}')

    def __or__(self, other):
        return FluxCombinedQ(f'{self} {self.OR} {other}')


class FluxEqual(FluxQ):
    pass


class FluxExclude(FluxQ):
    connector = '!='


class FluxLte(FluxQ):
    connector = '<='


class FluxLt(FluxQ):
    connector = '<'


class FluxGte(FluxQ):
    connector = '>='


class FluxGt(FluxQ):
    connector = '>'


class FluxExists(FluxQ):

    def __init__(self, key):
        super().__init__(key, None)
        self.flux_string = f'''exists {self.key}'''


class FluxNotExists(FluxQ):

    def __init__(self, key):
        super().__init__(key, None)
        self.flux_string = f'''not exists {self.key}'''


class FluxReg(FluxQ):
    def __init__(self, key: str, value: str):
        """
        正则表达式 value必须是字符串，并且格式符合 /xxx/
        :param key:
        :param value:
        """
        super().__init__(key, value)
        assert isinstance(self.value, str), 'param `value` must be string'
        self.flux_string = f'''{self.key} {self.connector} {self.value}'''


class FluxRegEqual(FluxReg):
    connector = '=~'


class FluxRegExclude(FluxReg):
    connector = '=!'


class FluxQuery:
    def __init__(self, bucket: str = None):
        self.pipe = '\n    |> '
        self.time_start = None
        self.time_end = None
        self.has_bucket = False
        self.has_range = False
        if self.time_end is None:
            self.time_end = 'now()'
        self.base = f'''from(bucket: "{bucket}") '''
        self.chains = []
        self.chains.append(self.base)

    def _syntax_check(self, input_string: str):
        if self.pipe in input_string:
            raise FluxSyntaxError(f'{self.pipe} in input_string: {input_string}')

    def _check_chains(self):
        if len(self.chains) < 2:
            raise FluxSyntaxError('flux query language is error')
        else:
            if not re.match(r'^range\(start:.+stop:.+\)$', self.chains[1]):
                raise FluxSyntaxError('flux query language must with range function')

    def clone(self) -> Optional['FluxQuery']:
        obj = self.__class__()
        obj.time_start = self.time_start
        obj.time_end = self.time_end
        obj.has_bucket = self.has_bucket
        obj.has_range = self.has_range
        obj.chains = copy.copy(self.chains)
        obj.base = self.base
        return obj

    def range(self,
              time_start: str,
              time_end: Optional[str] = 'now()'):
        self.time_start = time_start
        self.time_end = time_end
        self.chains.append(f'''range(start: {self.time_start}, stop: {self.time_end})''')
        return self

    def filter(self, condition: Union[FluxQ, FluxCombinedQ]):
        """
        :param condition:
        :return:
        """
        flux_string = f"""filter(fn: (r) => {condition})"""
        self.chains.append(flux_string)
        return self

    @staticmethod
    def _list_to_string(items):
        _temp = []
        for item in items:
            _temp.append(f'''"{item}"''')

        item_str = ','.join(_temp)

        return f'''[{item_str}]'''

    def pivot(self, row_key: List = None, column_key: List = None, value_column: str = '_time'):
        if row_key is None:
            row_key = ['_time']
        if column_key is None:
            column_key = ['_field']
        assert isinstance(value_column, str), 'param `value_column` not a string'
        self.chains.append((
            f'''pivot(rowKey: {self._list_to_string(row_key)}, '''
            f'''columnKey: {self._list_to_string(column_key)}, '''
            f'''valueColumn: "{value_column}")'''
        ))
        return self

    def limit(self, n: int, offset: int = 0):
        self.chains.append(f'''limit(n: {n}, offset: {offset})''')
        return self

    def duplicate(self, column_name: str, as_name: str):
        """
        duplicate(column: "column-name", as: "duplicate-name")
        :param column_name:
        :param as_name:
        :return:
        """
        self.chains.append(f'''duplicate(column: "{column_name}", as: "{as_name}")''')
        return self

    def sort(self, column_names: Optional[List[str]] = None, desc=True):
        """
        sort(columns: ["_value"], desc: false)
        :param desc:
        :param column_names:
        :return:
        """
        if column_names is None:
            column_names = ["_time"]
        self.chains.append(
            f'''sort(columns: {self._list_to_string(column_names)}, desc: {str(desc).lower()})''')
        return self

    def first(self):
        self.chains.append(f'''first()''')
        return self

    def last(self):
        self.chains.append(f'''last()''')
        return self

    def count(self, column='_value'):
        self.chains.append(f'''count(column: "{column}")''')
        return self

    def map(self, item_map: dict):

        _map_params = []

        for key, value in item_map.items():
            _map_params.append(f'''r with {key}: {value}''')

        _map_params_str = ','.join(_map_params)

        self.chains.append(f'''map(fn: (r)=> ({{{_map_params_str}}}))''')

        return self

    def group(self, group_columns: Optional[List[str]] = None):
        if group_columns is None:
            group_columns = ["_measurement"]
        self.chains.append(f'''group(columns: {self._list_to_string(group_columns)})''')
        return self

    def drop(self, drop_columns: List[str]):
        self.chains.append(f'''drop(columns: {self._list_to_string(drop_columns)})''')
        return self

    def rename(self, rename_map: dict):
        _map_params = []
        for key, value in rename_map.items():
            _map_params.append(f'''{key}: "{value}"''')
        _map_params_str = ','.join(_map_params)
        self.chains.append(f'''rename(columns: {{{_map_params_str}}})''')
        return self

    def fill(self, column, value):
        # |> fill(column: "granularity", value: "minute")
        self.chains.append(f'''fill(column: "{column}", value: {value})''')
        return self

    def get_script(self):
        self._check_chains()
        script = self.pipe.join(self.chains)
        return script
