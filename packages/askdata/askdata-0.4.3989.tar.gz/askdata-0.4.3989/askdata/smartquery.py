from enum import Enum, auto
from typing import List, Optional, Union
from dataclasses import dataclass


class SQLFunction(Enum):
    MAX = auto()
    MIN = auto()
    AVG = auto()
    COUNT = auto()
    SUM = auto()


class TimeDimensionGranularity(Enum):
    year = auto()
    quarter = auto()
    month = auto()
    week = auto()
    day = auto()
    hour = auto()


@dataclass
class Field:
    column: str
    aggregation: Optional[Union[SQLFunction, TimeDimensionGranularity, str]] = None
    dataset: Optional[str] = None
    entityType: Optional[str] = None
    alias: Optional[str] = None


class SQLOperator(Enum):
    EQ = auto()
    GOE = auto()
    GT = auto()
    LOE = auto()
    LT = auto()
    IN = auto()
    NOT_IN = auto()


@dataclass
class Condition:
    field: Field
    operator: Union[SQLOperator, str]
    value: List[Union[str, float]]
    type: Optional[str] = None


class SQLSorting(Enum):
    DESC = auto()
    ASC = auto()


@dataclass
class Sorting:
    field: str
    order: SQLSorting


@dataclass
class Setting:
    type: str


@dataclass
class Component:
    component_type: str
    setting: Optional[List[Setting]] = None


@dataclass
class From:
    dataset: str


@dataclass
class Query:
    fields: List[Field]
    datasets: Optional[List[From]] = None
    where: Optional[List[Condition]] = None
    orderBy: Optional[List[Sorting]] = None
    limit: Optional[Union[int, str]] = None

    def to_sql(self, dataset: str = None):
        sql = "SELECT {} FROM {}"

        fields_with_agg = []
        for field in self.fields:
            if field.aggregation is not None:
                if isinstance(field.aggregation, SQLFunction):
                    field_with_agg = field.aggregation.name + " ( " + field.column + " )"
                elif isinstance(field.aggregation, TimeDimensionGranularity):
                    field_with_agg = field.column
                else:
                    field_with_agg = field.aggregation + " ( " + field.column + " )"
            else:
                field_with_agg = field.column
            if field.alias is not None:
                field_with_agg += " AS " + "'" + field.alias + "'"
            fields_with_agg.append(field_with_agg)

        formatted_fields = ", ".join(fields_with_agg)

        froms_array = []
        if self.datasets is not None:
            for f in self.datasets:
                froms_array.append(f.dataset)
            table = ", ".join(froms_array)
        elif dataset is not None:
            table = dataset
        else:
            table = "{{dataset.A}}"
        sql = sql.format(formatted_fields, table)

        where_conditions = []
        having_conditions = []
        if self.where is not None:
            sql_where = " WHERE {}"

            for condition in self.where:
                vars = []
                for var in condition.value:
                    var = "'" + str(var) + "'"
                    if var.isnumeric():
                        vars.append(var)
                    else:
                        vars.append(var)
                formatted_value = "( " + ", ".join(vars) + " )"
                if isinstance(condition.operator, str):
                    operator = condition.operator
                else:
                    operator = condition.operator.name
                    if operator == "GOE":
                        operator = ">="
                    elif operator == "LOE":
                        operator = "<="
                    elif operator == "EQ":
                        operator = "=="
                if condition.field.aggregation is not None:
                    having_conditions.append(condition)
                    # if isinstance(condition.field.aggregation, SQLFunction):
                    #     field_with_agg = condition.field.aggregation.name + " ( " + condition.field.column + " )"
                    # elif isinstance(condition.field.aggregation, TimeDimensionGranularity):
                    #     field_with_agg = condition.field.column
                    # else:
                    #     field_with_agg = condition.field.aggregation + " ( " + condition.field.column + " )"
                else:
                    field_with_agg = condition.field.column
                    where_condition = (
                            field_with_agg + " " + operator + " " + str(formatted_value)
                    )
                    where_conditions.append(where_condition)
            if where_conditions:
                formatted_where_conditions = " AND ".join(where_conditions)
                sql_where = sql_where.format(formatted_where_conditions)
                sql += sql_where

        group_conditions = []
        sql_groupBy = " GROUP BY {}"

        for field in self.fields:
            if field.entityType is not None:
                if "P_DIMENSION" == field.entityType or "P_TIMEDIM" == field.entityType:
                    group_conditions.append(field.column)
        if group_conditions:
            formatted_group = ", ".join(group_conditions)
            sql_groupBy = sql_groupBy.format(formatted_group)
            sql += sql_groupBy

        if having_conditions:
            if not group_conditions:
                formatted_group = " '' "
                sql_groupBy = sql_groupBy.format(formatted_group)
                sql += sql_groupBy
            sql_having = " HAVING {}"
            all_having_conditions = []
            for condition in having_conditions:
                vars = []
                for var in condition.value:
                    var = str(var)
                    if var.isnumeric():
                        vars.append(var)
                    else:
                        vars.append(var)
                formatted_value = "( " + ", ".join(vars) + " )"
                if isinstance(condition.operator, str):
                    operator = condition.operator
                else:
                    operator = condition.operator.name
                    if operator == "GOE":
                        operator = ">="
                    elif operator == "LOE":
                        operator = "<="
                    elif operator == "EQ":
                        operator = "=="
                if condition.field.aggregation is not None:
                    if isinstance(condition.field.aggregation, SQLFunction):
                        field_with_agg = condition.field.aggregation.name + " ( " + condition.field.column + " )"
                    elif isinstance(condition.field.aggregation, TimeDimensionGranularity):
                        field_with_agg = condition.field.column
                    else:
                        field_with_agg = condition.field.aggregation + " ( " + condition.field.column + " )"
                else:
                    field_with_agg = condition.field.column
                having_condition = (
                        field_with_agg + " " + operator + " " + str(formatted_value)
                )
                all_having_conditions.append(having_condition)
            formatted_having_conditions = " AND ".join(all_having_conditions)
            sql_having = sql_having.format(formatted_having_conditions)
            sql += sql_having

        sorting_conditions = []
        if self.orderBy is not None:
            sql_orderby = " ORDER BY {}"

            for sorting in self.orderBy:
                sort_order = sorting.order.name
                sort_condition = sorting.field + " " + sort_order
                sorting_conditions.append(sort_condition)

            formatted_sorting = ", ".join(sorting_conditions)
            sql_orderby = sql_orderby.format(formatted_sorting)
            sql += sql_orderby

        if self.limit is not None:
            sql += " LIMIT " + str(self.limit)

        return sql


@dataclass
class SmartQuery:
    queries: List[Query]
    components: Optional[List[Component]] = None  # use this for of charts
    javascript: Optional[List[str]] = None
