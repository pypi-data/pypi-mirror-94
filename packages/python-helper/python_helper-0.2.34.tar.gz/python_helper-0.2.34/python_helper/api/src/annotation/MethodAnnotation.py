from python_helper.api.src.service import LogHelper, ReflectionHelper
from python_helper.api.src.domain import Constant as c

def Function(function,*args,**kwargs) :
    def wrapedFunction(*args,**kwargs) :
        try :
            functionReturn = function(*args,**kwargs)
        except Exception as exception :
            functionName = ReflectionHelper.getName(function, typeName=c.TYPE_FUNCTION)
            LogHelper.wraper(Function,f'''Failed to execute "{functionName}(args={args}, kwargs={kwargs})" {c.TYPE_FUNCTION} call''', exception)
            raise exception
        return functionReturn
    ReflectionHelper.overrideSignatures(wrapedFunction, function)
    return wrapedFunction

def Method(method,*args,**kwargs) :
    def wrapedMethod(*args,**kwargs) :
        try :
            methodReturn = method(*args,**kwargs)
        except Exception as exception :
            className = ReflectionHelper.getName(args[0].__class__, typeName=c.TYPE_CLASS)
            methodName = ReflectionHelper.getName(method, typeName=c.TYPE_METHOD)
            LogHelper.wraper(Method,f'''Failed to execute "{className}{c.DOT}{methodName}(args={args}, kwargs={kwargs})" {c.TYPE_METHOD} call''',exception)
            raise exception
        return methodReturn
    ReflectionHelper.overrideSignatures(wrapedMethod, method)
    return wrapedMethod
