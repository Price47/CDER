from contextvars import ContextVar

CONTEXT_VAR__ROUND = "current_round"
current_round = ContextVar(CONTEXT_VAR__ROUND, default=0)
