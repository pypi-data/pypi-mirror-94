# Peerless Optimizer

Developed by Eve Utils

[www.eveutils.com](http://www.eveutils.com)

Peerless is a software that implements an optimization algorithm to solve
the following type of problems

  min f(x);
  subject to g(x) >= 0,
             h(x) >= 0,
             lb <= x <= ub

where:
 - x is an element in R^n where some x_i in N (some or all can be integers)
 - lb, ub in R^n with lb_i <= ub_i forall i in 1,...,n
 - g : R^n -> R^m is a function that can be nonlinear, non-differentiable
                  or discontinuous
 - h : R^n -> R^p is a function that can also be nonlinear, non-differentiable
                  or discontinuous

## Documentation

The documentation can be found at [https://docs.eveutils.com/peerless/index.html](https://docs.eveutils.com/peerless/index.html).

## Main features

 - Nonlinear, non-differentiable, discontinuous.
   The functions f, g and h can be of any type as long as they return similar
   values when evaluated are the same point different times (more about this
   later).
 - Discrete.
   Some or all the variables can be restricted to take integer values.
 - Global.
   Problems can have many local and global optima.
 - Stochastic.
   Function evaluations can be the result of a process using one or many
   probability distributions.
 - Scenarios.
   A Stochastic problem can be specified by scenarios
 - Parallel and distributed.
   Peerless can be executed in parallel or distributed mode
