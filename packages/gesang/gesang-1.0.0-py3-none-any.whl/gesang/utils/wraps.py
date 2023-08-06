from gesang.utils import exc
from pydantic.error_wrappers import ValidationError
from starlette.responses import JSONResponse


def view_error_wrap(func):
    """
    视图方法全局异常处理装饰器

    :param func: [Callable] 视图方法
    :return:
    """

    async def inner(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except exc.MethodNotAllowed:
            return JSONResponse(status_code=405, content={"message": "Method not allowed."})
        except ValidationError as e:
            return JSONResponse(status_code=400, content={"message": str(e)})
        except exc.Error as e:
            return JSONResponse(status_code=500, content={"message": str(e)})
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": str(e)})

    return inner
