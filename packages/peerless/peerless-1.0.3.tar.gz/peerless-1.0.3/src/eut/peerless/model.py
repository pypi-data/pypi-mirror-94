"""
This module contains the classes and function needed to model a problem.

The principal class is :class:`eut.peerless.model.Model`, it will hold
the variables, constraints and the objective function.

Almost all classes extend :class:`eut.peerless.model.Function`, and this class
has some special methods overriden so creating expressions is as close
as possible as to writting algebraic expressions. The overriden special
methods are:

* __add__(self, other):
* __radd__(self, other):
* __sub__(self, other):
* __rsub__(self, other):
* __mul__(self, other):
* __rmul__(self, other):
* __truediv__(self, other):
* __rtruediv__(self, other):
* __mod__(self, other):
* __pow__(self, other):
* __neg__(self):
* __le__(self, other):
* __ge__(self, other):
* __eq__(self, other):

The last three methods return :class:`eut.peerless.model.Constraint` instead of
a function. These constraints can then be added to a model.
"""

import abc
import collections
import json
import math
import numbers
import sys

class _Serializable(abc.ABC):
    """Abstract class. All classes that will be sent to the server,
    but the Model, must extend this class."""
    def __init__(self):
        pass

    @abc.abstractmethod
    def serialize(self):
        """Returns a json representation of the object"""
        pass

    @classmethod
    @abc.abstractmethod
    def deserialize(cls, *args, **kwds):
        """Creates an object from the serialized content given in the
        arguments."""
        pass

    @staticmethod
    def get_class_name(obj):
        """Auxiliary method to return the name of the class"""
        return obj.__class__.__name__

class _NamedObject:
    """An object with a name"""
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._set_name(value)

    def _set_name(self, value):
        self._name = value

    def __str__(self):
        return str(self._name)

class _Number(_Serializable):
    """A _Number represents just that, it has a value"""
    def __init__(self, value):
        self.__value = value
        self.tag = "number"

    @property
    def is_linear(self):
        return True

    @property
    def value(self):
        return self.__value

    def serialize(self):
        return {"class": _Serializable.get_class_name(self),
                "value": self.value}

    @classmethod
    def deserialize(cls, model, content):
        return model._get_number(content["value"])

    def __call__(self, solution):
        return self.value

    def __str__(self):
        return str(self.value)

def Expression(constant=0):
    """Returns a constant function initialized the given value

    :param constant: the value to initialize the expression to
    :return: a number function
    """
    return _Number(constant)

class Function(_Serializable):
    """Base class for all other functions in the module.
    A function can be evaluated on a :class:`eut.peerless.model.Solution`.
    """
    def __init__(self, *arguments, tag="unknown"):
        _Serializable.__init__(self)
        self.arguments = [_Number(a) if isinstance(a, numbers.Number) else a
                          for a in arguments]
        self.tag = tag

    @property
    def is_linear(self):
        """:return: True if the function and all its arguments are linear"""
        return False

    def serialize(self):
        return {"class": _Serializable.get_class_name(self),
                "arguments": [arg.serialize() for arg in self.arguments]}

    @classmethod
    def deserialize(self, model, content):
        module = sys.modules[__name__]
        clazz = getattr(module, content["class"])
        if clazz is _Number or clazz is _Variable:
            return clazz.deserialize(model, content)
        arguments = []
        for arg in content["arguments"]:
            arg_clazz = getattr(module, arg["class"])
            obj = arg_clazz.deserialize(model, arg)
            arguments.append(obj)
        return clazz(*arguments)

    def __add__(self, other):
        """
        :return: self + other
        :rtype: eut.peerless.model.add
        """
        return add(self, other)

    def __radd__(self, other):
        """
        :return: other + self
        :rtype: eut.peerless.model.add
        """
        return add(other, self)

    def __sub__(self, other):
        """
        :return: self - other
        :rtype: eut.peerless.model.sub
        """
        return sub(self, other)

    def __rsub__(self, other):
        """
        :return: -self + other
        :rtype: eut.peerless.model.add
        """
        return add(-self, other)

    def __mul__(self, other):
        """
        :return: self * other
        :rtype: eut.peerless.model.mul
        """
        return mul(self, other)

    def __rmul__(self, other):
        """
        :return: other * self
        :rtype: eut.peerless.model.mul
        """
        return mul(other, self)

    def __truediv__(self, other):
        """
        :return: self / other
        :rtype: eut.peerless.model.truediv
        """
        return truediv(self, other)

    def __rtruediv__(self, other):
        """
        :return: other * (1 / self)
        :rtype: eut.peerless.model.mul
        """
        return other * truediv(_Number(1), self)

    def __mod__(self, other):
        """
        :return: self % other
        :rtype: eut.peerless.model.mod
        """
        return mod(self, other)

    def __pow__(self, other):
        """
        :return: self**other
        :rtype: eut.peerless.model.pow
        """
        return ppow(self, other)

    def __neg__(self):
        """
        :return: -self
        :rtype: eut.peerless.model.mul
        """
        return mul(_Number(-1), self)

    def __le__(self, other):
        """
        :return: the constraint self <= other
        :rtype: eut.peerless.model.Constraint
        """
        return Constraint(self, Constraint.le, other)

    def __ge__(self, other):
        """
        :return: the constraint self >= other
        :rtype: eut.peerless.model.Constraint
        """
        return Constraint(self, Constraint.ge, other)

    def __eq__(self, other):
        """
        :return: the constraint self = other
        :rtype: eut.peerless.model.Constraint
        """
        return Constraint(self, Constraint.eq, other)

# Begin functions =============================================================

class _OneArgumentsFunction(Function):
    def __init__(self, x, tag):
        Function.__init__(self, x, tag=tag)
        self.x = self.arguments[0]

class _TwoArgumentsFunction(Function):
    def __init__(self, x, y, tag):
        Function.__init__(self, x, y, tag=tag)
        self.x = self.arguments[0]
        self.y = self.arguments[1]

class add(_TwoArgumentsFunction):
    def __init__(self, x, y):
        _TwoArgumentsFunction.__init__(self, x, y, tag="add")

    @property
    def is_linear(self):
        return self.x.is_linear and self.y.is_linear

    def __call__(self, solution):
        return self.x(solution) + self.y(solution)

    def __str__(self):
        return f"({self.x} + {self.y})"

class sub(_TwoArgumentsFunction):
    def __init__(self, x, y):
        _TwoArgumentsFunction.__init__(self, x, y, tag="sub")

    @property
    def is_linear(self):
        return self.x.is_linear and self.y.is_linear

    def __call__(self, solution):
        return self.x(solution) - self.y(solution)

    def __str__(self):
        return f"({self.x} - {self.y})"

class mul(_TwoArgumentsFunction):
    def __init__(self, x, y):
        _TwoArgumentsFunction.__init__(self, x, y, tag="mul")

    @property
    def is_linear(self):
        # One of the arguments is a number and the other is linear
        return ((isinstance(self.x, _Number) and self.y.is_linear) or
                (self.x.is_linear and isinstance(self.y, _Number)))

    def __call__(self, solution):
        return self.x(solution) * self.y(solution)

    def __str__(self):
        return f"({self.x} * {self.y})"

class truediv(_TwoArgumentsFunction):
    def __init__(self, x, y):
        _TwoArgumentsFunction.__init__(self, x, y, tag="div")

    @property
    def is_linear(self):
        return (self.x.is_linear and isinstance(self.y, _Number))

    def __call__(self, solution):
        return self.x(solution) / self.y(solution)

    def __str__(self):
        return f"({self.x} / {self.y})"

class pow(_TwoArgumentsFunction):
    def __init__(self, x, y):
        _TwoArgumentsFunction.__init__(self, x, y, tag="pow")

    def __call__(self, solution):
        return math.pow(self.x(solution),
                        self.y(solution))

    def __str__(self):
        return f"pow({self.x}, {self.y})"
ppow = pow
class abs(_OneArgumentsFunction):
    def __init__(self, x):
        _OneArgumentsFunction.__init__(self, x, tag="abs")

    def __call__(self, solution):
        return math.fabs(self.x(solution))

    def __str__(self):
        return f"abs({self.x})"

class remainder(_TwoArgumentsFunction):
    def __init__(self, x, y):
        _TwoArgumentsFunction.__init__(self, x, y, tag="mod")

    def __call__(self, solution):
        return math.remainder(self.x(solution), self.y(solution))

    def __str__(self):
        return f"remainder({self.x}, {self.y})"

class mod(_TwoArgumentsFunction):
    def __init__(self, x, y):
        """x % y"""
        _TwoArgumentsFunction.__init__(self, x, y, tag="modulo")

    def __call__(self, solution):
        return self.x(solution) % self.y(solution)

    def __str__(self):
        return f"{self.x} % {self.y}"

class sign(_TwoArgumentsFunction):
    def __init__(self, x, y):
        """
        copysign(x, y)
        """
        _TwoArgumentsFunction.__init__(self, x, y, tag="sign")

    def __call__(self, solution):
        return math.copysign(self.x(solution), self.y(solution))

    def __str__(self):
        return f"sign({self.x}, {self.y})"

bmin = min
class min(_TwoArgumentsFunction):
    def __init__(self, x, y):
        _TwoArgumentsFunction.__init__(self, x, y, tag="min")

    def __call__(self, solution):
        return bmin(self.x(solution), self.y(solution))

    def __str__(self):
        return f"min({self.x}, {self.y})"

bmax = max
class max(_TwoArgumentsFunction):
    def __init__(self, x, y):
        _TwoArgumentsFunction.__init__(self, x, y, tag="max")

    def __call__(self, solution):
        return bmax(self.x(solution), self.y(solution))

    def __str__(self):
        return f"max({self.x}, {self.y})"

class sin(_OneArgumentsFunction):
    def __init__(self, x):
        _OneArgumentsFunction.__init__(self, x, tag="sin")

    def __call__(self, solution):
        return math.sin(self.x(solution))

    def __str__(self):
        return f"sin({self.x})"

class cos(_OneArgumentsFunction):
    def __init__(self, x):
        _OneArgumentsFunction.__init__(self, x, tag="cos")

    def __call__(self, solution):
        return math.cos(self.x(solution))

    def __str__(self):
        return f"cos({self.x})"

class tan(_OneArgumentsFunction):
    def __init__(self, x):
        _OneArgumentsFunction.__init__(self, x, tag="tan")

    def __call__(self, solution):
        return math.tan(self.x(solution))

    def __str__(self):
        return f"tan({self.x})"

class sqrt(_OneArgumentsFunction):
    def __init__(self, x):
        _OneArgumentsFunction.__init__(self, x, tag="sqrt")

    def __call__(self, solution):
        return math.sqrt(self.x(solution))

    def __str__(self):
        return f"sqrt({self.x})"

class exp(_OneArgumentsFunction):
    def __init__(self, x):
        _OneArgumentsFunction.__init__(self, x, tag="exp")

    def __call__(self, solution):
        return math.exp(self.x(solution))

    def __str__(self):
        return f"exp({self.x})"

class log(_OneArgumentsFunction):
    def __init__(self, x):
        _OneArgumentsFunction.__init__(self, x, tag="log")

    def __call__(self, solution):
        return math.log(self.x(solution))

    def __str__(self):
        return f"log({self.x}, e)"

class round(_TwoArgumentsFunction):
    def __init__(self, x, y):
        """round(x, y)"""
        _TwoArgumentsFunction.__init__(self, x, y, tag="nint")

    def __call__(self, solution):
        return math.round(self.x(solution), self.y(solution))

    def __str__(self):
        return f"round({self.x}, {self.y})"

class ceil(_OneArgumentsFunction):
    def __init__(self, x):
        _OneArgumentsFunction.__init__(self, x, tag="ceiling")

    def __call__(self, solution):
        return math.ceil(self.x(solution))

    def __str__(self):
        return f"ceil({self.x})"

class floor(_OneArgumentsFunction):
    def __init__(self, x):
        _OneArgumentsFunction.__init__(self, x, tag="floor")

    def __call__(self, solution):
        return math.floor(self.x(solution))

    def __str__(self):
        return f"floor({self.x})"

# End functions ===============================================================

class Model(_NamedObject):
    """A model is the main class of the module and it is used to store
    the representation of the problem at hand.

    The structure is simple, it is a container that holds variables and,
    possibly, constraints and an objective function.

    Variables and the objective are added to the model at construction
    of these. Constraints, on the other hand, must be added to
    the model using the :func:`eut.peerless.model.Model.add_constraint`.
    """
    def __init__(self, name):
        """
        :param name: the name of the model
        """
        _NamedObject.__init__(self, name)
        self.__variables = {}
        self.__constraints = set()
        self.objective = None
        self._numbers = {}

    @property
    def is_linear(self):
        """
        :return: True if the objective and constraints of the model are linear
        """
        ans = all(ct.is_linear for ct in self.__constraints)
        if ans and self.objective is not None:
            ans = self.objective.is_linear
        return ans

    def _get_number(self, value):
        return self._numbers.setdefault(value, _Number(value))

    def serialize(self):
        info = {"class": _Serializable.get_class_name(self),
                "name": self.name,
                "variables": [v.serialize() for v in self.__variables.values()],
                "constraints": [ct.serialize() for ct in self.constraints],
                "objective": (None if self.objective is None else
                              self.objective.serialize())}
        return json.dumps(info)

    @classmethod
    def deserialize(cls, content):
        content = json.loads(content)
        ans = Model(content["name"])
        for var_content in content["variables"]:
            _Variable.deserialize(ans, var_content)
        for ct_content in content["constraints"]:
            ct = Constraint.deserialize(ans, ct_content)
            ans.add_constraint(ct)
        obj_content = content["objective"]
        if obj_content is not None:
            _Objective.deserialize(ans, obj_content)
        return ans

    def __str__(self):
        """Returns a representation of the model"""
        ans = f"Model: {self.name}\n"
        if self.objective is not None:
            ans += f"\n  {self.objective}\n"
        ans += "\n  subject to:\n"
        for ct in self.constraints:
            ans += f"   {ct}\n"
        ans += "\n  variables:\n"
        for v in sorted(self.__variables.values(), key=lambda v: v.name):
            ans +=  f"    {v.name} [{v.lb}, {v.ub}] {v.vtype}\n"
        return ans

    def _add_variable(self, variable):
        if variable.name is None:
            variable.name = f"x_{len(self.__variables)}"
        variable.index = len(self.__variables) + 1
        self.__variables[variable.name] = variable

    def _remove_variable(self, variable):
        self.__variables.pop(variable.name)

    def get_variable(self, name):
        """
        :return: the variable of that name
        """
        return self.__variables.get(name)

    @property
    def variables(self):
        """
        :return: a list of variables sorted by name
        """
        return sorted(self.__variables.values(), key=lambda v: v.name)

    @property
    def constraints(self):
        """
        :return: a list of constraints sorted by name
        """
        return sorted(self.__constraints, key=lambda ct: ct.name)

    def add_constraint(self, constraint, name=None):
        """
        Adds constraint to the model. If name is not None, it is assigned
        to the constraint. If name is None and the constraint's name
        is also None, the constraint is assigned a generic name
        of the form ct_n where n is the number of constraints in the model.

        :param constraint: the constraint to add to the model
        :param name: the name to assign to the constraint if the constraint's
                     name is None
        """
        if name is not None:
            constraint.name = name
        if constraint.name is None:
            constraint.name = f"ct_{len(self.__constraints)}"
        self.__constraints.add(constraint)

    def _set_objective(self, objective):
        self.objective = objective

    def cts_residual(self, solution):
        """
        Evaluates and returns the residual of the model, that is,
        :math:`\sum_{ct} ct(solution)`. Notice that constraints always return
        a positive number.

        :param eut.peerless.model.Solution solution: the solution to evaluate
               the residual on
        """
        ans = 0
        # Add the residuals of the constraints
        for ct in self.constraints:
            ans += ct(solution)
        return ans

    def bounds_residual(self, solution):
        """
        Evaluates and returns the residual of the variables' bounds,
        that is,
        :math:`\sum_{v} (v_{lb} - solution(v))^+ + (solution(v) - v_{ub})^+`

        :param eut.peerless.model.Solution solution: the solution to evaluate
               the residual on
        """
        # Add the bounds residuals
        ans = 0
        for variable in self.variables:
            value = variable(solution)
            if variable.lb is not None:
                # lb <= value <=> lb - value <= 0 <=> res = max(0, lb - value)
                ans += bmax(0, variable.lb - value)
            if variable.ub is not None:
                # value <= ub <=> value - ub <= 0 <=> res = max(0, value - ub)
                ans += bmax(0, value - variable.ub)
        return ans

    def __call__(self, solution):
        """
        Evaluates the model at the solution

        :param eut.peerless.model.Solution solution: the solution to evaluate
               the residual on
        :return: the objective, residual and bound residual of the model at
                 solution
        :rtype: eut.peerless.model.ModelMeasures
        """
        objective = None if self.objective is None else self.objective(solution)
        cts_residual = self.cts_residual(solution)
        bounds_residual = self.bounds_residual(solution)
        return ModelMeasures(objective, cts_residual, bounds_residual)

ModelMeasures = collections.namedtuple("ModelMeasures",
                                       ["objective", "cts_residual",
                                        "bounds_residual"])
"""A namedtuple holding the objective, constraint residual and bound residual"""

class _Variable(_NamedObject, Function):

    continuous = "continous"
    integer = "integer"
    binary = "binary"

    def __init__(self, model, name, lb=None, ub=None, vtype=continuous):
        _NamedObject.__init__(self, name)
        Function.__init__(self, tag="variable")
        self.lb = lb
        self.ub = ub
        self.vtype = vtype
        self.index = None
        self.model = model
        self.model._add_variable(self)

    @property
    def is_linear(self):
        return True

    def _set_name(self, value):
        index = self.index
        self.model._remove_variable(self)
        self._name = value
        self.model._add_variable(self)
        self.index = index

    def __str__(self):
        return f"{self.name}"

    def __call__(self, solution):
        return solution[self]

    def serialize(self):
        return {"class": _Serializable.get_class_name(self),
                "name": self.name, "lb": self.lb, "ub": self.ub,
                "vtype": self.vtype, "index": self.index}

    @classmethod
    def deserialize(cls, model, content):
        name = content["name"]
        ans = model.get_variable(name)
        if ans is None:
            ans = _Variable(model, name, content["lb"], content["ub"],
                            content["vtype"])
            ans.index = content["index"]
        return ans

def Variable(model, name, lb=None, ub=None):
    """
    Represents a variable in the model.

    * Even thought it isn't required to define lower and upper bounds
      on a variable, the algorithms will perform better the thighter
      the bounds of the variables are.
    * Variables can be continuous, integer and binary.
    * Variables are added to the model at construction time
    * A variable is a :class:`eut.peerless.model.Function` that evaluates
      to the value at the given solution.

    To create a continuous variable use this class without specifying

    :param model: the model to which the variable will be added
    :param name: the name of the variable
    :param lb: lower bound
    :param ub: upper bound
    """
    return _Variable(model, name, lb, ub, _Variable.continuous)

def IntegerVariable(model, name, lb=None, ub=None):
    """
    Represents an integer variable. See :func:`eut.peerless.model.Variable`
    for more information.
    """
    return _Variable(model, name, lb, ub, _Variable.integer)

def BinaryVariable(model, name):
    """
    Represents a binary variable. See :func:`eut.peerless.model.Variable`
    for more information.
    """
    return _Variable(model, name, 0, 1, _Variable.binary)

class Constraint(_NamedObject, _Serializable):
    """
    A constraint represent a relation between variables that must
    be satisfied by the solutions. Constraints are generally created
    usign the overriden operators of :class:`eut.peerless.model.Function`,
    <=, >=, ==. Constraints can also be created directly using the
    constructor of the class.

    Constraints must be added to the model using
    :func:`eut.peerless.model.Model.add_constraint`.
    """

    le = "<="
    """Less or equal constraint tag"""
    ge = ">="
    """Greater or equal constraint tag"""
    eq = "="
    """Equal constraint tag"""

    def __init__(self, lhs, sense, rhs, name=None):
        """
        Creates the constraint: lhs sense rhs

        :param lhs: a function or number
        :param sense: one of :attr:`eut.peerless.model.Constraint.le`,
                      :attr:`eut.peerless.model.Constraint.ge` or
                      :attr:`eut.peerless.model.Constraint.eq`
        :param rhs: a function or number
        :param name: the name of the constraint
        """
        _NamedObject.__init__(self, name)
        _Serializable.__init__(self)
        self.model = None
        self.lhs = _Number(lhs) if isinstance(lhs, numbers.Number) else lhs
        self.sense = sense
        self.rhs = _Number(rhs) if isinstance(rhs, numbers.Number) else rhs

    @property
    def is_linear(self):
        """
        :return: True if lhs and rhs are linear
        """
        return self.lhs.is_linear and self.rhs.is_linear

    def serialize(self):
        return {"class": _Serializable.get_class_name(self),
                "name": self.name,
                "lhs": self.lhs.serialize(), "sense": self.sense,
                "rhs": self.rhs.serialize()}

    @classmethod
    def deserialize(cls, model, content):
        lhs = Function.deserialize(model, content["lhs"])
        rhs = Function.deserialize(model, content["rhs"])
        name = content["name"]
        ct = Constraint(lhs, content["sense"], rhs, name)
        model.add_constraint(ct)
        return ct

    def __call__(self, solution):
        """
        Evaluates the constraint according to the sense:
        * eq: abs(ct(solution))
        * le: max(0, lhs(solution) - rhs(solution))
        * ge: -min(0, lhs(solution), rhs(solution))

        :param eut.peerless.model.Solution solution: a solution
        """
        if self.sense == Constraint.le:
            # lhs <= rhs <=> lhs - rhs <= 0 <=> res = max(0, lhs - rhs)
            return bmax(0, self.lhs(solution) - self.rhs(solution))
        elif self.sense == Constraint.ge:
            # lhs >= rhs <=> lhs - rhs >= 0 <=> res = -min(0, lhs - rhs)
            return -bmin(0, self.lhs(solution) - self.rhs(solution))
        elif self.sense == Constraint.eq:
            return math.fabs(self.lhs(solution) - self.rhs(solution))
        raise ValueError(f"Unknown operator {self.sense}")

    def __str__(self):
        return f"{self.name}: {self.lhs} {self.sense} {self.rhs}"

class _Objective(_NamedObject, _Serializable):

    minimize = "minimize"
    maximize = "maximize"

    def __init__(self, model, name, sense, function):
        _NamedObject.__init__(self, name)
        _Serializable.__init__(self)
        self.sense = sense
        self.function = function
        self.model = model
        self.model._set_objective(self)

    @property
    def is_linear(self):
        return self.function.is_linear

    def __call__(self, solution):
        return self.function(solution)

    def serialize(self):
        return {"class": _Serializable.get_class_name(self),
                "name": self.name, "sense": self.sense,
                "function": self.function.serialize()}

    @classmethod
    def deserialize(cls, model, content):
        obj = _Objective(model, content["name"], content["sense"],
                         Function.deserialize(model, content["function"]))
        return obj

    def __str__(self):
        return f"{self.sense} {self.name} {self.function}"

def Maximize(model, name, function):
    """
    Creates a maximization objective function and set it in the model

    :param model: the model to set objective to
    :param name: the name of the objective
    :param function: the function representing the objective
    :return: a callable receiving a solution as argument
    """
    return _Objective(model, name, _Objective.maximize, function)

def Minimize(model, name, function):
    """
    Creates a minimization objective function and set it in the model.
    See :func:`eut.peerless.model.Maximize`.
    """
    return _Objective(model, name, _Objective.minimize, function)

class Solution(_Serializable):
    """A solution is a class emulating a container used
    to set and get the value of variables in the solution."""
    def __init__(self):
        self.values = {}
        self.variables = {}

    def __setitem__(self, variable, value):
        """Allows the following: solution[variable] = value"""
        self.variables[variable.index] = variable
        self.values[variable.index] = value

    def __getitem__(self, variable):
        """Allows the following: solution[variable]"""
        return self.values.get(variable.index, 0)

    def items(self):
        """Returns a list of pairs (variable, value)"""
        ans = []
        for index, value in self.values.items():
            ans.append((self.variables[index], value))
        return ans

    def __str__(self):
        ans = "{"
        ans += ", ".join(f"{var.name}: {self.values[idx]}"
                         for idx, var in sorted(self.variables.items()))
        ans += "}"
        return ans

    def serialize(self):
        return {"values": {str(i[0]): i[1] for i in self.values.items()}}

    @classmethod
    def deserialize(cls, model, content):
        ans = Solution()
        variables = {}
        for variable in model.variables:
            variables[variable.index] = variable
        for index, value in content["values"].items():
            index = int(index)
            ans.values[index] = value
            ans.variables[index] = variables[index]
        return ans

class Parameters(_Serializable):
    """
    Class to specify the parameters used by the solver.
    """
    def __init__(self, max_seconds=3600, objective_goal=None):
        """
        :param max_seconds: stop the solve process after max_seconds.
                            The current best solution is returned if available.
        :param objective_goal: stop the solve process if found a feasible
                               solution with an objective less or equals to
                               this value.
        """
        self.max_seconds = max_seconds
        self.objective_goal = objective_goal

    def serialize(self):
        return json.dumps({"max_seconds": self.max_seconds,
                           "objective_goal": self.objective_goal})

    @classmethod
    def deserialize(cls, content):
        content = json.loads(content)
        ans = Parameters()
        ans.max_seconds = content["max_seconds"]
        ans.objective_goal = content["objective_goal"]
        return ans
