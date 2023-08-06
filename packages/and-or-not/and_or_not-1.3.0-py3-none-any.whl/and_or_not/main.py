from termcolor import cprint
class Not():
    """
    Hey there, if you are looking for a beginner guide to not operators, then, follow along with this!\n
    Because this is a beginner guide, so I'll use print instead of return just for the sake of simplicity.\n
    PLEASE NOTE THAT IT ONLY SUPPORTS == AND != OPERATOR JUST TO GET YOU A SENSE OF LOGICAL OPERATORS
    """
    SUPPORTED_OPERATORS = ["!=", "=="]
    def __init__(self, *expression):
        """
        Please, in the parentheses, type in a string(wrapped with double/single quotes), something like ("1 == 3").\n
        Well actually, I'll just assume you know these basics, so that I don't have to spend time writing tutorials here : -) -|--<\n
        But PLEASE PLEASE PLEASE provide a STRING!!!\n
        But PLEASE PLEASE PLEASE provide a STRING!!!\n
        But PLEASE PLEASE PLEASE provide a STRING!!!\n
        """
        
        if len(expression) == 0:
            cprint("Please provide an expression!", "red")
        elif len(expression) > 1:
            cprint("Please provide ONLY one expression", "red")
        elif "!=" not in expression[0] and "==" not in expression[0]:
            cprint("Please use an supported operator(== or !=)", "red")
        else:
            self.expression = expression[0]
    def evaluate(self):
        return(self.reverse())
    def show(self):
        print(f"not {self.expression}")
    def explain(self):
        val = self.evaluate()
        if val == False:
            print(f"The entire expression(not {self.expression}) is False because the provided expression({self.expression}) is True.\n\n\nAlright, I know this may sound a bit confusing, so let's start from scratch.\n\nSo what the not operator does, is basically reverses the boolean value.\nWhich is to say, if the original expression is True, it reverses the value and turns it into False, which can be represented as \n\n<Not True == False>\n\n and vice versa.")
        else:
            print(f"The entire expression(not {self.expression}) is True because the provided expression ({self.expression}) is False.\n\n\nAlright, I know this may sound a bit confusing, so let's start from scratch.\n\nSo what the not operator does, is basically reverses the boolean value.\nWhich is to say, if the original expression is False, it reverses the value and turns it into True, which can be represented as \n\n<Not False == True>\n\nand vice versa.")
    def reverse(self):
        if "==" in self.expression:
            copy = self.expression
            a = copy.split("==")[0].strip()
            b = copy.split("==")[1].strip()
            if a == b:
                res = True
            else:
                res = False
        else:
            copy = self.expression
            a = copy.split("!=")[0].strip()
            b = copy.split("!=")[1].strip()
            if a != b:
                res = True
            else:
                res = False
        if res == True:
            return False
        else:
            return True
    def pythonic(self):
        print(f"not {self.expression}")

class And():
    """
    Hey there, if you are looking for a beginner guide to and operators, then, follow along with this!\n
    Because this is a beginner guide, so I'll use print instead of return just for the sake of simplicity.\n
    PLEASE NOTE THAT IT ONLY SUPPORTS == AND != OPERATOR JUST TO GET YOU A SENSE OF LOGICAL OPERATORS
    """
    SUPPORTED_OPERATORS = ["!=", "=="]
    """
        Please, in the parentheses, type in one or more strings(wrapped with double/single quotes), something like ("1 == 3", "1 == 1").\n
        Well actually, I'll just assume you know these basics, so that I don't have to spend time writing tutorials here : -) -|--<\n
        But PLEASE PLEASE PLEASE provide STRINGS!!!\n
        But PLEASE PLEASE PLEASE provide STRINGS!!!\n
        But PLEASE PLEASE PLEASE provide STRINGS!!!\n
    """
    def __init__(self, *expressions:str):
        if len(expressions) == 0 :
            cprint("Please provide AT LEAST one expression!", "red")
        self.expressions = []
        for i in expressions:
            if "!=" not in i and "==" not in i:
                cprint("Please use an supported operator(== or !=)", "red")
                break
            self.expressions.append(i)

    def evaluate(self):
        """
        Please do not use this function, you'll get literally nothing!!!
        """
        for i in self.expressions:
            if "==" in i:
                copy = i
                a = copy.split("==")[0].strip()
                b = copy.split("==")[1].strip()
                if a != b:
                    return False, i
            else:
                copy = i
                a = copy.split("!=")[0].strip()
                b = copy.split("!=")[1].strip()
                if a == b:
                    return False, i
            
        return True, None

    def pythonic(self):
        """
        Do not try to use this function!!! You would literally get nothing!
        """
        tmp = ""
        for i in range(len(self.expressions) - 1):
            tmp += f"{self.expressions[i]} and "
        tmp += f"{self.expressions[-1]}"
        return tmp
    def display(self):
        print(self.pythonic())
    def explain(self):
        res, wrong = self.evaluate()
        if res == False:
            print(f"The evaluated expression: <{self.pythonic()}> is False because, one of its expressions: {wrong} is False, recall that: \n'When you use an and operator, it ONLY evaluates to True when both the expressions are True.', i.e. if one of the expressions it takes is wrong, the whole thing turns into False.")
        else:
            print(f"The evaluated expression: <{self.pythonic()}> is True because all the {len(self.expressions)} expressions evaluate as True. \nWhen you use an and operator, it ONLY evaluates to True when both the expressions are True.")
    def result(self):
        res, trash = self.evaluate()
        return res

class Or():
    """
    Hey there, if you are looking for a beginner guide to or operators, then, follow along with this!\n
    Because this is a beginner guide, so I'll use print instead of return just for the sake of simplicity.\n
    PLEASE NOTE THAT IT ONLY SUPPORTS == AND != OPERATOR JUST TO GET YOU A SENSE OF LOGICAL OPERATORS
    """
    SUPPORTED_OPERATORS = ["!=", "=="]
    
    def __init__(self, *expressions:str):
        """
        Please, in the parentheses, type in one or more strings(wrapped with double/single quotes), something like ("1 == 3", "1 == 1").\n
        Well actually, I'll just assume you know these basics, so that I don't have to spend time writing tutorials here : -) -|--<\n
        But PLEASE PLEASE PLEASE provide STRINGS!!!\n
        But PLEASE PLEASE PLEASE provide STRINGS!!!\n
        But PLEASE PLEASE PLEASE provide STRINGS!!!\n
        """
        if len(expressions) == 0 :
            cprint("Please provide AT LEAST one expression!", "red")
        self.expressions = []
        for i in expressions:
            if "!=" not in i and "==" not in i:
                cprint("Please use an supported operator(== or !=)", "red")
                break
            self.expressions.append(i)

    def evaluate(self):
        """
        Please do not use this function, you'll get literally nothing!!!
        """
        for i in self.expressions:
            if "==" in i:
                copy = i
                a = copy.split("==")[0].strip()
                b = copy.split("==")[1].strip()
                if a == b:
                    return True, i
            else:
                copy = i
                a = copy.split("!=")[0].strip()
                b = copy.split("!=")[1].strip()
                if a != b:
                    return True, i
            
        return False, None

    def pythonic(self):
        """
        Do not try to use this function!!! You would literally get nothing!
        """
        tmp = ""
        for i in range(len(self.expressions) - 1):
            tmp += f"{self.expressions[i]} and "
        tmp += f"{self.expressions[-1]}"
        return tmp
    def display(self):
        print(self.pythonic())
    def explain(self):
        res, correct = self.evaluate()
        if res == False:
            print(f"The evaluated expression: <{self.pythonic()}> is False because, because none of its expressions are True.\nRecall the rules of |or| operators: 'Evaluates to True when one of its expressions is True(The other one does not matter). Evaluates to False when none of the expressions are True'")
        else:
            print(f"The evaluated expression: <{self.pythonic()}> is True because one of its expressions: <{correct}> is True.\nPer the rule: An |or| operator evaluates to True when one of its expressions is True(The other one does not matter). Evaluates to False when none of the expressions are True")
    def result(self):
        res, trash = self.evaluate()
        return res

