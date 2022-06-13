import os
import sys
import re
import ast

error_dict = {"S001": "Too long",
              "S002": "Indentation is not a multiple of four",
              "S003": "Unnecessary semicolon",
              "S004": "At least two spaces required before inline comments",
              "S005": "TODO found",
              "S006": "More than two blank lines used before this line"}

output_list = []


def s001(string):
    if len(string) > 79:
        return "S001"
    else:
        return False


def s002(string):
    func_tuple = tuple(string)
    first_sign = [i for i in func_tuple if i != " "][0]
    condition_1 = len(string[:string.index(first_sign)]) % 4 != 0
    if condition_1:
        return "S002"
    else:
        return False


def s003(string):
    try:
        comment_start = string.index("#")
        if ";" in string[:comment_start]:
            return "S003"
        else:
            return False
    except ValueError:
        if string.endswith(";\n"):
            return "S003"
        else:
            return False


def s004(string):
    try:
        comment_start = string.index("#")
        condition_1 = string[comment_start - 2:comment_start] != "  "
        condition_2 = comment_start > 2
        if condition_1 and condition_2:
            return "S004"
        else:
            return False
    except ValueError:
        return False


def s005(string):
    try:
        comment_start = string.index("#")
        if "todo" in string[comment_start:].lower():
            return "S005"
        else:
            return False
    except ValueError:
        return False


def s006(error_line, line_number, path_to_file):
    condition = error_line == "\n"
    if line_number > 2 and condition:
        output_list.append(f"{path_to_file}: Line {line_number}: S006 "
                           + error_dict["S006"])


def line_checker(string, line_number, path_to_file):
    check_1 = s001(string)
    check_2 = s002(string)
    check_3 = s003(string)
    check_4 = s004(string)
    check_5 = s005(string)
    check_list = (check_1, check_2, check_3, check_4, check_5)
    if any(check_list):
        for check in check_list:
            if bool(check) is True:
                output_list.append(f"{path_to_file}: Line "
                                   + f"{line_number}:"
                                   + f" {check} {error_dict[check]}")


def s007(string):
    condition_class = re.match(r" *class", string)
    condition_def = re.match(r" *def", string)
    if condition_class:
        construction_name = "'class'"
        if re.match(r" *class \w", string) is None:
            problem = f"Too many spaces after {construction_name}"
            return "S007", problem
    elif condition_def:
        construction_name = "'def'"
        if re.match(r" *def \w", string) is None:
            problem = f"Too many spaces after {construction_name}"
            return "S007", problem
    else:
        return False


def s008(string):
    condition_class = re.match(r" *class", string)
    func_condition = re.match(r" *class +[A-Z][a-z]+[A-Z]?[a-z]*", string)
    if condition_class and (func_condition is None):
        class_in_string = string.index("class") + 5
        if ":" in string:
            sign_index = string.index(":")
            class_name = string[class_in_string:sign_index].lstrip()
            problem = f"Class name '{class_name}'"\
                      + " should be written in CamelCase"
            return "S008", problem
        elif "(" in string:
            sign_index = string.index("(")
            class_name = string[class_in_string:sign_index].lstrip()
            problem = f"Class name '{class_name}'"\
                      + " should be written in CamelCase"
            return "S008", problem
    else:
        return False


def s009(string):
    condition_def = re.match(r" *def", string)
    func_condition = re.match(r" *def +_{,2}[a-z\d]+_?[a-z\d]*_{,2}\(",
                              string)
    if condition_def and (func_condition is None):
        def_in_string = string.index("def") + 4
        sign_index = string.index("(")
        func_name = string[def_in_string:sign_index]
        problem = f"Function name '{func_name}'"\
                  + " should be written in snake_case"
        return "S009", problem
    else:
        return False


def check_names(string, line_number, path_to_file):
    check1 = s007(string)
    check2 = s008(string)
    check3 = s009(string)
    check_list = (check1, check2, check3)
    if any(check_list):
        for check in check_list:
            if bool(check) is True:
                output_list.append(f"{path_to_file}: Line "
                                   + f"{line_number}:"
                                   + f" {check[0]} {check[1]}")


class ArgumentName(ast.NodeVisitor):

    def __init__(self):
        self.wrong_list = []

    def visit_FunctionDef(self, node):

        for arg in node.args.args:
            condition = re.match(r"_{,2}[a-z\d]+_?[a-z\d]*_{,2}", arg.arg)
            if condition:
                self.wrong_list.append(False)
            else:
                self.wrong_list.append(
                    f": Line {arg.lineno}: S010 Argument name '{arg.arg}' "
                    f"should be snake_case")
        self.generic_visit(node)


class VariableCase(ast.NodeVisitor):

    def __init__(self):
        self.wrong_list = []

    def visit_FunctionDef(self, node):

        for assign in node.body:
            if isinstance(assign, ast.Assign):
                for name in assign.targets:

                    template = r"_{,2}[a-z\d]+_?[a-z\d]*_{,2}"

                    if isinstance(name, ast.Attribute):
                        problem = f": Line {name.lineno}: S011 Variable " \
                                  f"'{name.value.id}' in function " \
                                  f"should be snake_case"
                        condition = re.match(template, name.value.id)

                        if condition:
                            self.wrong_list.append(False)
                        else:
                            self.wrong_list.append(problem)
                    else:
                        problem = f": Line {name.lineno}: S011 Variable " \
                                  f"'{name.id}' in function should be " \
                                  f"snake_case"

                        condition = re.match(template, name.id)

                        if condition:
                            self.wrong_list.append(False)
                        else:
                            self.wrong_list.append(problem)

        self.generic_visit(node)


class MutableValue(ast.NodeVisitor):

    def __init__(self):
        self.wrong_list = []

    def visit_FunctionDef(self, node):

        for constant in node.args.defaults:
            cond1 = isinstance(constant, ast.List)
            cond2 = isinstance(constant, ast.Dict)
            cond3 = isinstance(constant, ast.Set)
            all_cond = (cond1, cond2, cond3)
            if any(all_cond):
                self.wrong_list.append(f": Line {constant.lineno}: S012 "
                                       f"Default argument value is mutable")
            else:
                self.wrong_list.append(False)
        self.generic_visit(node)


def ast_checker(file_read, path_to_file):
    error_list = []
    tree = ast.parse(file_read)
    check_1 = ArgumentName()
    check_1.visit(tree)
    for response in check_1.wrong_list:
        if response is not False:
            error_list.append(path_to_file + response)
    check_2 = VariableCase()
    check_2.visit(tree)
    for response in check_2.wrong_list:
        if response is not False:
            error_list.append(path_to_file + response)
    check_3 = MutableValue()
    check_3.visit(tree)
    for response in check_3.wrong_list:
        if response is not False:
            error_list.append(path_to_file + response)
    output_list.extend(error_list)


path_var = sys.argv
if len(path_var) != 2:
    print("The script should be called with one argument, "
          "path to the file or directory")
else:
    if path_var[1].endswith(".py"):
        file = open(path_var[1], "r")
        ast_checker(file.read(), path_var[1])
        file.close()

        file = open(path_var[1], "r")
        lines_list = file.readlines()

        line_counter = 1

        for line in lines_list:

            line_checker(line, line_counter, path_var[1])

            s006_condition1 = lines_list[line_counter - 2] == "\n"
            s006_condition2 = lines_list[line_counter - 3] == "\n"
            condition_tuple = (s006_condition1, s006_condition2,
                               line != "\n")

            if all(condition_tuple):
                s006(lines_list[line_counter - 4], line_counter, path_var[1])

            check_names(line, line_counter, path_var[1])

            line_counter += 1

        file.close()

    else:
        for root, dirs, files in os.walk(path_var[1]):
            for file_name in files:
                if file_name.endswith(".py"):
                    path = os.path.join(root, file_name)
                    file = open(path, "r")
                    ast_checker(file.read(), path)
                    file.close()

                    file = open(path, "r")
                    lines_list = file.readlines()

                    line_counter = 1

                    for line in lines_list:

                        line_checker(line, line_counter, path)

                        s006_condition1 = lines_list[line_counter - 2] == "\n"
                        s006_condition2 = lines_list[line_counter - 3] == "\n"
                        condition_tuple = (s006_condition1, s006_condition2,
                                           line != "\n")

                        if all(condition_tuple):
                            s006(lines_list[line_counter - 4],
                                 line_counter, path)

                        check_names(line, line_counter, path)

                        line_counter += 1

                    file.close()


def sort_func(x):
    first = x[:x.index(": Line")]
    second_index = x[x.index(": Line") + 6:x.index(": S0")]
    second = int("".join(second_index.split()))

    return first, second


output_list.sort(key=sort_func)

for output in output_list:
    print(output)
