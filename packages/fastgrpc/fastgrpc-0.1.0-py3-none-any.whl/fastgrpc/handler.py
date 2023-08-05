# coding:utf8
from abc import ABC, abstractmethod
from fastgrpc.typedef import *

class RegistryHandler(type):
    REGISTRY = []

    def __new__(cls, name, bases, attrs):
        """
        在添加handler类过程中就把排序工作好
        :param name:
        :param bases:
        :param attrs:
        :return:
        """
        new_cls = type.__new__(cls, name, bases, attrs)
        lastHandler = cls.REGISTRY[-1:]
        if lastHandler and lastHandler[0][1] > new_cls.order:
            cls.REGISTRY.insert(-1, (new_cls, new_cls.order))
        else:
            cls.REGISTRY.append((new_cls, new_cls.order))
        return new_cls


class Handler(metaclass=RegistryHandler):
    order = 0
    options = []

    def __init__(self, reverse: Optional[bool] = False):
        """
        是否将过滤器顺序反向
        需要将列表中的每一个过滤器类都连起来，同时也要将一些过滤器函数添加到Handler中，以便运行之用
        :param reverse:
        """
        if reverse:
            self.__class__.REGISTRY.reverse()
        for idx, handler in enumerate(dict(self.__class__.REGISTRY)):
            handler.next_handler = self.__class__.REGISTRY[idx + 1][0] if idx < (
                    len(self.__class__.REGISTRY) - 1) else None

    def pipeline(self, *args, **kwargs) -> None:
        """Pipeline 请求满足要求就进行加工,然后传递给下一个pipeline"""
        [option(*args, **kwargs) for option in self.options] if isinstance(self, Handler) else [
            self.option(self, *args, **kwargs)]
        if self.next_handler:
            self.next_handler.pipeline(self.next_handler, *args, **kwargs)

    def filter(self, *args, **kwargs) -> None:
        """过滤器  如果结果返回True,则表示过滤成功,继续校验其他过滤,全为True时,放行"""
        filterRes = [option(*args, **kwargs) for option in self.options] if isinstance(self, Handler) else [
            self.option(self, *args, **kwargs)]
        if all(filterRes) and self.next_handler:
            self.next_handler.filter(self.next_handler, *args, **kwargs)

    def interceptor(self, *args, **kwargs) -> None:
        """拦截器  如果结果有返回True,则表示需要拦截,全为False才放行"""
        print(self.options)
        interceptRes = [option(*args, **kwargs) for option in self.options] if isinstance(self, Handler) else [
            self.option(self, *args, **kwargs)]

        print(self,self.next_handler,self.next_handler.interceptor)
        if not any(interceptRes) and self.next_handler:
            self.next_handler.interceptor(self.next_handler, *args, **kwargs)

    def option(self, *args, **kwargs) -> Optional[bool]:
        return True

    @classmethod
    def add_option(cls, func):
        cls.options.append(func)

    @classmethod
    def add_handler(cls, new_handler):
        print(new_handler)
        new_handler_order = new_handler.__dict__.get('order', 0)
        print(new_handler_order)
        lastHandler = cls.REGISTRY[-1:]
        if lastHandler and lastHandler[0][1] > new_handler_order:
            cls.REGISTRY.insert(-1, (new_handler, new_handler_order))
        else:
            cls.REGISTRY.append((new_handler, new_handler_order))
        new_handler.interceptor=cls.interceptor
        new_handler.filter=cls.filter
        new_handler.pipeline=cls.pipeline
        print(cls.REGISTRY)
        return new_handler
