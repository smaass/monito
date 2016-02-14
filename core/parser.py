from core.ast.ast import *


class Parser(object):

    OPENING_PARENS = ['(', '[', '{']
    CLOSING_PARENS = [')', ']', '}']

    @classmethod
    def parse(cls, code):
        """
        :param code: Monito code string to parse
        :rtype: ASTNode
        """
        balanced, failure_index = cls.balanced_parens(code)
        if not balanced:
            raise SyntaxError('unbalanced parentheses')

        s_expression_strings = cls.separate_sexpr_strings(code)
        s_expressions = [
            cls.string_to_sexpr(string) for string in s_expression_strings
        ]
        abstract_syntax_trees = [
            cls.sexpr_to_ast(sexpr) for sexpr in s_expressions
        ]

        return BodySequence(abstract_syntax_trees)

    @classmethod
    def separate_sexpr_strings(cls, string):

        string = string.strip()
        s_expression_strings = []
        stack = []
        start_index = 0
        current_index = 0

        for char in string:
            if char in cls.OPENING_PARENS:
                stack.append(char)
            if char in cls.CLOSING_PARENS:
                stack.pop()
                if len(stack) == 0:
                    s_expression_strings.append(
                        string[start_index:current_index+1].strip()
                    )
                    start_index = current_index + 1
            current_index += 1

        # Handle single atoms
        if len(s_expression_strings) == 0 and current_index > 0:
            s_expression_strings.append(string)

        return s_expression_strings


    @classmethod
    def balanced_parens(cls, string):
        '''
        Returns a (<balanced>, <index>) tuple in which <balanced> is a
        boolean that represents whether <string> has balanced parentheses.
        If <balanced> is true, <index> is None. If <balanced> is false, <index>
        is an integer value indicating the index in <string> that caused the
        checking to fail.
        '''
        stack = []
        i = 0

        for char in string:
            if char in cls.OPENING_PARENS:
                stack.append(char)

            if char in cls.CLOSING_PARENS:
                if len(stack) == 0:
                    return False, i

                paren_index = cls.CLOSING_PARENS.index(char)
                if stack.pop() != cls.OPENING_PARENS[paren_index]:
                    return False, i
            i += 1

        if len(stack) > 0:
            return False, i

        return True, None

    @classmethod
    def string_to_sexpr(cls, string):

        simplified_string = string\
            .replace('{', '(')\
            .replace('[', '(')\
            .replace('}', ')')\
            .replace(']', ')')

        return cls.tokens_to_sexpr(cls.tokenize(simplified_string))

    @classmethod
    def tokenize(cls, chars):
        """
        Converts string to list of tokens
        """
        return chars.replace('(', ' ( ').replace(')', ' ) ').split()

    @classmethod
    def sexpr_to_ast(cls, sexpr):
        """
        :param sexpr: s-expression to transform to AST
        :rtype: ASTNode
        """

        "Numbers and booleans"
        if (
            type(sexpr) == type(1) or
            type(sexpr) == type(0.1) or
            type(sexpr) == type(True)
        ):
            return Val(sexpr)

        "Strings and symbols"
        if type(sexpr) != type([]):
            if sexpr.startswith('"') and sexpr.endswith('"'):
                return Val(sexpr[1:-1])
            return Id(sexpr)

        if sexpr[0] == 'if':
            return If(
                cls.sexpr_to_ast(sexpr[1]),
                cls.sexpr_to_ast(sexpr[2]),
                cls.sexpr_to_ast(sexpr[3])
            )
        if sexpr[0] == 'and':
            return And(
                cls.sexpr_to_ast(sexpr[1]),
                cls.sexpr_to_ast(sexpr[2])
            )
        if sexpr[0] == 'or':
            return Or(
                cls.sexpr_to_ast(sexpr[1]),
                cls.sexpr_to_ast(sexpr[2])
            )

        "Anonymous functions"
        if sexpr[0] == 'fun':
            return Fun(
                sexpr[1],
                cls.sexpr_to_ast(sexpr[2])
            )

        if sexpr[0] == 'define':
            return Definition(
                sexpr[1],
                cls.sexpr_to_ast(sexpr[2])
            )

        if sexpr[0] == 'local':
            return Local(
                [Definition(d[0], cls.sexpr_to_ast(d[1])) for d in sexpr[1]],
                cls.sexpr_to_ast(sexpr[2])
            )

        if sexpr[0] == 'begin':
            return BodySequence(
                [cls.sexpr_to_ast(sexpr) for sexpr in sexpr[1:]]
            )

        "Function application"
        return App(
            cls.sexpr_to_ast(sexpr[0]),
            [cls.sexpr_to_ast(sexpr) for sexpr in sexpr[1:]]
        )

    @classmethod
    def tokens_to_sexpr(cls, tokens):
        if len(tokens) == 0:
            raise SyntaxError('unexpected end of expression')
        token = tokens.pop(0)
        if '(' == token:
            l = []
            while tokens[0] != ')':
                l.append(cls.tokens_to_sexpr(tokens))
            tokens.pop(0)  # pop off ')'
            return l
        elif ')' == token:
            raise SyntaxError('unexpected )')
        else:
            return cls.atom(token)

    @classmethod
    def atom(cls, token):
        if token == 'true':
            return True
        if token == 'false':
            return False
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                return token
