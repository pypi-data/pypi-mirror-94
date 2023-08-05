from ..db import is_sqlite_db


class QueryBuilder:
    class Condition:
        def __init__(self, field, comparison, value, operator='AND'):
            self.field = field
            self.comparison = comparison
            self.value = value
            self.operator = operator

        def __str__(self):
            result = f"{self.field} {self.comparison} {self.value}"
            if self.field == 'original_name' and self.comparison == 'contains':
                result = f"dataset_images.original_name LIKE '%{self.value}%'"

            if self.operator:
                return f"{self.operator} {result}"
            return result

    class NestedConditions:
        def __init__(self, *conditions, operator='AND'):
            self.conditions = conditions
            self.operator = operator

            if len(self.conditions):
                self.conditions[0].operator = None

        def __str__(self):
            result = ' '.join([str(cond) for cond in self.conditions])
            return "{} ({})".format(self.operator, result)

    def __init__(self, query):
        self._query = query
        self._conditions = []
        self._order_by = None
        self._order_direction = None
        self._limit = None

    def condition(self, condition):
        if not condition:
            return

        if not len(self._conditions):
            if condition.operator in ('AND', 'OR'):
                condition.operator = None
            elif condition.operator.find('NOT'):
                condition.operator = 'NOT'
        self._conditions.append(condition)

    def order_by(self, field, direction='ASC'):
        self._order_by = field
        self._order_direction = direction

    def limit(self, limit):
        self._limit = limit

    def query(self):
        result = self._query
        if self._conditions:
            result = f"{result} WHERE"
        for cond in self._conditions:
            result = f"{result} {cond}"

        if self._order_by:
            result = f"{result} ORDER BY {self._order_by} {self._order_direction}"

        if self._limit:
            result = f"{result} LIMIT {self._limit}"

        return result


def transform_filter_to_condition(filter):
    filter_name = filter['name'].strip()
    filter_condition = filter['condition'].strip()
    filter_pattern = filter['pattern'].strip()

    if not filter_pattern:
        return None
    if filter_name not in ('class', 'tag', 'task', 'image_name'):
        return None
    if filter_condition not in ('is', 'is_not', 'contains'):
        return None

    filter_names = {
        'class': 'new_annotations.classes',
        'tag': 'new_annotations.tags',
        'task': 'new_annotations.task',
        'image_name': 'original_name',
    }

    comparison = ''
    value = ''
    field = filter_names.get(filter_name, '')

    if filter_condition == 'contains':
        comparison = 'contains'
        value = filter_pattern

    if filter_condition in ('is', 'is_not') and filter_name in ('class', 'tag'):
        comparison = 'LIKE' if is_sqlite_db() else '?'

    if filter_name in ('class', 'tag'):
        if is_sqlite_db():
            value = """'%"{}"%'""".format(filter_pattern)
        else:
            value = "'{}'".format(filter_pattern)

        if filter_condition == 'is_not':
            return QueryBuilder.NestedConditions(
                QueryBuilder.Condition(field, comparison, value),
                QueryBuilder.Condition(field, "IS", "NOT NULL"),
                operator='AND NOT'
            )

    if filter_name == 'task':
        if filter_condition == 'is':
            comparison = '='
        elif filter_condition == 'is_not':
            comparison = '<>'

        value = "'{}'".format(filter_pattern)

    return QueryBuilder.Condition(field, comparison, value)
