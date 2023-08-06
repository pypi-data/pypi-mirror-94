import typing as tp
import itertools as it

import pytest
from pytest_mock import MockFixture

from blip_flowanalysis.errors.long_script_error import (
    LongScriptParameterError,
)
from blip_flowanalysis.analysis.long_script import (
    Evaluator,
    JavaScriptEvaluator,
    Sample,
)


class TestJavaScriptEvaluator(object):
    
    @pytest.fixture
    def evaluator(self) -> JavaScriptEvaluator:
        return JavaScriptEvaluator()
    
    @pytest.mark.parametrize('script_expected', [
        ('content', 'content'),
        ('content: "a // b"', 'content: "a // b"'),
        ('content: "x /* y */"', 'content: "x /* y */"'),
    ])
    def test_remove_comments_has_no_comments(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._remove_comments(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('content // comment', 'content '),
        ('// comment\n content', '\n content'),
        ('// comment1\n// comment2\ncontent', '\n\ncontent'),
    ])
    def test_remove_comments_has_one_line_comments(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._remove_comments(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('content /* comment */', 'content '),
        ('/* comment\ncomment */\n content', '\n content'),
        ('/* comment\ncomment */\n/* comment */\n content', '\n\n content'),
    ])
    def test_remove_comments_has_multi_lines_comments(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._remove_comments(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('content', 'content'),
    ])
    def test_hide_strings_has_no_strings(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._hide_strings(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ("content 'string'", 'content --------'),
        ("content 'string1''string2'!", 'content ------------------!'),
        ("content 'string\nstring'", 'content ---------------'),
    ])
    def test_hide_strings_has_single_quoted_strings(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._hide_strings(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('content "string"', 'content --------'),
        ('content "string1""string2"!', 'content ------------------!'),
        ('content "string\nstring"', 'content ---------------'),
    ])
    def test_hide_strings_has_double_quoted_strings(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._hide_strings(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('no scope', (-1, -1)),
    ])
    def test_find_scope_has_no_scopes(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, tp.Tuple[int, int]]) -> None:
        script, expected = script_expected
        result = evaluator._find_scope(script, '(', ')')
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('ignore (scope)', (7, 13)),
        ('(scope1) (scope2)', (0, 7)),
    ])
    def test_find_scope_has_single_scopes(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, tp.Tuple[int, int]]) -> None:
        script, expected = script_expected
        result = evaluator._find_scope(script, '(', ')')
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('ignore (scope (inside))', (7, 22)),
        ('(scope (a) b (c) d)', (0, 18)),
        ('K * (a * (1 + (x - 1) / d) - 10)', (4, 31)),
    ])
    def test_find_scope_has_multi_scopes(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, tp.Tuple[int, int]]) -> None:
        script, expected = script_expected
        result = evaluator._find_scope(script, '(', ')')
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('closed script', False),
        ('closed (parenthesis)', False),
        ('closed [bracket]', False),
        ('closed {brace}', False),
        ('my_function(a, b, c) {return [c, b, a];}', False),
    ])
    def test_is_open_closed(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, bool]) -> None:
        script, expected = script_expected
        result = evaluator._is_open(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('opened (script', True),
        ('now [bracket', True),
        ('{brace is opened', True),
        ('my_function(a, b, c) {return [c, b, a];', True),
    ])
    def test_is_open_opened(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, bool]) -> None:
        script, expected = script_expected
        result = evaluator._is_open(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('no function', []),
    ])
    def test_list_functions_has_no_functions(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, tp.List[str]]) -> None:
        script, expected = script_expected
        result = evaluator._list_functions(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        (
                'function my_func(): {a = 1; print(a);}',
                ['a = 1; print(a);']
        ),
        (
                'function my_func():\n{\n  a = 1;\n  print(a);\n}',
                ['\n  a = 1;\n  print(a);\n']
        ),
        (
                'const func_1 = (a) =>\n{\n  print(a);\n}\n\n'
                'function func_2 (x):\n{\n  return x*x;\n}',
                ['\n  print(a);\n', '\n  return x*x;\n']
        ),
    ])
    def test_list_functions_has_functions(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, tp.List[str]]) -> None:
        script, expected = script_expected
        result = evaluator._list_functions(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        (
                'function my_func():'
                '\n{'
                '\n  a = 1;'
                '\n  function show(x):'
                '\n  {'
                '\n    print(x + a);'
                '\n  }'
                '\n}',
                ['\n  a = 1;'
                 '\n  function show(x):'
                 '\n  {'
                 '\n    print(x + a);'
                 '\n  }'
                 '\n']
        ),
    ])
    def test_list_functions_has_functions_inside_of_functions(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, tp.List[str]]) -> None:
        script, expected = script_expected
        result = evaluator._list_functions(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('no excess spaces', 'no excess spaces'),
    ])
    def test_remove_excess_spaces_has_no_excess_spaces(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._remove_excess_spaces(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('  excess on the left', 'excess on the left'),
        ('excess on the right  ', 'excess on the right'),
        ('excess   inside', 'excess inside'),
        ('excess \t  with\ttab', 'excess with tab'),
        ('excess   at   \n  multi  lines', 'excess at\nmulti lines'),
    ])
    def test_remove_excess_spaces_has_excess_spaces(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._remove_excess_spaces(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('there is no multi line', 'there is no multi line'),
    ])
    def test_remove_new_lines_has_no_new_lines(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]):
        script, expected = script_expected
        result = evaluator._remove_new_lines(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('there is\nmulti line', 'there is multi line'),
        ('there is\n  more \n multi line', 'there is   more   multi line'),
    ])
    def test_remove_new_lines_has_new_lines(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]):
        script, expected = script_expected
        result = evaluator._remove_new_lines(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        (
            'var x = 1;'
            '\nvar y = "var x = 1; if (x == 1) {}...";'
            '\nprint("coffee");',
            [
                'var x = 1;',
                'var y = "var x = 1; if (x == 1) {}...";',
                'print("coffee");',
            ]
        ),
        (
            'var x = 1;'
            '\nif (x == 1) {'
            '\n  print("coffee");'
            '\n}'
            '\nelse {'
            '\n  print("tea");'
            '\n}',
            [
                'var x = 1;',
                'if (x == 1)',
                'print("coffee");',
                'print("tea");',
            ]
        ),
        (
                'var x = 1;'
                '\nif (x == 1) {'
                '\n  print("coffee");'
                '\n  var w = {'
                '\n    "a": 1,'
                '\n    "b": 2'
                '\n  }'
                '\n}'
                '\nelse {'
                '\n  print("tea");'
                '\n}'
                '\nfunction my_function(q, r) {'
                '\n  print(q);'
                '\n  return r'
                '\n}'
                '\nreturn w',
                [
                    'var x = 1;',
                    'if (x == 1)',
                    'print("coffee");',
                    'var w = {     "a": 1,     "b": 2   }',
                    'print("tea");',
                    'function my_function(q, r)',
                    'print(q);',
                    'return r',
                    'return w',
                ]
        ),
    ])
    def test_split_commands_simple_scripts(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, tp.List[str]]) -> None:
        script, expected = script_expected
        result = evaluator._split_commands(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('there are no numbers', 'there are no numbers'),
        ('do not remove1234567890', 'do not remove1234567890'),
    ])
    def test_remove_numbers_has_no_numbers(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._remove_numbers(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('remove this 1234567890', 'remove this '),
        ('var x = 2 + 2;', 'var x =  + ;'),
        ('var x = 2.1;', 'var x = ;'),
        ('var x = -2;', 'var x = ;'),
        ('var x = -2.1;', 'var x = ;'),
    ])
    def test_remove_numbers_has_numbers(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._remove_numbers(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('there are no strings', 'there are no strings'),
    ])
    def test_remove_strings_has_no_strings(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._remove_strings(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('remove this "1234567890"', 'remove this '),
        ("var x = '2' + '2';", "var x =  + ;")
    ])
    def test_remove_strings_has_strings(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        result = evaluator._remove_strings(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('there are no lists', 'there are no lists'),
    ])
    def test_remove_lists_has_no_lists(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        script = evaluator._remove_numbers(script)
        script = evaluator._remove_strings(script)
        result = evaluator._remove_lists(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('remove this: [1234567890, "1234567890"]', 'remove this: '),
        ("var x = [2, '2'];", "var x = ;")
    ])
    def test_remove_lists_has_lists(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        script = evaluator._remove_numbers(script)
        script = evaluator._remove_strings(script)
        result = evaluator._remove_lists(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('there are no dicts', 'there are no dicts'),
    ])
    def test_remove_dicts_has_no_dicts(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        script = evaluator._remove_numbers(script)
        script = evaluator._remove_strings(script)
        result = evaluator._remove_dicts(script)
        assert result == expected
    
    @pytest.mark.parametrize('script_expected', [
        ('remove this: {"a": 123, "b": "123"}', 'remove this: '),
        ("var x = {'a': 2, 'b': '2'};", "var x = ;")
    ])
    def test_remove_dicts_has_dicts(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, str]) -> None:
        script, expected = script_expected
        script = evaluator._remove_numbers(script)
        script = evaluator._remove_strings(script)
        result = evaluator._remove_dicts(script)
        assert result == expected
    
    def test_remove_static_values(
            self,
            mocker: MockFixture,
            evaluator: JavaScriptEvaluator) -> None:
        str_mock = mocker.Mock(spec=str)
        
        remove_dicts = mocker.Mock(return_value=str_mock)
        remove_lists = mocker.Mock(return_value=str_mock)
        remove_strings = mocker.Mock(return_value=str_mock)
        remove_numbers = mocker.Mock(return_value=str_mock)
        
        evaluator._remove_dicts = remove_dicts
        evaluator._remove_lists = remove_lists
        evaluator._remove_strings = remove_strings
        evaluator._remove_numbers = remove_numbers
        
        script = str_mock
        expected = str_mock
        result = evaluator._remove_static_values(script)
        assert result is expected
        
        remove_numbers.assert_called_once_with(str_mock)
        remove_strings.assert_called_once_with(str_mock)
        remove_lists.assert_called_once_with(str_mock)
        remove_dicts.assert_called_once_with(str_mock)
    
    @pytest.mark.parametrize('script_expected', [
        (
            '/* This is a comment. */'
            'function run(a, b, c) {'
            '  if (a > 0) {'
            '    var type = "up";'
            '  }'
            '  else {'
            '    var type = "down";'
            '  }'
            '  print("type", type);'
            '  for (var x = 0; x < 10; x ++) {'
            '    var y =     quadratic(x);'
            '    print(x, y);'
            '  }'
            '  return 1;'
            '}'
            ''
            'function quadratic(a, b, c, x) {'
            '  return a * x * x + b * x + c;'
            '}',
            143
        )
    ])
    def test_count_chars_simple_scripts(
            self,
            evaluator: JavaScriptEvaluator,
            script_expected: tp.Tuple[str, int]) -> None:
        script, expected = script_expected
        result = evaluator.count_chars(script)
        assert result == expected
    
    def test_count_chars_mocked_script(
            self,
            mocker: MockFixture,
            evaluator: JavaScriptEvaluator) -> None:
        n_commands = 12
        n_functions = 3
        n_chars_command = 10
        str_mock = mocker.MagicMock(spec=str)
        list_commands = list(it.repeat(str_mock, n_commands))
        list_functions = list(it.repeat(str_mock, n_functions))
        
        str_mock_len = mocker.Mock(return_value=n_chars_command)
        remove_excess_spaces = mocker.Mock(return_value=str_mock)
        remove_static_values = mocker.Mock(return_value=str_mock)
        split_commands = mocker.Mock(return_value=list_commands)
        list_functions = mocker.Mock(return_value=list_functions)
        remove_comments = mocker.Mock(return_value=str_mock)
        
        str_mock.__len__ = str_mock_len
        evaluator._remove_excess_spaces = remove_excess_spaces
        evaluator._remove_static_values = remove_static_values
        evaluator._split_commands = split_commands
        evaluator._list_functions = list_functions
        evaluator._remove_comments = remove_comments
        
        script = str_mock
        expected = 360
        result = evaluator.count_chars(script)
        assert result == expected
        
        remove_comments.assert_called_once_with(str_mock)
        list_functions.assert_called_once_with(str_mock)
        split_commands.assert_has_calls(list(it.repeat(
            mocker.call(str_mock), n_functions)))
        remove_static_values.assert_has_calls(list(it.repeat(
            mocker.call(str_mock), n_functions * n_commands)))
        remove_excess_spaces.assert_has_calls(list(it.repeat(
            mocker.call(str_mock), n_functions * n_commands)))
        str_mock_len.assert_has_calls(list(it.repeat(
            mocker.call(), n_functions * n_commands)))
    
    def test_count_lines_mocked_script(
            self,
            mocker: MockFixture,
            evaluator: JavaScriptEvaluator) -> None:
        n_empty_lines = 9
        n_filled_lines = 3
        str_mock = mocker.MagicMock(spec=str)
        str_mock_empty = mocker.MagicMock(spec=str)
        list_lines =\
            list(it.repeat(str_mock, n_filled_lines))\
            + list(it.repeat(str_mock_empty, n_empty_lines))
        
        str_strip = mocker.Mock(return_value='a')
        str_strip_empty = mocker.Mock(return_value='')
        str_mock_splitlines = mocker.Mock(return_value=list_lines)
        remove_static_values = mocker.Mock(return_value=str_mock)
        remove_comments = mocker.Mock(return_value=str_mock)
        
        str_mock.strip = str_strip
        str_mock_empty.strip = str_strip_empty
        str_mock.splitlines = str_mock_splitlines
        evaluator._remove_static_values = remove_static_values
        evaluator._remove_comments = remove_comments
        
        script = str_mock
        expected = 3
        result = evaluator.count_lines(script)
        assert result == expected
        
        remove_comments.assert_called_once_with(str_mock)
        remove_static_values.assert_called_once_with(str_mock)
        str_mock_splitlines.assert_called_once_with()
        str_strip.assert_has_calls(list(it.repeat(
            mocker.call(), n_filled_lines)))
        str_strip_empty.assert_has_calls(list(it.repeat(
            mocker.call(), n_empty_lines)))
    
    def test_count_functions_mocked_script(
            self,
            mocker: MockFixture,
            evaluator: JavaScriptEvaluator) -> None:
        n_functions = 3
        str_mock = mocker.MagicMock(spec=str)
        list_functions = list(it.repeat(str_mock, n_functions))
        
        list_functions = mocker.Mock(return_value=list_functions)
        remove_comments = mocker.Mock(return_value=str_mock)
        
        evaluator._list_functions = list_functions
        evaluator._remove_comments = remove_comments
        
        script = str_mock
        expected = 3
        result = evaluator.count_functions(script)
        assert result == expected
        
        remove_comments.assert_called_once_with(str_mock)
        list_functions.assert_called_once_with(str_mock)
    
    def test_count_commands_mocked_script(
            self,
            mocker: MockFixture,
            evaluator: JavaScriptEvaluator) -> None:
        n_commands = 12
        n_functions = 3
        str_mock = mocker.MagicMock(spec=str)
        list_commands = list(it.repeat(str_mock, n_commands))
        list_functions = list(it.repeat(str_mock, n_functions))
        
        split_commands = mocker.Mock(return_value=list_commands)
        list_functions = mocker.Mock(return_value=list_functions)
        remove_comments = mocker.Mock(return_value=str_mock)
        
        evaluator._split_commands = split_commands
        evaluator._list_functions = list_functions
        evaluator._remove_comments = remove_comments
        
        script = str_mock
        expected = 36
        result = evaluator.count_commands(script)
        assert result == expected
        
        remove_comments.assert_called_once_with(str_mock)
        list_functions.assert_called_once_with(str_mock)
        split_commands.assert_has_calls(list(it.repeat(
            mocker.call(str_mock), n_functions)))


Position = int
Action = tp.Dict[str, tp.Any]
Interface = str
State = tp.Dict[str, tp.Any]
Context = tp.Tuple[
    State,
    Interface,
    Position,
    Action,
]

Check = bool
IntOrFloat = tp.Union[int, float]
AnalysisValues = tp.Tuple[IntOrFloat, ...]
AnalysisChecks = tp.Tuple[Check, ...]
Causes = tp.List[str]


class TestSample(object):
    
    @pytest.fixture
    def state_id(self, mocker: MockFixture) -> str:
        return mocker.Mock(spec=str)
    
    @pytest.fixture
    def state_name(self, mocker: MockFixture) -> str:
        return mocker.Mock(spec=str)
    
    @pytest.fixture
    def script(self, mocker: MockFixture) -> str:
        return mocker.Mock(spec=str)
    
    @pytest.fixture
    def values(self) -> AnalysisValues:
        chars = 50
        lines = 15
        functions = 1
        commands = 12
        lines_by_commands = lines / commands
        return chars, lines, functions, commands, lines_by_commands
    
    @pytest.fixture
    def checks(self) -> AnalysisChecks:
        return (
            False,
            False,
            False,
            False,
            False,
            False,
        )
    
    @pytest.fixture
    def evaluator(
            self,
            mocker: MockFixture,
            values: AnalysisValues) -> Evaluator:
        chars, lines, functions, commands, lines_by_commands = values
        evaluator = mocker.Mock(spec=Evaluator)
        evaluator.count_chars = mocker.Mock(return_value=chars)
        evaluator.count_lines = mocker.Mock(return_value=lines)
        evaluator.count_functions = mocker.Mock(return_value=functions)
        evaluator.count_commands = mocker.Mock(return_value=commands)
        return evaluator
    
    @pytest.fixture
    def context(
            self,
            mocker: MockFixture,
            state_id: str,
            state_name: str,
            script: str) -> Context:
        state = {
            'id': state_id,
            'name': state_name,
        }
        io_action = mocker.Mock(spec=str)
        n_action = mocker.Mock(spec=int)
        action = {
            'settings': {
                'source': script
            }
        }
        return state, io_action, n_action, action
    
    def test_sample(
            self,
            evaluator: Evaluator,
            context: Context,
            state_id: str,
            state_name: str,
            script: str,
            values: AnalysisValues,
            checks: AnalysisChecks) -> None:
        state, io_action, n_action, action = context
        chars, lines, functions, commands, lines_by_commands = values
        sample = Sample(evaluator, context)
        
        assert sample.script is action['settings']['source']
        assert sample.values == values
        assert sample.checks == checks
        
        assert sample.state is state
        assert sample.state_id == state_id
        assert sample.state_name == state_name
        assert sample.io_action == io_action
        assert sample.n_action == n_action
        assert sample.action is action
        
        assert sample.chars == chars
        assert sample.lines == lines
        assert sample.functions == functions
        assert sample.commands == commands
        assert sample.lines_by_commands == lines_by_commands
    
    def test_sample_too_many_chars(
            self,
            mocker: MockFixture,
            evaluator: Evaluator,
            context: Context) -> None:
        chars = 20
        evaluator.count_chars = mocker.Mock(return_value=chars)
        sample = Sample(evaluator, context, max_chars=10)
        assert sample.values[0] == chars
        assert sample.checks[0]
    
    def test_sample_too_many_lines(
            self,
            mocker: MockFixture,
            evaluator: Evaluator,
            context: Context) -> None:
        lines = 20
        evaluator.count_lines = mocker.Mock(return_value=lines)
        sample = Sample(evaluator, context, max_lines=10)
        assert sample.values[1] == lines
        assert sample.checks[1]
    
    def test_sample_too_many_functions(
            self,
            mocker: MockFixture,
            evaluator: Evaluator,
            context: Context) -> None:
        functions = 2
        evaluator.count_functions = mocker.Mock(return_value=functions)
        sample = Sample(evaluator, context, max_functions=1)
        assert sample.values[2] == functions
        assert sample.checks[2]
    
    def test_sample_too_many_commands(
            self,
            mocker: MockFixture,
            evaluator: Evaluator,
            context: Context) -> None:
        commands = 20
        evaluator.count_commands = mocker.Mock(return_value=commands)
        sample = Sample(evaluator, context, max_commands=10)
        assert sample.values[3] == commands
        assert sample.checks[3]
    
    def test_sample_too_many_commands_by_lines(
            self,
            mocker: MockFixture,
            evaluator: Evaluator,
            context: Context) -> None:
        lines = 10
        commands = 20
        evaluator.count_lines = mocker.Mock(return_value=lines)
        evaluator.count_commands = mocker.Mock(return_value=commands)
        sample = Sample(evaluator, context, span_lines_by_commands=(0.9, 1.1))
        assert sample.values[1] == lines
        assert sample.values[3] == commands
        assert sample.checks[4]
    
    def test_sample_too_many_lines_by_commands(
            self,
            mocker: MockFixture,
            evaluator: Evaluator,
            context: Context) -> None:
        lines = 20
        commands = 10
        evaluator.count_lines = mocker.Mock(return_value=lines)
        evaluator.count_commands = mocker.Mock(return_value=commands)
        sample = Sample(evaluator, context, span_lines_by_commands=(0.9, 1.1))
        assert sample.values[1] == lines
        assert sample.values[3] == commands
        assert sample.checks[5]
    
    def test_sample_zero_commands(
            self,
            mocker: MockFixture,
            evaluator: Evaluator,
            context: Context) -> None:
        commands = 0
        evaluator.count_commands = mocker.Mock(return_value=commands)
        sample = Sample(evaluator, context)
        assert sample.values[3] == commands
        assert sample.values[4] is None
        assert not sample.checks[4]
        assert not sample.checks[5]
    
    @pytest.mark.parametrize('context', [123, (1, 2, 3), (1, 2, 3, 4, 5)])
    def test_sample_invalid_context(
            self,
            evaluator: Evaluator,
            context: tp.Any) -> None:
        pytest.raises(LongScriptParameterError, Sample, evaluator, context)
    
    @pytest.mark.parametrize('state', [
        {'name': ''},
        {'id': ''},
        {},
    ])
    def test_sample_invalid_state(
            self,
            evaluator: Evaluator,
            context: Context,
            state: tp.Dict[str, tp.Any]) -> None:
        _, io_action, n_action, action = context
        context = state, io_action, n_action, action
        pytest.raises(LongScriptParameterError, Sample, evaluator, context)
    
    @pytest.mark.parametrize('action', [
        {'settings': {}},
        {},
    ])
    def test_sample_invalid_action(
            self,
            evaluator: Evaluator,
            context: Context,
            action: tp.Dict[str, tp.Any]) -> None:
        state, io_action, n_action, _ = context
        context = state, io_action, n_action, action
        pytest.raises(LongScriptParameterError, Sample, evaluator, context)
    
    @pytest.mark.parametrize('n_cause', range(6))
    def test_is_long_script_with_true(
            self,
            evaluator: Evaluator,
            context: Context,
            n_cause: int) -> None:
        checks = list(it.repeat(False, 6))
        checks[n_cause] = True
        sample = Sample(evaluator, context)
        sample.checks = checks
        assert sample.is_long_script()
    
    def test_is_long_script_with_all_false(
            self,
            evaluator: Evaluator,
            context: Context) -> None:
        sample = Sample(evaluator, context)
        sample.checks = tuple(it.repeat(False, 6))
        assert not sample.is_long_script()
    
    @pytest.mark.parametrize('n_causes', range(1, 7))
    def test_list_causes_with_true(
            self,
            evaluator: Evaluator,
            context: Context,
            n_causes: int) -> None:
        checks = [k < n_causes for k in range(6)]
        sample = Sample(evaluator, context)
        sample.checks = checks
        causes = sample.list_causes()
        
        assert isinstance(causes, list)
        assert causes
        for cause in causes:
            assert isinstance(cause, str)
    
    def test_list_causes_with_all_false(
            self,
            evaluator: Evaluator,
            context: Context) -> None:
        sample = Sample(evaluator, context)
        sample.checks = tuple(it.repeat(False, 6))
        causes = sample.list_causes()
        
        assert isinstance(causes, list)
        assert not causes
