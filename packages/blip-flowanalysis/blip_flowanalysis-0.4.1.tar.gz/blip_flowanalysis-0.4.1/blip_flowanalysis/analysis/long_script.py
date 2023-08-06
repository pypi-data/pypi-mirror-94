__all__ = [
    'Evaluator',
    'JavaScriptEvaluator',
    'Sample',
    'LongScript',
    'LongScriptParameterError',
]

import abc
import re
import typing as tp

from blip_flowanalysis.abstract import Analyser
from blip_flowanalysis.errors import LongScriptParameterError
from blip_flowanalysis.core import Flow

Script = str
Count = int
Check = bool


class Evaluator(abc.ABC):
    """Script evaluator interface."""
    
    @abc.abstractmethod
    def count_chars(self, script: Script) -> Count:
        """Count chars.
        
        This count does not considers:
            * Blank-lines
            * Comments
            * Multiple space
            * Static values
        
        :param script: Script.
        :type script: `str`
        :return: Number of chars.
        :rtype: `int`
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def count_lines(self, script: Script) -> Count:
        """Count lines.
        
        This count does not considers:
            * Blank-lines
            * Comments
            * Static values
        
        :param script: Script.
        :type script: `str`
        :return: Number of lines.
        :rtype: `int`
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def count_functions(self, script: Script) -> Count:
        """Count functions.
        
        This count considers only top level functions.
        
        :param script: Script.
        :type script: `str`
        :return: Number of functions.
        :rtype: `int`
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def count_commands(self, script: Script) -> Count:
        """Count commands.
        
        This count does not considers:
            * Blank-lines
            * Comments
            * Static values
        
        :param script: Script.
        :type script: `str`
        :return: Number of commands.
        :rtype: `int`
        """
        raise NotImplementedError()


class JavaScriptEvaluator(Evaluator):
    """Evaluate JS script for LongScripts analysis."""
    
    def __init__(self) -> None:
        super().__init__()
    
    def _re(self, pattern: str) -> re.Pattern:
        return re.compile(pattern, re.DOTALL | re.MULTILINE)
    
    def _remove_comments(self, script: Script) -> Script:
        pattern = r'(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)'
        regex = self._re(pattern)
        
        def repl(match):
            return '' if match.group(2) is not None else match.group(1)
        
        return regex.sub(repl, script)
    
    def _remove_excess_spaces(self, script: Script) -> Script:
        return '\n'.join(
            filter(None, (
                ' '.join(map(str.strip, line.split()))
                for line in script.splitlines()
            ))
        )
    
    def _remove_new_lines(self, script: Script) -> Script:
        return script.replace('\n', ' ')
    
    def _remove_numbers(self, script: Script) -> Script:
        pattern = r'\W[+-]?[\d]+(?:\.\d+)?'
        regex = self._re(pattern)
        return regex.sub((lambda m: script[m.start()]), script)
    
    def _remove_strings(self, script: Script) -> Script:
        pattern = r'\".*?\"|\'.*?\''
        regex = self._re(pattern)
        return regex.sub('', script)
    
    def _remove_lists(self, script: Script) -> Script:
        pattern = r'[=(,;:]\s*\['
        regex = self._re(pattern)
        start = 0
        match = regex.search(script, start)
        while match:
            start = match.end()
            _, end = self._find_scope(script[(start - 1):], '[', ']')
            end += start - 1
            if not any(map(str.isalnum, script[start:end])):
                script = f'{script[:(start - 1)]}{script[(end + 1):]}'
                start = end + 1
            match = regex.search(script, start)
        return script
    
    def _remove_dicts(self, script: Script) -> Script:
        pattern = r'[=(,;:]\s*\{'
        regex = self._re(pattern)
        start = 0
        match = regex.search(script, start)
        while match:
            start = match.end()
            _, end = self._find_scope(script[(start - 1):], '{', '}')
            end += start - 1
            if not any(map(str.isalnum, script[start:end])):
                script = f'{script[:(start - 1)]}{script[(end + 1):]}'
                start = end + 1
            match = regex.search(script, start)
        return script
    
    def _remove_static_values(self, script: Script) -> Script:
        script = self._remove_numbers(script)
        script = self._remove_strings(script)
        script = self._remove_lists(script)
        script = self._remove_dicts(script)
        return script
    
    def _split_commands(self, script: Script) -> tp.List[Script]:
        pattern = (
            r'(^if\s*\()'
            r'|(^switch\s*\()'
            r'|(^for\s*\()'
            r'|(^while\s*\()'
            r'|(^function\s*[a-zA-Z_]\w*\s*\()'
            r'|(^catch\s*\()'
            r'|(^else\s*\{)'
            r'|(^do\s*\{)'
            r'|(^try\s*\{)'
            r'|(^finally\s*\{)'
            r'|(^case\s+[^:]*:)'
            r'|(^default\s*:)'
        )
        limiters = r'^[\s{}]*'
        open_parenthesis = [
            'if',
            'switch',
            'for',
            'while',
            'function',
            'catch',
        ]
        not_commands = [
            'else',
            'finally',
            'default',
        ]
        
        re_commands = self._re(pattern)
        re_limiters = re.compile(limiters)
        
        script = re_limiters.sub('', script)
        coded_script = self._hide_strings(script)
        commands = list()
        
        while script:
            match = re_commands.search(coded_script)
            
            if match and match.start() == 0:
                end = match.end()
                
                if any(map(coded_script.startswith, open_parenthesis)):
                    _, close = self._find_scope(coded_script, '(', ')')
                    if close >= 0:
                        end = close + 1
                
                if any(map(coded_script.startswith, not_commands)):
                    command = ''
                else:
                    command = script[:end]
                    if command.endswith('{'):
                        command = command[:-1]
            
            else:
                for index, char in enumerate(coded_script):
                    if char == ';':
                        end = index + 1
                        command = script[:end]
                        break
                    if char == '\n':
                        if not self._is_open(coded_script[:index]):
                            end = index + 1
                            command = script[:end]
                            break
                else:
                    end = len(script)
                    command = script
            
            if end == len(script):
                script = ''
                coded_script = ''
            else:
                script = script[end:]
                script = re_limiters.sub('', script)
                coded_script = coded_script[end:]
                coded_script = re_limiters.sub('', coded_script)
            
            command = command.replace('\n', ' ').strip()
            if command:
                commands.append(command)
        return commands
    
    def _hide_strings(self, script: Script) -> Script:
        pattern = r'\".*?\"|\'.*?\''
        regex = self._re(pattern)
        
        def repl(match):
            start, end = match.span()
            return (end - start) * '-'
        
        return regex.sub(repl, script)
    
    def _list_functions(self, script: Script) -> tp.List[Script]:
        pattern = (
            r'(function [\w^\d]\w*\s*\()'
            r'|(const\s+[\w^\d]\w*\s*=\s*\()'
        )
        regex = self._re(pattern)
        coded_script = self._hide_strings(script)
        functions = list()
        
        match = regex.search(coded_script)
        while match:
            script = script[match.end():]
            coded_script = coded_script[match.end():]
            start, end = self._find_scope(coded_script, '{', '}')
            
            if start == -1:
                break
            if end == -1:
                functions.append(script[(start + 1):])
                break
            
            functions.append(script[(start + 1):end])
            script = script[(end + 1):]
            coded_script = coded_script[(end + 1):]
            match = regex.search(coded_script)
        return functions
    
    def _find_scope(
            self,
            script: Script,
            start: str, end: str) -> tp.Tuple[int, int]:
        index_start = script.find(start)
        if index_start == -1:
            return -1, -1
        
        count = 1
        bias = index_start + 1
        for index, char in enumerate(script[bias:], bias):
            if char == start:
                count += 1
            elif char == end:
                count -= 1
                if not count:
                    return index_start, index
        return index_start, -1
    
    def _is_open(self, script: Script) -> bool:
        for c0, c1 in ('()', '[]', '{}'):
            i0, i1 = self._find_scope(script, c0, c1)
            if i0 >= 0 > i1:
                return True
        return False
    
    def count_chars(self, script: Script) -> Count:
        """Count chars on JS script.
        
        This count does not considers:
            * Blank-lines
            * Comments
            * Multiple space
            * Static values
        
        :param script: JS script.
        :type script: `str`
        :return: Number of chars.
        :rtype: `int`
        """
        n_chars = 0
        script = self._remove_comments(script)
        functions = self._list_functions(script)
        for script in functions:
            commands = self._split_commands(script)
            for command in commands:
                command = self._remove_static_values(command)
                command = self._remove_excess_spaces(command)
                n_chars += len(command)
        return n_chars
    
    def count_lines(self, script: Script) -> Count:
        """Count lines on JS script.
        
        This count does not considers:
            * Blank-lines
            * Comments
            * Static values
        
        :param script: JS script.
        :type script: `str`
        :return: Number of lines.
        :rtype: `int`
        """
        n_lines = 0
        script = self._remove_comments(script)
        script = self._remove_static_values(script)
        for line in script.splitlines():
            line = line.strip()
            if line:
                n_lines += 1
        return n_lines
    
    def count_functions(self, script: Script) -> Count:
        """Count functions on JS script.
        
        This count considers only top level functions.
        
        :param script: JS script.
        :type script: `str`
        :return: Number of functions.
        :rtype: `int`
        """
        script = self._remove_comments(script)
        functions = self._list_functions(script)
        return len(functions)
    
    def count_commands(self, script: Script) -> Count:
        """Count commands on JS script.
        
        This count does not considers clauses `else`, `finally` and `default`.
        
        :param script: JS script.
        :type script: `str`
        :return: Number of commands.
        :rtype: `int`
        """
        n_commands = 0
        script = self._remove_comments(script)
        functions = self._list_functions(script)
        for script in functions:
            commands = self._split_commands(script)
            n_commands += len(commands)
        return n_commands


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

IntOrFloat = tp.Union[int, float]
AnalysisValues = tp.Tuple[IntOrFloat, ...]
AnalysisChecks = tp.Tuple[Check, ...]
Causes = tp.List[str]


class Sample(object):
    """Represents a sample for execute script actions.
    
    This is a business layer that contains context information (including
    state, interface and action) and results (scripts, analysis values and
    analysis checks).
    
    :param evaluator: Evaluator instance that analyses script.
    :type evaluator: `Evaluator`
    :param context: Context input. Includes state, interface (inputActions or
        outputActions) and action (number and data).
    :type context: (`dict`, `str`, `int`, `dict`)
    :param max_chars: Maximum chars to not check as long script.
    :type max_chars: `int`
    :param max_lines: Maximum lines to not check as long script.
    :type max_lines: `int`
    :param max_functions: Maximum functions to not check as long script.
    :type max_functions: `int`
    :param max_commands: Maximum commands to not check as long script.
    :type max_commands: `int`
    :param span_lines_by_commands: Acceptable span for lines commands ratio.
    :type span_lines_by_commands: (`float`, `float`)
    """
    
    def __init__(
            self,
            evaluator: Evaluator,
            context: Context,
            max_chars: int = 837,
            max_lines: int = 36,
            max_functions: int = 1,
            max_commands: int = 21,
            span_lines_by_commands: tp.Tuple[float, float] = (0.9, 3.5)) -> None:
        super().__init__()
        self.evaluator = evaluator
        self.context = self._validated_context(context)
        self.max_chars = max_chars
        self.max_lines = max_lines
        self.max_functions = max_functions
        self.max_commands = max_commands
        self.span_lines_by_commands = span_lines_by_commands
        self.script = self._get_script()
        self.values = self._get_analysis_values()
        self.checks = self._check_analysis_values()
    
    @property
    def state(self) -> State:
        state, io_action, n_action, action = self.context
        return state
    
    @property
    def state_id(self) -> str:
        return self.state['id']
    
    @property
    def state_name(self) -> str:
        return self.state['name']
    
    @property
    def io_action(self) -> Interface:
        state, io_action, n_action, action = self.context
        return io_action
    
    @property
    def n_action(self) -> Position:
        state, io_action, n_action, action = self.context
        return n_action
    
    @property
    def action(self) -> Action:
        state, io_action, n_action, action = self.context
        return action
    
    @property
    def chars(self) -> Count:
        chars, lines, functions, commands, lines_by_commands = self.values
        return chars
    
    @property
    def lines(self) -> Count:
        chars, lines, functions, commands, lines_by_commands = self.values
        return lines
    
    @property
    def functions(self) -> Count:
        chars, lines, functions, commands, lines_by_commands = self.values
        return functions
    
    @property
    def commands(self) -> Count:
        chars, lines, functions, commands, lines_by_commands = self.values
        return commands
    
    @property
    def lines_by_commands(self) -> float:
        chars, lines, functions, commands, lines_by_commands = self.values
        return lines_by_commands
    
    def _validated_context(self, context: Context) -> Context:
        try:
            state, io_action, n_action, action = context
        except TypeError:
            raise LongScriptParameterError(
                f'Parameter `context` must be packable like '
                f'`(state, io_action, n_action, action)`. '
                f'Given: {context}')
        except ValueError:
            raise LongScriptParameterError(
                f'Parameter `context` must be packable like '
                f'`(state, io_action, n_action, action)`. '
                f'Given: {context}')
        
        try:
            _ = state['id']
            _ = state['name']
        except KeyError as exc:
            raise LongScriptParameterError(
                f'First element `state` on `context` must be a '
                f'valid state setting. Missed {exc}. '
                f'Given: {state}')
        
        try:
            _ = action['settings']['source']
        except KeyError as exc:
            raise LongScriptParameterError(
                f'Fourth element `action` on `context` must be a '
                f'valid action setting. Missed {exc}. '
                f'Given: {action}')
        except TypeError:
            raise LongScriptParameterError(
                f'Fourth element `action` on `context` must be a '
                f'valid action setting. '
                f'Given: {action}')
        
        return context
    
    def _get_script(self) -> str:
        state, io_action, n_action, action = self.context
        return action['settings']['source']
    
    def _get_analysis_values(self) -> AnalysisValues:
        chars = self.evaluator.count_chars(self.script)
        lines = self.evaluator.count_lines(self.script)
        functions = self.evaluator.count_functions(self.script)
        commands = self.evaluator.count_commands(self.script)
        try:
            lines_by_commands = lines / commands
        except ZeroDivisionError:
            lines_by_commands = None
        return chars, lines, functions, commands, lines_by_commands
    
    def _check_analysis_values(self) -> AnalysisChecks:
        chars, lines, functions, commands, lines_by_commands = self.values
        lc_lower, lc_upper = self.span_lines_by_commands
        return (
            (chars > self.max_chars),
            (lines > self.max_lines),
            (functions > self.max_functions),
            (commands > self.max_commands),
            (lines_by_commands is not None and lines_by_commands < lc_lower),
            (lines_by_commands is not None and lines_by_commands > lc_upper),
        )
    
    def is_long_script(self) -> bool:
        """Evaluate if is long script.
        
        :return: `True` if is long script otherwise `False`.
        :rtype: `bool`
        """
        return any(self.checks)
    
    def list_causes(self) -> Causes:
        """List causes why this sample detect any problem.
        
        :return: Causes explaining detections.
        :rtype: `list` of `str`
        """
        (
            too_many_chars,
            too_many_lines,
            too_many_functions,
            too_many_commands,
            too_many_commands_by_line,
            too_many_lines_by_command,
        ) = self.checks
        causes = list()
        
        if too_many_chars:
            causes.append('There are too many chars.')
        
        if too_many_lines:
            causes.append('There are too many lines.')
        
        if too_many_functions:
            causes.append(
                'More that one function. Consider apply one function by '
                'script and assign scripts in Blip variable to reuse.')
        
        if too_many_commands:
            causes.append('There are too many commands.')
        
        if too_many_commands_by_line:
            causes.append(
                'There are too many lines with more than one command.')
        
        if too_many_lines_by_command:
            causes.append('There are too many commands along many lines.')
        
        return causes


States = tp.List[State]
Samples = tp.List[Sample]
Results = tp.Tuple[
    States,
    Samples
]

ReportSummary = tp.Dict[str, tp.Any]
ReportDetails = tp.List[tp.Dict[str, tp.Any]]
Report = tp.Dict[str, tp.Any]


class LongScript(Analyser):
    """Check if bot scripts are too long.
    
    It is known, from bots development experience, that scripts on each state
    should be short. Long scripts would be considered as problem for bot
    maintainability and also a vulnerability to bugs occurrence.
    
    This analysis finds all scripts on bot states and measures their length as
    several aspects:
        * Number of characters. Does not count blank-lines, comments, multiples
        spaces and static values.
        * Lines. Does not count blank-lines.
    
    For each measure, there is a threshold. Default values are:
        * `1240` characters.
        * `40` lines.
    
    For each script, if any of these measures is above the threshold, this is
    reported in the analysis. See `analysis` for more details.
    
    Attributes:
        * max_length (`int`) - Maximum number of characters a script can have.
        * max_lines (`int`) - Maximum number of non-blank lines a script can
        have.
        * script_show_limit (`int`) - Limit of characters for displaying a
        script on the report.
        * execute_script_type (`str`) - Action type that execute a script on
        bot flow.
        * io_actions (`tuple`) - Interfaces on states to search for scripts.
    
    Methods:
        * analyse - Detects too long scripts on bot flow.
    """
    
    def __init__(
            self,
            max_chars: int = 837,
            max_lines: int = 36,
            max_functions: int = 1,
            max_commands: int = 21,
            span_lines_by_commands: tp.Tuple[float, float] = (0.9, 3.5),
            script_show_limit: int = 200,
            execute_script_type: str = 'ExecuteScript',
            io_actions: tuple = ('inputActions', 'outputActions')) -> None:
        super().__init__()
        self.max_chars = max_chars
        self.max_lines = max_lines
        self.max_functions = max_functions
        self.max_commands = max_commands
        self.span_lines_by_commands = span_lines_by_commands
        self.script_show_limit = script_show_limit
        self.execute_script_type = execute_script_type
        self.io_actions = io_actions
    
    def analyse(self, flow: Flow) -> Report:
        """Detects too long scripts on bot flow.
        
        Returns a report with summary and details.
        
        Summary includes:
            * Number of scripts;
            * Number of too long scripts;
            * Number of states;
            * Number of states having almost one long script.
        
        For each long script detection, details includes:
            * State ID;
            * State name;
            * IO Action (inputAction or outputAction);
            * Script;
            * Chars;
            * Lines;
            * Cause.
        
        :param flow: Bot flow structure.
        :type flow: `blip_flowanalysis.core.Flow`
        :return: Report with analysis of scripts on bot flow.
        :rtype: `dict` from `str` to `any`
        """
        states = flow.get_states_list()
        samples = self.measure(states)
        
        results = states, samples
        return self._report(results)
    
    def measure(self, states: States) -> Samples:
        """Measure all scripts on bot flow.
        
        Returns a list of samples.
        Each sample is related to an action with script execution and gives a
        result including chars count, lines count, functions count, commands
        count and ratio lines by commands.
        
        See also: blip_flowanalysis.analysis.long_script.Sample.
        
        :param states: List of states on bot flow.
        :type states: `list` of `dict`
        :return: Samples for each action with script execution.
        :rtype: `list` of `blip_flowanalysis.analysis.long_script.Sample`
        """
        samples = list()
        
        for context in self._iterate_contexts(states):
            state, io_action, n_action, action = context
            if self._is_execute_script(action):
                samples.append(self._sample(context))
        
        return samples
    
    def _iterate_contexts(
            self,
            states: tp.List[State]) -> tp.Iterator[Context]:
        for state in states:
            for io_action in self.io_actions:
                for n_action, action in enumerate(state[io_action]):
                    yield state, io_action, n_action, action
    
    def _is_execute_script(self, action: Action) -> bool:
        return action['type'] == self.execute_script_type
    
    def _sample(self, context: Context) -> Sample:
        evaluator = JavaScriptEvaluator()
        sample = Sample(
            evaluator,
            context,
            self.max_chars,
            self.max_lines,
            self.max_functions,
            self.max_commands,
            self.span_lines_by_commands,
        )
        return sample
    
    def _report_summary(self, results: Results) -> ReportSummary:
        states, samples = results
        n_scripts = len(samples)
        n_long_scripts = sum(s.is_long_script() for s in samples)
        n_states = len(states)
        n_irregular_states = len({sample.state_id for sample in samples})
        return {
            'scripts count': n_scripts,
            'scripts too long': n_long_scripts,
            'states count': n_states,
            'states with too long scripts': n_irregular_states,
        }
    
    def _report_details(self, results: Results) -> ReportDetails:
        states, samples = results
        details = list()
        for sample in samples:
            if sample.is_long_script():
                script = sample.script
                chars = sample.chars
                lines = sample.lines
                functions = sample.functions
                commands = sample.commands
                lines_by_commands = sample.lines_by_commands
                causes = sample.list_causes()
                
                limit = min(len(script), self.script_show_limit)
                script = sample.script[:limit]
                
                details.append({
                    'state id': sample.state_id,
                    'state name': sample.state_name,
                    'io action': sample.io_action,
                    'action number': sample.n_action,
                    'script': script,
                    'chars': chars,
                    'lines': lines,
                    'functions': functions,
                    'commands': commands,
                    'lines by commands': lines_by_commands,
                    'causes': causes,
                })
        return details
    
    def _report(self, results: Results) -> Report:
        summary = self._report_summary(results)
        details = self._report_details(results)
        return {
            'summary': summary,
            'details': details
        }
