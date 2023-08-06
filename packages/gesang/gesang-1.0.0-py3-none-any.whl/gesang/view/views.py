from gesang.utils import exc
from gesang.validator.base import Path, Query, Body, Form
from starlette.responses import JSONResponse, HTMLResponse
from gesang.utils import wraps
import json


class RestResponse:

    def __init__(self, code, message, data=None):
        self.__code = code
        self.__message = message
        self.__data = data

    @property
    def code(self):
        return self.__code

    @property
    def message(self):
        return self.__message

    @property
    def data(self):
        return self.__data

    def to_json(self):
        return {
            "code": self.__code,
            "message": self.__message,
            "data": self.__data
        }


class View:
    allow_methods = ["GET", "POST", "PUT", "DELETE", "HEAD"]

    def __init__(self, **kwargs):
        self._request = kwargs.pop("request")

    @wraps.view_error_wrap
    async def dispatch_method(self, request, *args, **kwargs):
        """
        分发调用方法，获取request.method中对应的方法，进行调用

        :param request: [starlette.Requests]  starlette 请求体对象
        :param args: [list] 列表参数
        :param kwargs: [dict] 字典参数
        :raise MethodNotAllowed: 方法没有找到，请求方法在View视图类中没有没有被定义
        :raise ValidationError: 参数校验失败
        :raise Exception: 其他未知异常
        :return: [object] 返回值
        """
        if request.method.upper() in self.allow_methods:
            handler = getattr(self, request.method.lower())
        else:
            raise exc.MethodNotAllowed("Method not Allowed.")
        params_dict = await self._do_validate(annotations=handler.__annotations__)
        kwargs.update(params_dict)
        resp = await handler(request, *args, **kwargs)
        if isinstance(resp, RestResponse):
            return JSONResponse(content=resp.to_json())
        elif isinstance(resp, HTMLResponse):
            return resp
        else:
            return HTMLResponse(content=resp)

    @property
    async def form_data(self):
        """
        获取FORM数据
        :return:
        """
        return await self._request.form()

    @property
    async def query_data(self):
        """
        获取QUERY请求数据
        :return:
        """
        return self._request.query_params

    @property
    async def path_data(self):
        """
        获取请求路由参数
        :return:
        """
        return self._request.path_params

    @property
    async def body_data(self):
        """
        获取请求BODY数据
        :return:
        """
        body = await self._request.body()
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {}

    async def _do_validate(self, annotations):
        """
        方法中校验参数

        :param annotations: [dict] 方法中自定义参数校验字典
        :return:
        """
        annotations_var_dict = {}
        for var_name, annotation_cls in annotations.items():
            if issubclass(annotation_cls, Path):
                params = await self.path_data
            elif issubclass(annotation_cls, Query):
                params = await self.query_data
            elif issubclass(annotation_cls, Body):
                params = await self.body_data
            elif issubclass(annotation_cls, Form):
                params = await self.form_data
            else:
                params = await self._request.query_params
            annotations_var_dict.update({var_name: annotation_cls(**params)})
        return annotations_var_dict

    @classmethod
    def as_view(cls, **init_kwargs):
        """
        View视图转化方法构造器
        :param init_kwargs: [dict] 初始化参数
        :return: [Callable] 用于路由中的方法
        """

        async def view(request, *args, **kwargs):
            """
            View对象生成
            :param request: [starlette.Requests]  starlette 请求体对象
            :param args: [list] 列表参数
            :param kwargs: [dict] 字典参数
            :return:
            """
            self = cls(request=request, **init_kwargs)
            return await self.dispatch_method(request, *args, **kwargs)

        view.view_class = cls
        view.view_init_kwargs = init_kwargs
        return view


class RestView(View):

    def as_rest_response(self, code, message, data=None):
        """
        生成Restful形式的返回值

        :param code: [int] 返回代码
        :param message: [str] 返回消息
        :param data: [json] 用户返回内容
        :return:
        """
        resp = RestResponse(code=code, message=message, data=data)
        return resp
