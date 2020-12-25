import abc


class Device(abc.ABC):

    @abc.abstractmethod
    def login_host(self):
        pass

    @abc.abstractmethod
    def logout_host(self):
        pass

    @abc.abstractmethod
    def execute_command(self, command):
        pass
