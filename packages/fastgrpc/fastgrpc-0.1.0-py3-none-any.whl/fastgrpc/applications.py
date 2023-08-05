from fastgrpc.manage import *
from fastgrpc.typedef import *
from fastgrpc.handler import Handler
class FastgRPC(object):
    def __init__(
            self,
            debug: bool = False,
            logOptions=None,
            openApiOptions=None,
            grpcOptions=None,
    ) -> None:
        self.debug = debug

        self.apiFuncManager: ApiFuncManage = ApiFuncManage()

        self.servicerManager: ServicerManage = ServicerManage()

        self.servicerImplManager: ServicerImplManage = ServicerImplManage()

        self.servicerApiManager: ServicerApiManage = ServicerApiManage()

        self.servicerApiImplManager: ServicerApiImplManage = ServicerApiImplManage()

        self.servicerApiReqManager: ServicerApiReqManage = ServicerApiReqManage()

        self.servicerApiResManager: ServicerApiResManage = ServicerApiResManage()

        self.handler = Handler
        self.dependencies_dict = {}

    def add_api(
            self,
            func,
            servicerApi,
            request,
            response
    ) -> None:
        self.apiFuncManager.add_api(
            func,
            servicerApi,
            request,
            response
        )

    def api(
            self,
            servicerApi,
            request,
            response=None
    ) -> Callable[[Decorated], Decorated]:
        def decorator(func: Decorated) -> Decorated:
            self.apiFuncManager.add_api(
                func,
                servicerApi,
                request,
                response
            )
            return func

        return decorator

    def handlerOption(self):
        def decorator(func: Decorated) -> Decorated:
            self.handler.add_option(func)

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def interceptor(self):
        def decorator(cls):
            print(cls)
            self.handler.add_handler(cls)
            print(self.handler.REGISTRY)
            # @wraps(func)
            # def wrapper(*args, **kwargs):
            #     return func(*args, **kwargs)
            # return wrapper

        return decorator

    def dependencies(self, key: str, object: object):
        def decorator(func):
            dependencies_dict = self.dependencies_dict

            @wraps(func)
            def wrapper(*args, **kwargs):
                dependencies_dict[key] = object
                __builtins__['__DI__'] = key
                res = func(*args, **kwargs)
                del dependencies_dict[key]
                del __builtins__['__DI__']
                return res

            return wrapper

        return decorator

    def DI(self, key=None):
        try:
            return self.dependencies_dict[__DI__] if not key else self.dependencies_dict[key]
        except NameError as e:
            import warnings
            warnings.warn("\nMust Decorator Function Use: `@fastgrpc.di(object)`, First!",stacklevel=2)

    def __call__(self, port=50051,alts=True,max_workers=10,thread_name_prefix='') -> None:
        import grpc
        from concurrent import futures
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers,thread_name_prefix=thread_name_prefix))
        if alts:
            pass
            # server_creds = grpc.alts_server_credentials()
            # server.add_secure_port(server_address, server_creds)
        try:
            try:
                for servicer in self.servicerManager.__sourceList__:
                    add_to_server=self.servicerManager.get(servicer).__dict__[f'add_{servicer.__name__}_to_server']
                    add_to_server(self.servicerImplManager.__sourceMap__[f'{servicer.__name__}Impl'](),server)
                    print(add_to_server,self.servicerImplManager.__sourceMap__[f'{servicer.__name__}Impl'](),server)
                server.add_insecure_port(f'[::]:{port}')
                server.start()
                print("启动rpc服务成功")
                server.wait_for_termination()
            except Exception as e:
                print(e)
        except KeyboardInterrupt:
            print("开始停止rpc服务")
            server.stop(0)

    def setup(self):
        pass
