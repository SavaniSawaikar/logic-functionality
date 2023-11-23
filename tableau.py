
MAX_CONSTANTS = 10

class Proposition:

    def __init__(self, fmla):
        self.fmla = fmla.strip()

    def is_proposition(self):
        return self.fmla in ['p', 'q', 'r', 's']
    
    def is_negation(self):
        if self.fmla.startswith('~'):
            if self.fmla[1:].startswith('(') and self.fmla[1:].endswith(')'):
                if Proposition(self.fmla[2:-1]).is_proposition():
                    return False
            return True
        return False
    
    def is_binary_connective(self):
        if not (self.fmla.startswith('(') and self.fmla.endswith(')')):
            return None

        brackets = 0
        for i in range(1, len(self.fmla) - 1):
            if self.fmla[i] == '(':
                brackets += 1
            elif self.fmla[i] == ')':
                brackets -= 1
            elif brackets == 0:
                for conn in ['=>', '/\\', '\\/']:
                    if self.fmla[i:i+len(conn)] == conn:
                        left = self.fmla[1:i]
                        right = self.fmla[i+len(conn):-1]
                        if Proposition(left).is_fmla() and Proposition(right).is_fmla():
                            return left, conn, right
        return None
    
    def is_fmla(self):
        if ' ' in self.fmla or not check_matching_brackets(self.fmla):
            return False
        if self.is_proposition():
            return True
        elif self.is_negation():
            return True
        elif bool(self.is_binary_connective()):
            return True
        return False
    
    def parse(self):
        # Check if it is actually a formula
        if not self.is_fmla():
            return 0
        if self.is_negation():
            return 7
        elif self.is_binary_connective():
            return 8
        elif self.is_proposition():
            return 6

class FirstOrderLogic:
    def __init__(self, fmla):
        self.fmla = fmla.strip()

    def is_variable(self):
        return self.fmla in ['x', 'y', 'z', 'w']

    def is_predicate(self):
        predicates = ['P', 'Q', 'R', 'S']
        if len(self.fmla) > 4 and self.fmla[0] in predicates and self.fmla[1] == '(' and self.fmla[-1] == ')' and ',' in self.fmla:
            vars = self.fmla[2:-1].split(',')
            return len(vars) == 2 and all(var in ['x', 'y', 'z', 'w'] for var in vars)
        return False

    def is_negation(self):
        return self.fmla.startswith('~') and FirstOrderLogic(self.fmla[1:]).is_fmla()

    def is_universally_quantified(self):
        return self.fmla.startswith('A') and self.fmla[1] in ['x', 'y', 'z', 'w'] and FirstOrderLogic(self.fmla[2:]).is_fmla()

    def is_existentially_quantified(self):
        return self.fmla.startswith('E') and self.fmla[1] in ['x', 'y', 'z', 'w'] and FirstOrderLogic(self.fmla[2:]).is_fmla()

    def is_binary_connective(self):
        if not (self.fmla.startswith('(') and self.fmla.endswith(')')):
            return None

        brackets = 0
        for i in range(1, len(self.fmla) - 1):
            if self.fmla[i] == '(':
                brackets += 1
            elif self.fmla[i] == ')':
                brackets -= 1
            elif brackets == 0:
                for conn in ['=>', '/\\', '\\/']:
                    if self.fmla[i:i+len(conn)] == conn:
                        left = self.fmla[1:i]
                        right = self.fmla[i+len(conn):-1]
                        # check if there are any extra pairs of brackets on the end of both formulas
                        if FirstOrderLogic(left).is_fmla() and FirstOrderLogic(right).is_fmla():
                            return left, conn, right
        return None

    def is_fmla(self):
        if ' ' in self.fmla or not check_matching_brackets(self.fmla):
            return False
        return self.is_predicate() or self.is_negation() or self.is_universally_quantified() or self.is_existentially_quantified() or bool(self.is_binary_connective())

    def parse(self):
        if not self.is_fmla():
            return 0
        if self.is_predicate():
            return 1
        if self.is_negation():
            return 2
        if self.is_universally_quantified():
            return 3
        if self.is_existentially_quantified():
            return 4
        if self.is_binary_connective():
            return 5
    
# Check if a formula has matching brackets
def check_matching_brackets(fmla):
    stack = []
    for elem in fmla:
        if elem == '(':
            stack.append(elem)
        elif elem == ')':
            if len(stack) == 0:
                return False
            stack.pop()
    if len(stack) == 0:
        return True
    return False

# Parse a formula, consult parseOutputs for return values.
def parse(fmla):
    if FirstOrderLogic(fmla).is_fmla():
        return FirstOrderLogic(fmla).parse()
    elif Proposition(fmla).is_fmla():
        return Proposition(fmla).parse()
    else:
        return 0

# Return the LHS of a binary connective formula
def lhs(fmla):
    if FirstOrderLogic(fmla).is_fmla():
        if FirstOrderLogic(fmla).is_binary_connective():
            return FirstOrderLogic(fmla).is_binary_connective()[0]
        else:
            return ''
    elif Proposition(fmla).is_fmla():
        if Proposition(fmla).is_binary_connective():
            return Proposition(fmla).is_binary_connective()[0]
        else:
            return ''
    else:
        return ''

# Return the connective symbol of a binary connective formula
def con(fmla):
    if FirstOrderLogic(fmla).is_fmla():
        if FirstOrderLogic(fmla).is_binary_connective():
            return FirstOrderLogic(fmla).is_binary_connective()[1]
        else:
            return ''
    elif Proposition(fmla).is_fmla():
        if Proposition(fmla).is_binary_connective():
            return Proposition(fmla).is_binary_connective()[1]
        else:
            return ''
    return ''

# Return the RHS symbol of a binary connective formula
def rhs(fmla):
    if FirstOrderLogic(fmla).is_fmla():
        if FirstOrderLogic(fmla).is_binary_connective():
            return FirstOrderLogic(fmla).is_binary_connective()[2]
        else:
            return ''
    elif Proposition(fmla).is_fmla():
        if Proposition(fmla).is_binary_connective():
            return Proposition(fmla).is_binary_connective()[2]
        else:
            return ''
    return '' 


# You may choose to represent a theory as a set or a list
def theory(fmla):#initialise a theory with a single formula in it
    return [fmla]

#check for satisfiability
def sat(tableau):
#output 0 if not satisfiable, output 1 if satisfiable, output 2 if number of constants exceeds MAX_CONSTANTS
    return 0

#DO NOT MODIFY THE CODE BELOW
f = open('input.txt')

parseOutputs = ['not a formula',
                'an atom',
                'a negation of a first order logic formula',
                'a universally quantified formula',
                'an existentially quantified formula',
                'a binary connective first order formula',
                'a proposition',
                'a negation of a propositional formula',
                'a binary connective propositional formula']

satOutput = ['is not satisfiable', 'is satisfiable', 'may or may not be satisfiable']

firstline = f.readline()

PARSE = False
if 'PARSE' in firstline:
    PARSE = True

SAT = False
if 'SAT' in firstline:
    SAT = True

for line in f:
    if line[-1] == '\n':
        line = line[:-1]
    parsed = parse(line)

    if PARSE:
        output = "%s is %s." % (line, parseOutputs[parsed])
        if parsed in [5,8]:
            output += " Its left hand side is %s, its connective is %s, and its right hand side is %s." % (lhs(line), con(line) ,rhs(line))
        print(output)

    if SAT:
        if parsed:
            tableau = [theory(line)]
            print('%s %s.' % (line, satOutput[sat(tableau)]))
        else:
            print('%s is not a formula.' % line)