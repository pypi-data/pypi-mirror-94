import collections
import logging
import time
import xmlrpc.client

import eut.abba.processor.statuses
import eut.abba.processor.priority
import eut.peerless
import eut.peerless.model

logger = logging.getLogger(__name__)

class OptimizationResult:
    """This is the object returned by :func:`eut.peerless.solver.solve`.
    It has the following attributes:

    * **solution**: an instance of :class:`eut.peerless.model.Solution`
    * **statuses**: a list of the statuses
      (:class:`eut.abba.processor.statuses.StatusStamp`) the solve process went through.
    * **log**: the output of the solve process
    """
    def __init__(self, solution=None, statuses=[], log=""):
        self.solution = solution
        self.statuses = statuses
        self.log = log

class _Solver:
    def __init__(self, model, parameters):
        self.model = model
        self.parameters = parameters

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def solve(self, environment):
        """Returns (result, statuses)"""
        ans = OptimizationResult()
        with xmlrpc.client.ServerProxy(environment.jobstore,
                                       allow_none=True) as processor:
            logger.info("Sending problem to the jobstore")
            # Send the serialized model to the server and wait for the result
            job = processor.submit(environment.username, environment.password,
                                   self.model.serialize(),
                                   self.parameters.serialize(),
                                   environment.priority)
            logger.info(f"..job's key is {job}")
            # Get the statuses and stop when the last one indicates
            # that the job processing is done
            logger.info(f"..pooling every {environment.pooling_gap} seconds")
            previous_status = None
            # TBD: Add a timeout in the parameters
            statuses = []
            while True:
                statuses = processor.get_statuses(environment.username,
                                                  environment.password, job)
                StatusStamp = eut.abba.processor.statuses.StatusStamp
                statuses = [StatusStamp(**s) for s in statuses]
                last_status = statuses[-1]
                if ((not environment.only_log_status_changes) or
                    previous_status is None or
                    last_status.date != previous_status.date):
                    msg = "..|{}|{}|{}: '{}'"
                    logger.info(msg.format(job, last_status.date,
                                           last_status.status,
                                           last_status.message))
                    previous_status = last_status
                # Check if the status is a final one
                if (last_status.status in
                    eut.abba.processor.statuses.Statuses.finals):
                    break
                # Wait to pool again
                time.sleep(environment.pooling_gap)
            # Build the solution
            solution, log = self._build_solution(processor, job, environment)
            # Answer
            ans = OptimizationResult(solution, statuses, log)
        # Return
        return ans

    def _build_solution(self, processor, job, environment):
        result, log = processor.get_result(environment.username,
                                           environment.password, job)
        solution = eut.peerless.model.Solution.deserialize(self.model, result)
        return solution, log

class Environment:
    """
    An environment is used to define the way the client will interact with
    the solve service.
    """
    def __init__(self, username, password, *,
                 jobstore=eut.peerless.default_jobstore_url,
                 pooling_gap=2, only_log_status_changes=True,
                 priority=eut.abba.processor.priority.Priority.low):
        """
        :param username: a username authorize to send jobs
        :param password: the password
        :param jobstore: the url of the jobstore
        :param pooling_gap: nb. seconds between requests for job status
        :param only_log_status_changes: if True, only status changes will
                                        be logged, else, show a log every
                                        time the server is poolled.
        :param priority: the priority of the job. A positive number.
                         The lower the value the higher the priority.
                         It is overriden by the priority specified in
                         the user, if any.
        """
        self.jobstore = jobstore
        self.username = username
        self.password = password
        # Number of seconds between server poolings
        self.pooling_gap = pooling_gap
        self.only_log_status_changes = only_log_status_changes
        self.priority = priority

def solve(model, parameters, environment):
    """
    Sends the model and parameters to the jobstore specified in the
    environment.

    :param eut.peerless.model.Model model: the model to be solved
    :param eut.peerless.model.Parameters parameters: the solver parameters
    :param eut.peerless.solver.Environment environment: jobstore, username,
           password and server interaction configuration.
    :return: the best solution found by the solver
    :rtype: eut.peerless.solver.OptimizationResult
    """
    ans = OptimizationResult()
    with _Solver(model, parameters) as slv:
        ans = slv.solve(environment)
    return ans
