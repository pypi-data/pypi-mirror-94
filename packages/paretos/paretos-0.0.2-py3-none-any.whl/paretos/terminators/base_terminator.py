import abc

from paretos.objects.progress import Progress


class BaseTerminator(metaclass=abc.ABCMeta):
    """Interface to describe Environments"""

    def should_terminate(self, progress: Progress) -> bool:
        """
        Interface method to guarantee that child classes implement this. Should be true
        when termination is desired
        :param progress: Progress to check whether termination should happen
        """
        raise NotImplementedError
