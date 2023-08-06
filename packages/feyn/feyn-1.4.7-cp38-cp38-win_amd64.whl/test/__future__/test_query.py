import unittest
import pytest


# Things under test
from feyn.__future__.contrib.filters._query import Query, _make_parens_pair_optional_for_searchterm

@pytest.mark.future
class TestQuery(unittest.TestCase):

    def setUp(self):
        self.features = ['bmi', 'sex', 'smoker', 'region', 'children', 'age']

    def test_make_parens_pair_optional_for_searchterm(self):
        string_to_replace = "func(hello, optfunc(world))"
        term_to_make_optional = "optfunc"

        expected = "func(hello, optfunc(?world)?)"

        replaced = _make_parens_pair_optional_for_searchterm(string_to_replace, term_to_make_optional)

        assert expected == replaced, "Exactly the optional function should be made optional"

    def test_make_parens_pair_optional_for_searchterm_multiple_terms(self):
        string_to_replace = "func(optfunc(hello), optfunc(world))"
        term_to_make_optional = "optfunc"

        expected = "func(optfunc(?hello)?, optfunc(?world)?)"

        replaced = _make_parens_pair_optional_for_searchterm(string_to_replace, term_to_make_optional)

        assert expected == replaced, "All the optional functions should be made optional"

    def test_make_parens_pair_optional_for_searchterm_simple_case(self):
        string_to_replace = "optfunc(hello)"
        term_to_make_optional = "optfunc"

        expected = "optfunc(?hello)?"

        replaced = _make_parens_pair_optional_for_searchterm(string_to_replace, term_to_make_optional)

        assert expected == replaced, "Even simple functions should be optional"

    def test_Query_specific_parameter(self):
        query = "bmi"
        str_graph = "bmi"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), "The specific parameter graph should match")

        bad_graph = "age"
        self.assertFalse(q.is_match(bad_graph), "A graph with a wrong parameter should not match")

    def test_Query_match_required_param(self):
        query = "_"
        str_graph = "children"

        q = Query(query, self.features)

        self.assertTrue(q.is_match(str_graph), "A simple graph should match")

        bad_graph = "multiply(children)"
        self.assertFalse(q.is_match(bad_graph), "A bad graph should not match")

    def test_Query_match_optional_param(self):
        query = "*"
        str_graph = "sex"

        q = Query(query, self.features)

        self.assertTrue(q.is_match(str_graph), "A simple graph should match")

        str_graph = ""
        self.assertTrue(q.is_match(str_graph), "It also matches nothing (but this doesn't exist in the wild)")

    def test_Query_specific_function(self):
        query = "gaussian(_)"
        str_graph = "gaussian(bmi)"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), "The specific function graph should match")

        bad_graph = "multiply(bmi)"
        self.assertFalse(q.is_match(bad_graph), "A graph with a wrong function should not match")

    def test_Query_required_function(self):
        query = "!(_)"
        str_graph = "linear(bmi)"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), "The required function graph should match")

        str_graph = "tanh(bmi)"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), "The required function graph should match another function too")

        bad_graph = "bmi"
        self.assertFalse(q.is_match(bad_graph), "A graph with no function should not match")

    def test_Query_function_with_optional_param(self):
        query = "!(_, *)"
        str_graph = "add(bmi, age)"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), "The graph should match two parameters in a function")

        str_graph = "exp(bmi)"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), "The graph should match one parameter only in a function")

        bad_graph = "bmi"
        self.assertFalse(q.is_match(bad_graph), "A graph with no function should not match")

    def test_Query_required_with_only_optional_param(self):
        query = "!(*, *)" # This is a bit nonsensical, but does the same as the case above
        str_graph = "gaussian(bmi, age)"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), "The graph should match two parameters in a function")

        str_graph = "inverse(bmi)"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), "The graph should match one parameter only in a function")

        bad_graph = "bmi"
        self.assertFalse(q.is_match(bad_graph), "A graph with no function should not match")

    def test_Query_optional_function_and_param(self):
        query = "?(_, *)"
        str_graph = "gaussian(bmi, age)"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), "The graph should match two parameters in a function")

        str_graph = "sqrt(bmi)"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), "The graph should match one parameter only in a function")

        str_graph = "bmi"
        self.assertTrue(q.is_match(str_graph), "A graph with no function should match")

    def test_Query_optional_function_and_params(self):
        query = "?(*, *)"
        str_graph = "gaussian(bmi, age)"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), "The graph should match two parameters in a function")

        str_graph = "log(bmi)"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), "The graph should match one parameter only in a function")

        str_graph = "bmi"
        self.assertTrue(q.is_match(str_graph), "A graph with no function should match")

        str_graph = ""
        self.assertTrue(q.is_match(str_graph), "A graph with nothing also matches (but these don't exist in the wild)")

    def test_Query_required_function_required_params(self):
        query = "!(_, _)"
        str_graph = "gaussian(bmi, age)"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), "The graph should match two parameters in a function")

        bad_graph = "sine(bmi)"

        q = Query(query, self.features)
        self.assertFalse(q.is_match(bad_graph), "The graph should not match one parameter only in a function")

    def test_Query_nested_queries(self):
        query = "!(!(_), ?(*))"
        str_graph = "gaussian(sine(bmi), log(age))"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), "The graph should match nested function with the optional function")

        str_graph = "gaussian(sine(bmi), region)"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), "The graph should match nested function with just an optional param")

        str_graph = "gaussian(sine(smoker))"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), "The graph should match nested function without optional param")

        bad_graph = "sine(bmi)"

        q = Query(query, self.features)
        self.assertFalse(q.is_match(bad_graph), "The graph should not match one parameter only in a function")

    def test_Query_mixed_syntax_nested_queries(self):
        query = "!(sqrt(_), ?(_))"
        str_graph = "add(sqrt(bmi), log(age))"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), "The graph should match nested function with the optional function")

        str_graph = "gaussian(sqrt(bmi), region)"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), "The graph should match nested function with just an optional param")

        bad_graph = "gaussian(sqrt(smoker))"

        q = Query(query, self.features)
        self.assertFalse(q.is_match(bad_graph), "The graph should not match nested function without second param")

        bad_graph = "sine(bmi)"

        q = Query(query, self.features)
        self.assertFalse(q.is_match(bad_graph), "The graph should not match one parameter only in a function")

    def test_Query_nested_functions_with_first_optional(self):
        query = "!(?(*, *), ?(bmi))"
        str_graph = "add(sqrt(region, children), log(bmi))"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), f"The graph should match nested function {str_graph}")

        str_graph = "add(sqrt(region), log(bmi))"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), f"The graph should match nested function {str_graph}")

        str_graph = "add(region, log(bmi))"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), f"The graph should match nested function {str_graph}")

        str_graph = "add(region, bmi)"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), f"The graph should match function {str_graph}")

        str_graph = "add(bmi)"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), f"The graph should match function {str_graph}")

        bad_graph = "bmi"

        q = Query(query, self.features)
        self.assertFalse(q.is_match(bad_graph), "The graph should not match one parameter only")

    def test_Query_specific_param_order(self):
        query = "gaussian(sex, _)"
        str_graph = "gaussian(sex, bmi)"

        q = Query(query, self.features)
        self.assertTrue(q.is_match(str_graph), f"The graph should match function {str_graph}")

        bad_graph = "gaussian(bmi, sex)"

        q = Query(query, self.features)
        self.assertFalse(q.is_match(bad_graph), f"The graph will not match function {str_graph}")
