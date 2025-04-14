SEED = 42

SYNTAX_ELEMENT_COUNT_CAP = 10
REGULATION = 0.5
MAX_TASK_COUNT = 30

# DQL_MODEL = {
#     "join": ["inner_join", "outer_join", "self_join"],
#     "nesting": ["cte", "correlated_subquery", "uncorrelated_subquery"],
#     "predicates": ["basic_operators", "logical_operators", "set_operators"]
# }

DQL_MODEL = {
    "duplicates": ["distinct", "union", "intersect", "except", "group_by"],
    "join": ["inner_join", "left_join", "right_join", "full_outer_join", "cross_join", "self_join"],
    "where": ["where", "comparison_operators", "logical_operators", "between", "like", "in", "is_null"],
    "grouping": ["group_by", "having"],
    "ordering": ["order_by", "asc", "desc"],
    "limiting": ["limit", "offset", "fetch"],
    "nesting": ["cte", "correlated_subquery", "uncorrelated_subquery", "derived_table"],
    "set_operations": ["union", "union_all", "intersect", "except"],
    "aggregations": ["count", "sum", "avg", "min", "max"],
    "window_functions": ["row_number", "rank", "dense_rank", "ntile", "lag", "lead"],
    "predicates": ["exists", "all", "any", "some"],
    "case_expressions": ["case", "when", "then", "else", "end"],
    "functions": ["coalesce", "nullif", "cast", "convert"]
}