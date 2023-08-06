from ..objects.progress import Progress
from .base_terminator import BaseTerminator


class RunTerminator(BaseTerminator):
    def __init__(self, n_runs):
        super().__init__()
        self.n_runs = n_runs

    def should_terminate(self, progress: Progress) -> bool:
        if self.n_runs < progress.get_nr_of_evaluations():
            return True

        return False
