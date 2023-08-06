import collections

class Statuses:
    """Possible job statuses"""

    created = "created"
    """The job was created and is waiting for a worker to start processing it"""

    acquired = "acquired"
    """The job was acquired by a worker"""

    processing = "processing"
    """The job is beign processed by a worker"""

    partial = "partial"
    """Status associated to a partial solution"""

    optimum = "optimum"
    """Indicates that a solution is optimal"""

    infeasible = "infeasible"
    """Indicates that a solution in infeasible"""

    failure = "failure"
    """Status used when an error ocurrs"""

    executed = "executed"
    """This status is used when a job has been processed"""

    # Final statuses. Jobs stop after one of these statuses is reached
    finals = (optimum, infeasible, failure, executed)
    """List of possible final statuses of a job"""

class StatusStamp:
    """A status stamp"""
    def __init__(self, date, status, message):
        """
        :param date: datetime.datetime of the stamp
        :param status: one of the attributes of
                       :py:class:`eut.abba.processor.statuses.Statuses`
        :param message: the message associated to the stamp
        """
        self.date = date
        self.status = status
        self.message = message

    def __str__(self):
        return f"[{self.date}|{self.status}] {self.message}"

class PartialSolution:
    """A partial solution"""
    def __init__(self, date, result):
        """
        :param date: datetime.datetime when the partial solution was created
        :param result: the result,
               see :py:meth:`eut.abba.processor.jobstore.JobStore.get_result`
        """
        self.date = date
        self.result = result
