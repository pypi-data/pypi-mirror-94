import feyn


class Query(feyn.filters.QGraphFilter):
    """ Rules
        "!(children, *)"

        "feature_name" -> "specific feature"
        "function_name" -> "specific function"

        "_" -> "A feature"
        "*" -> "Nothing, or a feature"

        "!(_)" ->  "function(features)"
        "?(_)" ->  "function(features) | features"
        "!(*)" -> "function(maybe_feature)"

        "!(_, *)" -> "function(features[, maybe_feature])"
        "!(*, *)" -> "Exactly the same as above - or nonsensical"

        "!(_, _)" -> "function(features, features)"

        "?(_, *)" -> "A feature", "A function with one feature",  "A function with two features"
        "?(*, *)" -> "Nothing", "A feature", "A function with one feature", "A function with two features"
    """
    def __init__(self, query, columns, verbose=False):
        import regex as re
        self.verbose = verbose

        regex = _regexify(query, columns)
        if self.verbose:
            print(regex)
        self.query = re.compile(regex)

    def __call__(self, graphs:feyn.filters.List[feyn._graph.Graph]):
        to_keep = []
        for g in graphs:
            str_repr = _get_string_representation(g)
            if self.verbose:
                print('-----')
                print(str_repr)

            if(self.is_match(str_repr)):
                to_keep.append(g)

            if self.verbose:
                print('-----')

        return to_keep

    def is_match(self, str_graph):
        match = self.query.match(str_graph)
        if self.verbose:
            print(match)
        return match and match.span() == (0, len(str_graph))


# TODO: This does not work for the simple case '?(bmi)'
# Are those offsets correct? paren_end does not get assigned.


def _make_parens_pair_optional_for_searchterm(string, searchterm):
    import regex as re

    offset = 0
    for m in re.finditer(searchterm, string):
        paren_start = m.end()

        count = 0
        for i, character in enumerate(string[paren_start+offset:]):
            if character == '(':
                count = count + 1
            if character == ')':
                count = count - 1
            if count == 0:
                paren_end = paren_start + i
                break

        # Put the question mark just after the parentheses - and adjust the offset now
        # that the string has an extra character there
        string = string[:paren_start+1+offset] + "?" + string[paren_start+1+offset:]
        offset = offset +1
        string = string[:paren_end+1+offset] + "?" + string[paren_end+1+offset:]
        offset = offset +1

    return string


def _regexify(squery, features):
    import regex as re
    functions = ["inverse", "gaussian", "multiply", "linear", "add", "sqrt", "log", "tanh", "sine", "exp", "circle"]

    # Utility Regexes
    not_already_escaped = r"[^\\]"
    all_contents = r".*"

    # Function regexes
    req_func = fr"\!\(({all_contents}{not_already_escaped})\)"
    opt_func_second = fr", \?\(({all_contents}{not_already_escaped})\)"
    opt_func = fr"\?\(({all_contents}{not_already_escaped})\)"

    # Parameter regexes
    req_param = r"(?<=\()_"
    req_param2 = r"(?<=, )_" # comma is needed, so don't substitute it out
    opt_param = fr"(?<=\()\*"
    opt_param2 = r", \*"     # Comma will be optional, so substitute it out (with an optional variant later)

    # Finding parens!
    left_paren = r"\("
    right_paren = r"\)"

    # Replacing function names:
    repl_fun = r"%fun%"
    repl_optfun = r"%optfun%"

    # Replacing feature names:
    repl_feat = r"%feat%"
    repl_optfeat = r"%optfeat%"

    # Special case for graphs with no functions
    # squery = "_"
    req_param_alone = r"_"
    if re.match(req_param_alone, squery):
        squery = re.sub(req_param_alone, repl_feat, squery)
        pass

    # "*" doesn't quite make sense, but treat it the same
    req_param_alone = r"\*"
    if re.match(req_param_alone, squery):
        squery = re.sub(req_param_alone, repl_optfeat, squery)
        pass

    # Substitute out required params
    squery = re.sub(req_param, repl_feat, squery)
    squery = re.sub(req_param2, repl_feat, squery)

    # Substitute out optional params
    squery = re.sub(opt_param, repl_optfeat, squery)
    squery = re.sub(opt_param2, repl_optfeat, squery)

    # Recursively replace required functions
    while(re.search(req_func, squery)):
        squery = re.sub(req_func, fr"{repl_fun}(\1)", squery)

    # Recursively replace problematic optional functions that are second parameter
    while(re.search(opt_func_second, squery)):
        squery = re.sub(opt_func_second, fr"{repl_optfun}(\1)", squery)


    # Recursively replace optional functions
    while(re.search(opt_func, squery)):
        squery = re.sub(opt_func, fr"{repl_optfun}(\1)", squery)

    # Add optional notation (?'s) to parens belonging to optional functions
    squery = _make_parens_pair_optional_for_searchterm(squery, repl_optfun)

    # Note: This will kill parentheses in feature names
    squery = re.sub(left_paren, r"\(", squery)
    squery = re.sub(right_paren, r"\)", squery)

    # Do the final replacement of function names, parameter names.
    return squery \
          .replace(repl_fun, fr"({'|'.join(functions)})") \
          .replace(repl_optfun, fr"(, )?({'|'.join(functions)})?") \
          .replace(repl_feat, fr"({'|'.join(features)})") \
          .replace(repl_optfeat, fr"(, )?({'|'.join(features)})?")


def _get_string_representation(graph):
    expressions = []
    for i in graph:
        if "in:" in i.spec:
            expressions.append(i.name)
        elif "out:" in i.spec:
            expressions.append(i.name)
        else:
            function = i.spec.split('cell:')[1].split('->')[0]
            if len(i.sources) > 1:
                function = function.replace('(i,i)', '(__x0__, __x1__)')
            else:
                function = function.replace('(i)', '(__x0__)')
            expressions.append(function)


    for ix, i in enumerate(graph):
        if "in:" in i.spec:
            continue
        elif "out:" in i.spec:
            continue

        if len(i.sources)>0:
            expressions[ix] = expressions[ix].replace("__x0__", expressions[i.sources[0]])
        if len(i.sources)>1:
            expressions[ix] = expressions[ix].replace("__x1__", expressions[i.sources[1]])

    return expressions[-2]  # Return the node before the output node
