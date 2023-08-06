from abc import ABC, abstractmethod


class AbstractTask(ABC):
    @abstractmethod
    def run(self) -> None:
        pass


class Task(AbstractTask):
    def run(self) -> None:
        print('hello world')
