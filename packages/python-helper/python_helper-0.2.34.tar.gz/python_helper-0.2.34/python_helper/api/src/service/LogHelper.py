import colorama, traceback
from python_helper.api.src.domain import Constant as c
from python_helper.api.src.service import SettingHelper, StringHelper, EnvironmentHelper, ObjectHelper, ReflectionHelper

LOG = 'LOG'
SUCCESS = 'SUCCESS'
SETTING = 'SETTING'
DEBUG = 'DEBUG'
WARNING = 'WARNING'
WRAPPER = 'WRAPPER'
FAILURE = 'FAILURE'
ERROR = 'ERROR'
TEST = 'TEST'

RESET_ALL_COLORS = colorama.Style.RESET_ALL

from python_helper.api.src.helper import LogHelperHelper

global LOG_HELPER_SETTINGS

def loadSettings() :
    global LOG_HELPER_SETTINGS
    colorama.deinit()
    settings = {}
    settings[SettingHelper.ACTIVE_ENVIRONMENT] = SettingHelper.getActiveEnvironment()
    if SettingHelper.activeEnvironmentIsLocal() :
        colorama.init()
        print(RESET_ALL_COLORS,end=c.NOTHING)
    for level in LogHelperHelper.LEVEL_DICTIONARY :
        status = EnvironmentHelper.get(level)
        settings[level] = status if not status is None else c.TRUE
    LOG_HELPER_SETTINGS = settings

loadSettings()

def log(origin, message, level=LOG, exception=None, newLine=False) :
    LogHelperHelper.softLog(origin, message, LOG, newLine=newLine, exception=exception)

def success(origin, message, newLine=False) :
    LogHelperHelper.softLog(origin, message, SUCCESS, newLine=newLine)

def setting(origin, message, newLine=False) :
    LogHelperHelper.softLog(origin, message, SETTING, newLine=newLine)

def debug(origin, message, exception=None, newLine=False) :
    LogHelperHelper.softLog(origin, message, DEBUG, newLine=newLine, exception=exception)

def warning(origin, message, exception=None, newLine=False) :
    LogHelperHelper.softLog(origin, message, WARNING, newLine=newLine, exception=exception)

def wraper(origin, message, exception, newLine=False) :
    LogHelperHelper.hardLog(origin, message, exception, WRAPPER, newLine=newLine)

def failure(origin, message, exception, newLine=False) :
    LogHelperHelper.hardLog(origin, message, exception, FAILURE, newLine=newLine)

def error(origin, message, exception, newLine=False) :
    LogHelperHelper.hardLog(origin, message, exception, ERROR, newLine=newLine)

def test(origin, message, exception=None, newLine=False) :
    LogHelperHelper.softLog(origin, message, TEST, newLine=newLine, exception=exception)

def printLog(message, condition=False, newLine=True, margin=True, exception=None) :
    LogHelperHelper.printMessageLog(LOG, message, condition=condition, newLine=newLine, margin=margin, exception=exception)

def printSuccess(message, condition=False, newLine=True, margin=True) :
    LogHelperHelper.printMessageLog(SUCCESS, message, condition=condition, newLine=newLine, margin=margin)

def printSetting(message, condition=False, newLine=True, margin=True) :
    LogHelperHelper.printMessageLog(SETTING, message, condition=condition, newLine=newLine, margin=margin)

def printDebug(message, condition=False, newLine=True, margin=True, exception=None) :
    LogHelperHelper.printMessageLog(DEBUG, message, condition=condition, newLine=newLine, margin=margin, exception=exception)

def printWarning(message, condition=False, newLine=True, margin=True, exception=None) :
    LogHelperHelper.printMessageLog(WARNING, message, condition=condition, newLine=newLine, margin=margin, exception=exception)

def printWarper(message, condition=False, newLine=True, margin=True, exception=None) :
    LogHelperHelper.printMessageLog(WRAPPER, message, condition=condition, newLine=newLine, margin=margin, exception=exception)

def printFailure(message, condition=False, newLine=True, margin=True, exception=None) :
    LogHelperHelper.printMessageLog(FAILURE, message, condition=condition, newLine=newLine, margin=margin, exception=exception)

def printError(message, condition=False, newLine=True, margin=True, exception=None) :
    LogHelperHelper.printMessageLog(ERROR, message, condition=condition, newLine=newLine, margin=margin, exception=exception)

def printTest(message, condition=False, newLine=True, margin=True, exception=None) :
    LogHelperHelper.printMessageLog(TEST, message, condition=condition, newLine=newLine, margin=margin, exception=exception)

def prettyPython(
        origin,
        message,
        dictionaryInstance,
        quote = c.SINGLE_QUOTE,
        tabCount = 0,
        nullValue = c.NONE,
        trueValue = c.TRUE,
        falseValue = c.FALSE,
        logLevel = LOG,
        condition = True
    ) :
    if condition :
        stdout, stderr = EnvironmentHelper.getCurrentSoutStatus()
        prettyPythonValue = StringHelper.prettyPython(
            dictionaryInstance,
            quote = quote,
            tabCount = tabCount,
            nullValue = nullValue,
            trueValue = trueValue,
            falseValue = falseValue,
            withColors = SettingHelper.activeEnvironmentIsLocal(),
            joinAtReturn = False
        )
        LogHelperHelper.softLog(origin, StringHelper.join([message, c.COLON_SPACE, *prettyPythonValue]), logLevel)
        EnvironmentHelper.overrideSoutStatus(stdout, stderr)

def prettyJson(
        origin,
        message,
        dictionaryInstance,
        quote = c.DOUBLE_QUOTE,
        tabCount = 0,
        nullValue = c.NULL_VALUE,
        trueValue = c.TRUE_VALUE,
        falseValue = c.FALSE_VALUE,
        logLevel = LOG,
        condition = True
    ) :
    if condition :
        stdout, stderr = EnvironmentHelper.getCurrentSoutStatus()
        prettyJsonValue = StringHelper.prettyJson(
            dictionaryInstance,
            quote = quote,
            tabCount = tabCount,
            nullValue = nullValue,
            trueValue = trueValue,
            falseValue = falseValue,
            withColors = SettingHelper.activeEnvironmentIsLocal(),
            joinAtReturn = False
        )
        LogHelperHelper.softLog(origin, StringHelper.join([message, c.COLON_SPACE, *prettyJsonValue]), logLevel)
        EnvironmentHelper.overrideSoutStatus(stdout, stderr)


def getExceptionMessage(exception) :
    if ObjectHelper.isEmpty(exception) :
        return c.UNKNOWN
    exceptionAsString = str(exception)
    if c.NOTHING == exceptionAsString :
        return ReflectionHelper.getName(exception.__class__)
    else :
        return exceptionAsString

def getTracebackMessage() :
    tracebackMessage = None
    try :
        tracebackMessage = traceback.format_exc()
    except :
        tracebackMessage = f'{c.NEW_LINE}'
    return LogHelperHelper.NO_TRACEBACK_PRESENT_MESSAGE if LogHelperHelper.NO_TRACEBACK_PRESENT == str(tracebackMessage) else tracebackMessage
