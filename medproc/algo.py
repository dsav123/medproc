from bisect import bisect_left, bisect_right
import itertools
from collections import Counter, OrderedDict
from scipy.stats import pearsonr


class OrderedCounter(Counter, OrderedDict):

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, OrderedDict(self))

    def __reduce__(self):
        return self.__class__, (OrderedDict(self),)


# takes general dataset and returns dataset between 2 dates
def choosedates(array1, start, end):

    dates = [x[0] for x in array1]
    left = bisect_left(dates, start)
    right = bisect_right(dates, end)
    return array1[left:right]


def generaldate(dataset):
    datelist = []
    for x in dataset:
        datelist.append(x[0])

    c = OrderedCounter(datelist)
    list1 = []
    for k, v in c.items():
        list1.append((k, v))

    datavalue = []
    for x in c.keys():
        datavalue.append(c[x])

    return list1


# takes the dataset and returns a list of all symptoms
def generalsympt(dataset):
    symptlist = []

    for x in dataset:
        symptlist.append(x[1])
    a = Counter(symptlist)

    keyvalue = []
    for k, v in a.items():
        keyvalue.append((k, v))

    return keyvalue


# takes the dataset and returns a list of all diagnosis
def generaldiag(dataset):
    diaglist = []

    for x in dataset:
        diaglist.append(x[2])
    a = Counter(diaglist)

    keyvalue = []
    for k, v in a.items():
        keyvalue.append((k, v))

    return keyvalue


def counting(data):
    return Counter(data)


def singleday(dataset, date):
    dayset = []
    for x in dataset:
        if x[0] == date:
            dayset.append(x)
    if dayset == []:
        return 'error date not found'
    else:
        return dayset


def daybydaybreak(dataset):
    a = [list(group) for k, group in itertools.groupby(dataset, lambda x: x[0])]

    counterholder =[]
    test = []
    for c in a:
        for d in c:
            test.append(d[1])
        counterholder.append((d[0], counting(test)))
        test = []

    flatlist = []
    for b in dataset:
        flatlist.append(b[1])


def specsympt(dataset, sympt):
    a = [list(group) for k, group in itertools.groupby(dataset, lambda x: x[0])]
    counterholder = []
    test = []
    for c in a:
        for d in c:
            test.append(d[1])
        counterholder.append((d[0], counting(test)))
        test = []

    symptcount = []
    for i in counterholder:
        symptcount.append((i[0], i[1][sympt]))

    return symptcount


def specdiag(dataset, diag):
    a = [list(group) for k, group in itertools.groupby(dataset, lambda x: x[0])]
    counterholder =[]
    test = []
    for c in a:
        for d in c:
            test.append(d[2])
        counterholder.append((d[0], counting(test)))
        test = []
    diagcount = []
    for i in counterholder:
        diagcount.append((i[0], i[1][diag]))

    return diagcount


def dictstrip(dataset):
    stripped = []
    for i in dataset:
        stripped.append((i[0], i[1]))
    return stripped


def listsum(dataset):
    temp = []
    for i in dataset:
        temp.append(i[1])
    return sum(temp)/len(temp)


def significance(sum, total):
    if float(sum) <= (float(total)*0.01):
        return 'This symptom is not siginificant'
    if (float(sum) > (float(total)*0.01)) and (float(sum) <= (float(total)*0.05)):
        return 'this symptom is significant'
    if (float(sum) > (float(total) * 0.05)) and (float(sum) <= (float(total) * 0.1)):
        return 'this symptom is very significant'
    if float(sum) > (float(total)*0.1):
        return 'This symptom is extremely siginificant'


def comparedate(start, end, data):
    if start >= data[0][:10] and end <= data[-1][:10]:
        return True
    else:
        return False


def corrsympt(dataset, sympt):
    a = specsympt(dataset, sympt)
    b = generaldiag(dataset)

    list1 = []
    for g in a:
        list1.append(g[1])

    list2 = []
    for h in b:
        list2.append(h[0])

    list3 = []
    for i in list2:
        j = specdiag(dataset, i)
        list4 = []
        for h in j:
            list4.append(h[1])
        corr, _ = pearsonr(list1, list4)
        list3.append(corr)

    return list2, list3


def corrdiag(dataset, diag):
    a = specdiag(dataset, diag)
    b = generalsympt(dataset)

    list1 = []
    for g in a:
        list1.append(g[1])

    list2 = []
    for h in b:
        list2.append(h[0])

    list3 = []
    for i in list2:
        j = specsympt(dataset, i)
        list4 = []
        for h in j:
            list4.append(h[1])
        corr, _ = pearsonr(list1, list4)
        list3.append(corr)

    return list2, list3


if __name__ == "__main__":
    print("hi")
