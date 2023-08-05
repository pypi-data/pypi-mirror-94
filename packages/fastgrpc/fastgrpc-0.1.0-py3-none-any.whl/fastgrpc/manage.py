from fastgrpc.typedef import *
from functools import wraps


class ManageMetaClass(type):
    def __new__(cls, name, bases, attrs):
        attrs['__sourceList__'] = []
        attrs['__sourceMap__'] = {}
        return type.__new__(cls, name, bases, attrs)


class Manager(object, metaclass=ManageMetaClass):

    @classmethod
    def add(cls, source):
        if cls.find(source) == None:
            cls.__sourceList__.append(source)

    def delete(cls, source):
        cls.__sourceList__.remove(source)

    def update(cls, source, relationObj):
        cls.__sourceMap__.update(source, relationObj)

    @classmethod
    def find(cls, source):
        for i in cls.__sourceList__:
            if i == source:
                return source
        return None

    @classmethod
    def set(cls, key, value):
        cls.__sourceMap__[key] = value

    @classmethod
    def get(cls, key):
        return cls.__sourceMap__[key]


class ApiFuncManage(Manager):
    def add_api(self,
                func: ApiFunc,
                servicerApi: ServicerApi,
                request: ServicerApiReq,
                response: ServicerApiRes):
        assert isinstance(servicerApi, FunctionType) and servicerApi.__qualname__.__contains__('.')
        assert (request.__class__.__name__) == "GeneratedProtocolMessageType"
        assert (response.__class__.__name__) == "GeneratedProtocolMessageType"


        [servicerApiQual, servicerApiName] = servicerApi.__qualname__.split('.') if len(
            servicerApi.__qualname__.split('.')) == 2 else servicerApi.__qualname__.split('.')[:-2]
        servicer = getattr(__import__(servicerApi.__module__), servicerApiQual)
        servicer_api = [getattr(servicer, i) for i in dir(servicer) if isinstance(getattr(servicer, i), FunctionType)]

        ServicerManage.add(servicer)
        ServicerManage.set(servicer, __import__(servicer.__module__))

        requestFields = [i for i in request.DESCRIPTOR.fields_by_name]
        responseFields = [i for i in response.DESCRIPTOR.fields_by_name]

        servicerApiVars = ','.join([i for i in servicerApi.__code__.co_varnames])
        servicerApiName = servicerApi.__name__  # 通过__name__获取方法名
        servicerImplName = servicer.__name__ + 'Impl'  # 构造实现类的类名

        ServicerApiReqManage.add(request)
        ServicerApiReqManage.set(servicerApiName,request)
        messageFieldsManage.set(request, requestFields)
        ServicerApiResManage.add(response)
        ServicerApiResManage.set(servicerApiName,response)
        messageFieldsManage.set(response,responseFields)


        if not hasattr(__import__(servicerApi.__module__), servicerImplName):
            _impl = type(servicerImplName, (servicer,), {})  # 手动生成一个不完善的类
            _impl.__module__ = servicerApi.__module__  # 修改这个类对象的__module__
            setattr(__import__(servicerApi.__module__), servicerImplName, _impl)  # 将这个类对象注入到api所在的module中去

            ServicerImplManage.add(servicerImplName)

        servicerImpl = getattr(__import__(servicerApi.__module__), servicerImplName)
        print("构造实现类对象", servicerImpl,ApiFuncManage.__module__)
        print(getattr(__import__('fastgrpc.manage'), 'ServicerApiReqManage'))

        """解析得到函数co"""
        servicerApiCO = compile(f"""
def {servicerApiName}({servicerApiVars}):
    print("生成的接口内部")
    # print('define',__name__,request.__module__ )
    print('RPC_req',getattr( __import__('fastgrpc.manage') , 'ServicerApiReqManage' ) )
    print('RPC_req',getattr( __import__('fastgrpc.manage') , 'ServicerApiReqManage' ).get('{servicerApiName}') )
    print('RPC_res',getattr( __import__('fastgrpc.manage') , 'ServicerApiResManage' ) )
    print('RPC_res',getattr( __import__('fastgrpc.manage') , 'ServicerApiResManage' ).get('{servicerApiName}') )
    res_class = getattr( __import__('fastgrpc.manage') , 'ServicerApiResManage' ).get('{servicerApiName}')
    print('RPC_func',getattr( __import__('fastgrpc.manage') , 'ServicerApiImplManage' ) )
    print('RPC_func',getattr( __import__('fastgrpc.manage') , 'ServicerApiImplManage' ).get('{servicerApiName}') )
    di_function = getattr(__import__('fastgrpc.manage') , 'ServicerApiImplManage' ).get('{servicerApiName}')
    print('func_param',dict( [(f[0].name, f[1]) for f in request.ListFields()] ) )

    print('res_params',getattr( __import__('fastgrpc.manage') , 'messageFieldsManage' ).get(res_class) )
    res_params = getattr( __import__('fastgrpc.manage') , 'messageFieldsManage' ).get(res_class)
    # print('res_params', ','.join( [i.name for i in getattr(__import__(request.__module__),request.DESCRIPTOR.name[:-3]+'Res').DESCRIPTOR.fields] ) )

    print('func_res',getattr( __import__('fastgrpc.manage') , 'ServicerApiImplManage' ).get('{servicerApiName}')( **dict( [(f[0].name, f[1]) for f in request.ListFields()] )  )  )
    func_res=getattr( __import__('fastgrpc.manage') , 'ServicerApiImplManage' ).get('{servicerApiName}')( **dict( [(f[0].name, f[1]) for f in request.ListFields()] )  ) 

    if not isinstance(func_res,tuple):
        func_res = (func_res,)

    return res_class (**dict( [rt for rt in zip( res_params,  func_res) ] ) )
""", "<string>", "exec")
        servicerApiImpl = FunctionType(servicerApiCO.co_consts[0], globals(), servicerApiName)  # 通过co构造函数对象
        ServicerImplManage.set(servicerImplName, servicerImpl)
        print("实现接口构造完毕")

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                print('包装函数内部', func, args, kwargs)
                res = func(*args, **kwargs)
                print('包装函数内部', res)
                return res
            except Exception as e:
                print('Error execute: %s' % func.__name__)

                print(type(e))
                print('wrapper', e)
            # return res

        print("准备将函数注入到实现类对象中:")
        setattr(servicerImpl, servicerApiName, servicerApiImpl)  # 将这个函数对象注入到类对象中
        ServicerApiImplManage.add(wrapper)
        ServicerApiImplManage.set(servicerApiName,wrapper)

        setattr(__import__(request.__module__), servicerApiName + '_' + request.__name__ + '_func',
                wrapper)  # 将这个函数对象注入到类对象中
        # print("函数注入到实现类对象完毕", request.__module__, servicerApiImpl + '_' + request.__name__ + '_func')
        print("函数注入到实现类对象完毕", servicerImpl.__dict__)
        print("*" * 20)

        return wrapper

    pass


class ServicerManage(Manager):
    pass


class ServicerImplManage(Manager):
    pass


class ServicerApiManage(Manager):
    pass


class ServicerApiImplManage(Manager):
    pass


class ServicerApiReqManage(Manager):
    pass


class ServicerApiResManage(Manager):
    pass

class messageFieldsManage(Manager):
    pass
