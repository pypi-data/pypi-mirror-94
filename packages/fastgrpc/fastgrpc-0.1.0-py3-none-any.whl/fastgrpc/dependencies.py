from fastgrpc.typedef import *
class RegistryDependencies(type):
    REGISTRY = []

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        cls.REGISTRY.append(new_cls)
        return new_cls


class Dependencies(metaclass=RegistryDependencies):
    dependencies = {}
    @classmethod
    def add_dependencies(cls, new_dependencies):
        cls.dependencies[new_dependencies.__name__] = new_dependencies

    def __call__(self, cls):
        print('call',cls)
        Dependencies.add_dependencies(cls)
