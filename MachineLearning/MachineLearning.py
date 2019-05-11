from __future__ import division
import math


class item:
    def __init__(self, age, prescription, astigmatic, tearRate, needLense):
        self.age = age
        self.prescription = prescription
        self.astigmatic = astigmatic
        self.tearRate = tearRate
        self.needLense = needLense


def getDataset():
    data = []
    labels = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0]
    data.append(item(0, 0, 0, 0,	labels[0]))
    data.append(item(0, 0, 0, 1,	labels[1]))
    data.append(item(0, 0, 1, 0,	labels[2]))
    data.append(item(0, 0, 1, 1,	labels[3]))
    data.append(item(0, 1, 0, 0,	labels[4]))
    data.append(item(0, 1, 0, 1,	labels[5]))
    data.append(item(0, 1, 1, 0,	labels[6]))
    data.append(item(0, 1, 1, 1,	labels[7]))
    data.append(item(1, 0, 0, 0,	labels[8]))
    data.append(item(1, 0, 0, 1,	labels[9]))
    data.append(item(1, 0, 1, 0,	labels[10]))
    data.append(item(1, 0, 1, 1,	labels[11]))
    data.append(item(1, 1, 0, 0,	labels[12]))
    data.append(item(1, 1, 0, 1,	labels[13]))
    data.append(item(1, 1, 1, 0,	labels[14]))
    data.append(item(1, 1, 1, 1,	labels[15]))
    data.append(item(1, 0, 0, 0,	labels[16]))
    data.append(item(1, 0, 0, 1,	labels[17]))
    data.append(item(1, 0, 1, 0,	labels[18]))
    data.append(item(1, 0, 1, 1,	labels[19]))
    data.append(item(1, 1, 0, 0,	labels[20]))
    return data


class Feature:
    def __init__(self, name):
        self.name = name
        self.visited = False
        self.infoGain = -1


class node:

    def __init__(self, rows):
        self.leaf = False
        self.prediction = None
        self.left = None #true
        self.right = None #false
        self.question = None
        self.rows = rows

    def isLeaf(self):
        return self.left == None and self.right == None


class ID3:

    def getGain(self, left, right, impurity):
        p = float(len(left)) / (len(left) + len(right))
        return impurity - p * self.calcImpurity(left) - (1 - p) * self.calcImpurity(right)

    def calcImpurity(self, rows):
        one = 0
        zero = 0
        for r in rows:
            if r.needLense == 1:
                one += 1
            else:
                zero += 1
        n = len(rows)
        imp = 0
        if one > 0:
            imp -= one / float(n) * math.log(one / float(n), 2)
        if zero > 0:
            imp -= zero / float(n) * math.log(zero / float(n), 2)
        return imp

    def bestQuestion(self, rows):
        bestGain = 0
        q = None
        impurity = self.calcImpurity(rows)
        for f in self.features:
            if f.visited == False:
                trueRows, falseRows = self.split(rows, f.name)
                if len(trueRows) == 0 or len(falseRows) == 0:
                    continue
                gain = self.getGain(trueRows, falseRows, impurity)
                if gain >= bestGain:
                    bestGain = gain
                    q = f.name
        for f in features:
            if f.name == q:
                f.visited = True
                f.infoGain = bestGain
        return bestGain, q

    def split(self, rows, question):
        yesList = []
        noList = []
        for r in rows:
            if question == 'age':
                if r.age == 1:
                    yesList.append(r)
                else:
                    noList.append(r)
            if question == 'prescription':
                if r.prescription == 1:
                    yesList.append(r)
                else:
                    noList.append(r)
            if question == 'astigmatic':
                if r.astigmatic == 1:
                    yesList.append(r)
                else:
                    noList.append(r)
            if question == 'tearRate':
                if r.tearRate == 1:
                    yesList.append(r)
                else:
                    noList.append(r)
        return yesList, noList

    def count(self, rows):
        counts = {}
        for row in rows:
            label = row.needLense
            if label not in counts:
                counts[label] = 0
            counts[label] += 1
        return counts

    def buildTree(self, rows):
        nodee = node(rows)
        gain, question = self.bestQuestion(nodee.rows)
        nodee.question = question
        if gain == 0:
            nodee.leaf = True
            nodee.prediction = self.count(rows)
            return nodee
        trueRows, falseRows = self.split(nodee.rows, question)
        nodee.left = self.buildTree(trueRows)
        nodee.right = self.buildTree(falseRows)
        return nodee

    def __init__(self, features, dataset):
        self.features = features
        self.root = self.buildTree(dataset)

    def classify(self, input, nodee):
        if nodee.leaf:
            for key, value in nodee.prediction.items():
                return key

        if nodee.question == 'age':
            if input[0] == 1:
                return self.classify(input, nodee.left)
            else:
                return self.classify(input, nodee.right)
        if nodee.question == 'prescription':
            if input[1] == 1:
                return self.classify(input, nodee.left)
            else:
                return self.classify(input, nodee.right)
        if nodee.question == 'astigmatic':
            if input[2] == 1:
                return self.classify(input, nodee.left)
            else:
                return self.classify(input, nodee.right)
        if nodee.question == 'tearRate':
            if input[3] == 1:
                return self.classify(input, nodee.left)
            else:
                return self.classify(input, nodee.right)

    def show(self, nodee):
        print(nodee.question)
        if nodee.leaf is False:
            print('left of ', nodee.question, '-->')
            self.show(nodee.left)
            print('right of ', nodee.question, '-->')
            self.show(nodee.right)
        else:
            for key, value in nodee.prediction.items():
                print('prediction of this node is ', key)


dataset = getDataset()
features = [Feature('age'), Feature('prescription'), Feature('astigmatic'), Feature('tearRate')]
id3 = ID3(features, dataset)
cls = id3.classify([0, 0, 1, 1], id3.root)  # should print 1
print('testcase 1: ', cls)
cls = id3.classify([1, 1, 0, 0], id3.root)  # should print 0
print('testcase 2: ', cls)
cls = id3.classify([1, 1, 1, 0], id3.root)  # should print 0
print('testcase 3: ', cls)
cls = id3.classify([1, 1, 0, 1], id3.root)  # should print 1
print('testcase 4: ', cls)







