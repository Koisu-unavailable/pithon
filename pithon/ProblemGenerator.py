import abc
import io
class ProblemGenerator(abc.ABC):
    @abc.abstractmethod
    def generate_problem(self) -> str:
        pass
    