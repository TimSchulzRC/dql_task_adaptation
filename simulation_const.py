SYNTAX_ELEMENT_COUNT_CAP = 10
REGULATION = 0.5
MAX_TASK_COUNT = 100

DQL_MODEL = {
    "join": ["inner_join", "outer_join", "self_join"],
    "nesting": ["cte", "correlated_subquery", "uncorrelated_subquery"],
    "predicates": ["basic_operators", "logical_operators", "set_operators"]
}