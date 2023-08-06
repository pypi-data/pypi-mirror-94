# sytk
Some tools making life a little easier :)
## @admin
Apply for the administrator right for the decorated function.
## @cache
Cache the `{'funcname-params': return value}` of the decorated functions. It is mainly used on functions calculating duplicate data.
## @debug
+ Show `parameters` and `return value` of the decorated function in a vivid color.
+ Meanwhile, in the same usage with `print()`, `d_print()`is also available to show the debug information in functions decorated with `@debug`.
## clean(path)
Delete code lines containing '@debug' and 'd_print'. It is used to turn projects into productions.
