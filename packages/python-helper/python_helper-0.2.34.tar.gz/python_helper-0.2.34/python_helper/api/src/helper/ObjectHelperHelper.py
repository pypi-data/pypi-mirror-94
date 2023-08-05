from python_helper.api.src.service import ObjectHelper, ReflectionHelper

def generatorInstance() :
    while True :
        yield False
        break

def leftEqual(left, right, visitedInstances) :
    isEqual = True
    leftIsCollection = ObjectHelper.isCollection(left)
    rightIsCollection = ObjectHelper.isCollection(right)
    if leftIsCollection and rightIsCollection :
        if len(left) == len(right) :
            for itemLeft, itemRight in zip(left, right) :
                if isEqual :
                    isEqual = isEqual and ObjectHelper.equals(itemLeft, itemRight, visitedInstances=visitedInstances)
                else :
                    break
            return isEqual
        else :
            return False
    elif (leftIsCollection and not rightIsCollection) or (not leftIsCollection and rightIsCollection) :
        return False
    else :
        for value, name in ReflectionHelper.getAttributeDataList(left) :
            if isEqual :
                isEqual = isEqual and ObjectHelper.equals(value, ReflectionHelper.getAttributeOrMethod(right, name), visitedInstances=visitedInstances)
            else :
                break
        return isEqual
