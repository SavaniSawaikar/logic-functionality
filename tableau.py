
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
        elif self.is_negation() and Proposition(self.fmla[1:]).is_fmla():
            return True
        elif bool(self.is_binary_connective()):
            return True
        return False
    
    def parse(self):
        if not self.is_fmla():
            return 0
        if self.is_negation():
            return 7
        elif self.is_binary_connective():
            return 8
        elif self.is_proposition():
            return 6
        
    def is_alpha(self):
        if con(self.fmla) == '/\\':
            return True
        elif self.is_negation() and con(self.fmla[1:]) == '=>':
            return True
        elif self.is_negation() and con(self.fmla[1:]) == '\\/':
            return True
        
    def is_beta(self):
        if con(self.fmla) == '\\/':
            return True
        elif con(self.fmla) == '=>':
            return True
        elif self.is_negation() and con(self.fmla[1:]) == '/\\':
            return True
        
class FirstOrderLogic:
    def __init__(self, fmla):
        self.fmla = fmla.strip()

    def is_variable(self):
        return self.fmla in ['x', 'y', 'z', 'w']

    def is_predicate(self):
        predicates = ['P', 'Q', 'R', 'S']
        if len(self.fmla) > 4 and self.fmla[0] in predicates and self.fmla[1] == '(' and self.fmla[-1] == ')' and ',' in self.fmla:
            vars = self.fmla[2:-1].split(',')
            return len(vars) == 2 and all(var in ['x', 'y', 'z', 'w'] + constants for var in vars)
        return False

    def is_negation(self):
        if self.fmla.startswith('~'):
            if FirstOrderLogic(self.fmla[1:]).is_fmla():
                return True
            return True
        return False

    def is_universally_quantified(self):
        return self.fmla.startswith('A') and self.fmla[1] in ['x', 'y', 'z', 'w'] + constants and FirstOrderLogic(self.fmla[2:]).is_fmla()

    def is_existentially_quantified(self):
        return self.fmla.startswith('E') and self.fmla[1] in ['x', 'y', 'z', 'w'] + constants and FirstOrderLogic(self.fmla[2:]).is_fmla()

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
                for conn in ['=>', '/\\', '\/']:
                    if self.fmla[i:i+len(conn)] == conn:
                        left = self.fmla[1:i]
                        right = self.fmla[i+len(conn):-1]
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
    
    def is_alpha(self):
        if con(self.fmla) == '/\\':
            return True
        elif self.is_negation() and con(self.fmla[1:]) == '=>':
            return True
        elif self.is_negation() and con(self.fmla[1:]) == '\\/':
            return True
        
    def is_beta(self):
        if con(self.fmla) == '\\/':
            return True
        elif con(self.fmla) == '=>':
            return True
        elif self.is_negation() and con(self.fmla[1:]) == '/\\':
            return True
        
    def is_delta(self):
        if self.is_existentially_quantified():
            return True
        elif self.is_negation() and FirstOrderLogic(self.fmla[1:]).is_universally_quantified():
            return True
        
    def is_gamma(self):
        if self.is_universally_quantified():
            return True
        elif self.is_negation() and FirstOrderLogic(self.fmla[1:]).is_existentially_quantified():
            return True

def clean_negations(fmla):
    negations = 0
    if fmla.startswith('~'):
        while fmla.startswith('~'):
            fmla = fmla[1:]
            negations += 1
    
    if negations % 2 == 0:
        return fmla
    else:
        return '~' + fmla

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

def parse(fmla):
    if fmla[0:2] + fmla[3:] == "~()":
        return 0
    if Proposition(fmla).is_fmla():
        return Proposition(fmla).parse()
    elif FirstOrderLogic(fmla).is_fmla():
            return FirstOrderLogic(fmla).parse()
    else:
        return 0


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

def lhsclean(fmla):
    return clean_negations(lhs(fmla))

def rhsclean(fmla):
    return clean_negations(rhs(fmla))


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


def theory(fmla):
    return [fmla]

def expanded(branch):
    for fmla in branch:
        fmla = clean_negations(fmla)

        if Proposition(fmla).is_fmla() and Proposition(fmla).is_binary_connective() or (Proposition(fmla).is_fmla() and Proposition(fmla).is_negation() and Proposition(fmla[1:]).is_binary_connective()):
            return False  
        elif (FirstOrderLogic(fmla).is_fmla() and FirstOrderLogic(fmla).is_binary_connective()) or (FirstOrderLogic(fmla).is_fmla() and FirstOrderLogic(fmla).is_negation() and FirstOrderLogic(fmla[1:]).is_binary_connective()) or (FirstOrderLogic(fmla).is_fmla() and FirstOrderLogic(fmla).is_universally_quantified()) or (FirstOrderLogic(fmla).is_fmla() and FirstOrderLogic(fmla).is_existentially_quantified()) or (FirstOrderLogic(fmla).is_fmla() and FirstOrderLogic(fmla).is_negation() and FirstOrderLogic(fmla[1:]).is_universally_quantified()) or (FirstOrderLogic(fmla).is_fmla() and FirstOrderLogic(fmla).is_negation() and FirstOrderLogic(fmla[1:]).is_existentially_quantified()):
            return False 
        
    return True

def contradictory(branch):
    for fmla in branch:
        if Proposition(fmla).is_fmla():
            if Proposition(fmla).is_proposition():
                if fmla in branch and '~'+fmla in branch:
                    return True
            if Proposition(fmla).is_negation():
                if fmla in branch and fmla[1:] in branch:
                    return True
        elif FirstOrderLogic(fmla).is_fmla(): 
            if FirstOrderLogic(fmla).is_predicate():
                if fmla in branch and '~'+fmla in branch:
                    return True
            if FirstOrderLogic(fmla).is_negation() and FirstOrderLogic(fmla[1:]).is_predicate():
                if fmla in branch and fmla[1:] in branch:
                    return True
    return False

def pick_non_literal(branch):
    for fmla in reversed(branch):
        if FirstOrderLogic(fmla).is_fmla():
            if FirstOrderLogic(fmla).is_alpha():
                return fmla
    
    for fmla in reversed(branch):
        if FirstOrderLogic(fmla).is_fmla():
            if FirstOrderLogic(fmla).is_delta():
                return fmla
            
    for fmla in reversed(branch):
        if FirstOrderLogic(fmla).is_fmla():
            if FirstOrderLogic(fmla).is_beta():
                return fmla
            
    for fmla in reversed(branch):
        if FirstOrderLogic(fmla).is_fmla():
            if FirstOrderLogic(fmla).is_gamma():
                return fmla
            
    for fmla in reversed(branch):
        if Proposition(fmla).is_fmla():
            if Proposition(fmla).is_binary_connective():
                return fmla
            if Proposition(fmla).is_negation() and Proposition(fmla[1:]).is_binary_connective():
                return fmla
        elif FirstOrderLogic(fmla).is_fmla():
            if FirstOrderLogic(fmla).is_binary_connective():
                return fmla
            if FirstOrderLogic(fmla).is_negation() and (FirstOrderLogic(fmla[1:]).is_binary_connective() or FirstOrderLogic(fmla[1:]).is_universally_quantified() or FirstOrderLogic(fmla[1:]).is_existentially_quantified):
                return fmla
            if FirstOrderLogic(fmla).is_universally_quantified():
                return fmla
            if FirstOrderLogic(fmla).is_existentially_quantified():
                return fmla
    return None

def pick_new_constant():
    for i in 'abcdefghijklmnotuv':
        if i not in constants:
            constants.append(i)
            return i

def replace_variable_in_scope(fmla, old_var, new_var):

    if len(fmla) < 3 or fmla[1] != old_var or fmla[0] not in ['A', 'E']:
        return fmla
 
    scope = fmla[2:]  

    modified_scope = scope.replace(old_var, new_var)

    return modified_scope

def pick_next_constant(last_constant = None):
    if last_constant:
        next_idx = constants.index(last_constant) + 1
        if next_idx < len(constants):
            return constants[next_idx]
        else:
            return None
    if not last_constant and len(constants) > 0:
        return constants[0]
    return pick_new_constant()

global constants
constants = []


def sat(tableau):
    last_constant_used = {}
    global constants
    constants = []
    while tableau:
        branch = tableau.pop()
        if expanded(branch) and not contradictory(branch):
            return 1
        else:
            fmla = pick_non_literal(branch)
            if fmla:
                fmla_index = branch.index(fmla)
                fmla = clean_negations(fmla)
                branch[fmla_index] = fmla


                if Proposition(fmla).is_fmla():
                    
                    if Proposition(fmla).is_alpha():
                        if con(fmla) == '/\\':
                            branch.remove(fmla)
                            branch = branch + [lhsclean(fmla), rhsclean(fmla)]
                            if not contradictory(branch) and branch not in tableau:
                                tableau.append(branch)
                        elif Proposition(fmla).is_negation() and con(fmla[1:]) == '=>':
                            branch.remove(fmla)
                            branch = branch + [lhsclean(fmla[1:]), clean_negations('~' + rhsclean(fmla[1:]))]
                            if not contradictory(branch) and branch not in tableau:
                                tableau.append(branch)
                        elif Proposition(fmla).is_negation() and con(fmla[1:]) == '\\/':
                            branch.remove(fmla)
                            branch = branch + [clean_negations('~' + lhsclean(fmla[1:])), clean_negations('~' + rhsclean(fmla[1:]))]
                            if not contradictory(branch) and branch not in tableau:
                                tableau.append(branch)
                    elif Proposition(fmla).is_beta():
                            branch.remove(fmla)
                            if con(fmla) == '\\/':
                                new_branch1 = branch + [lhsclean(fmla)]
                                new_branch2 = branch + [rhsclean(fmla)]
                                if not contradictory(new_branch1) and new_branch1 not in tableau:
                                    tableau.append(new_branch1)
                                if not contradictory(new_branch2) and new_branch2 not in tableau:
                                    tableau.append(new_branch2)

                            elif con(fmla) == '=>':
                                new_branch1 = branch + [clean_negations('~' + lhsclean(fmla))]
                                new_branch2 = branch + [rhsclean(fmla)]
                                if not contradictory(new_branch1) and new_branch1 not in tableau:
                                    tableau.append(new_branch1)
                                if not contradictory(new_branch2) and new_branch2 not in tableau:
                                    tableau.append(new_branch2)

                            elif Proposition(fmla).is_negation() and con(fmla[1:]) == '/\\':
                                new_branch1 = branch + [clean_negations('~' + lhsclean(fmla[1:]))]
                                new_branch2 = branch + [clean_negations('~' + rhsclean(fmla[1:]))]
                                if not contradictory(new_branch1) and new_branch1 not in tableau:
                                    tableau.append(new_branch1)
                                if not contradictory(new_branch2) and new_branch2 not in tableau:
                                    tableau.append(new_branch2)

                elif FirstOrderLogic(fmla).is_fmla():
                    if FirstOrderLogic(fmla).is_alpha():                        
                        if con(fmla) == '/\\':
                            branch.remove(fmla)
                            branch = branch + [lhsclean(fmla), rhsclean(fmla)]
                            if not contradictory(branch) and branch not in tableau:
                                tableau.append(branch)
                        elif FirstOrderLogic(fmla).is_negation() and con(fmla[1:]) == '=>':
                            branch.remove(fmla)
                            branch = branch + [lhsclean(fmla[1:]), clean_negations('~' + rhsclean(fmla[1:]))]
                            if not contradictory(branch) and branch not in tableau:
                                tableau.append(branch)
                        elif FirstOrderLogic(fmla).is_negation() and con(fmla[1:]) == '\\/':
                            branch.remove(fmla)
                            branch = branch + [clean_negations('~' + lhsclean(fmla[1:])), clean_negations('~' + rhsclean(fmla[1:]))]
                            if not contradictory(branch) and branch not in tableau:
                                tableau.append(branch)

                    elif FirstOrderLogic(fmla).is_beta():
                            branch.remove(fmla)
                            if con(fmla) == '\\/':
                                new_branch1 = branch + [lhsclean(fmla)]
                                new_branch2 = branch + [rhsclean(fmla)]
                                if not contradictory(new_branch1) and new_branch1 not in tableau:
                                    tableau.append(new_branch1)
                                if not contradictory(new_branch2) and new_branch2 not in tableau:
                                    tableau.append(new_branch2)

                            elif con(fmla) == '=>':
                                new_branch1 = branch + [clean_negations('~' + lhsclean(fmla))]
                                new_branch2 = branch + [rhsclean(fmla)]
                                if not contradictory(new_branch1) and new_branch1 not in tableau:
                                    tableau.append(new_branch1)
                                if not contradictory(new_branch2) and new_branch2 not in tableau:
                                    tableau.append(new_branch2)

                            elif FirstOrderLogic(fmla).is_negation() and con(fmla[1:]) == '/\\':
                                new_branch1 = branch + [clean_negations('~' + lhsclean(fmla[1:]))]
                                new_branch2 = branch + [clean_negations('~' + rhsclean(fmla[1:]))]
                                if not contradictory(new_branch1) and new_branch1 not in tableau:
                                    tableau.append(new_branch1)
                                if not contradictory(new_branch2) and new_branch2 not in tableau:
                                    tableau.append(new_branch2)

                    elif FirstOrderLogic(fmla).is_delta():
                        if len(constants) > MAX_CONSTANTS:
                            return 2
                        if FirstOrderLogic(fmla).is_existentially_quantified():
                            branch.remove(fmla)
                            fmla = replace_variable_in_scope(fmla, fmla[1], pick_new_constant())
                            branch = branch + [fmla]
                            if not contradictory(branch) and branch not in tableau:
                                tableau.append(branch)
                        elif FirstOrderLogic(fmla).is_negation() and FirstOrderLogic(fmla[1:]).is_universally_quantified():
                            branch.remove(fmla)
                            fmla = replace_variable_in_scope(fmla[1:], fmla[2], pick_new_constant())
                            branch = branch + [clean_negations('~' + fmla)]
                            if not contradictory(branch) and branch not in tableau:
                                tableau.append(branch)

                    elif FirstOrderLogic(fmla).is_gamma():

                        if len(constants) > MAX_CONSTANTS:
                            return 2
                        if FirstOrderLogic(fmla).is_universally_quantified():
                            quantified_var = fmla[1]
                            last_constant = None
                            if fmla in last_constant_used:
                                last_constant = last_constant_used[fmla]
                            new_term = pick_next_constant(last_constant)
                            if new_term is None:
                                branch.remove(fmla)
                                tableau.insert(0, branch)
                                continue
                            last_constant_used[fmla] = new_term
                            instantiated_fmla = replace_variable_in_scope(fmla, quantified_var, new_term)
                            if instantiated_fmla not in branch:
                                branch.insert(0, instantiated_fmla)
                            branch.remove(fmla)
                            branch.insert(0, fmla)
                            if not contradictory(branch) and branch not in tableau:
                                tableau.insert(0, branch)
                        elif FirstOrderLogic(fmla).is_negation() and FirstOrderLogic(fmla[1:]).is_existentially_quantified():
                            quantified_var = fmla[2]
                            last_constant = None
                            if fmla in last_constant_used:
                                last_constant = last_constant_used[fmla]
                            new_term = pick_next_constant(last_constant)
                            if new_term is None:
                                branch.remove(fmla)
                                tableau.insert(0, branch)
                                continue
                            last_constant_used[fmla] = new_term
                            instantiated_fmla = replace_variable_in_scope(fmla, quantified_var, new_term)
                            if instantiated_fmla not in branch:
                                branch.insert(0, instantiated_fmla)
                            branch.remove(fmla)
                            branch.insert(0, fmla)
                            if not contradictory(branch) and branch not in tableau:
                                tableau.insert(0, branch)
                                
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