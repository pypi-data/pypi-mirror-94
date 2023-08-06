""" Common exceptions that may occur. """


class AioTaskError(Exception):
    """ Base exception. """


class TaskNotFound(AioTaskError):
    """ Requested task id was not found. Task TTL may have expired. """


class TaskNotRegistered(AioTaskError):
    """ Task was not registered by any worker. """


class TaskAlreadyRegistered(AioTaskError):
    """ Task was not registered by any worker. """
