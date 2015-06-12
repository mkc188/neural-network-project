import math
import random
import string
import sys
import itertools
import time

class NeuralNetwork:
    def __init__(self, MAX, SMALL, NI=30, NH=3, NO=1, N=0.0003, M=0, ACCURACY=0.9):
        self.best = open(sys.argv[3], mode='w')

        self.ni = int(NI + 1)
        self.nh = int(NH + 1)
        self.no = int(NO)
        self.max = int(MAX)
        self.n = float(N)
        self.m = float(M)
        self.accuracy = float(ACCURACY)
        self.checkpt = 100 if SMALL == 0 else 50

        self.best.write(str(ACCURACY) + '\n')
        self.best.write(str(NI) + ' ')
        self.best.write(str(NH) + ' ')
        self.best.write(str(NO) + '\n')

        self.ai, self.ah, self.ao = [],[],[]
        self.ai = [1]*self.ni
        self.ah = [1]*self.nh
        self.ao = [1]*self.no

        self.wi = matrix(self.ni, self.nh)
        self.wo = matrix(self.nh, self.no)

        randomMatrix(self.wi, -0.2, 0.2)
        randomMatrix(self.wo, -0.2, 0.2)

        self.ci = matrix(self.ni, self.nh)
        self.co = matrix(self.nh, self.no)

    def __del__(self):
        self.best.close()

    def feedForward(self, inputs):
        for i in range(self.ni-1):
            self.ai[i] = inputs[i]

        for i in range(self.nh):
            sum = 0.0
            for j in range(self.ni):
                sum += (self.ai[j]*self.wi[j][i])
            self.ah[i] = sigmoid(sum)

        for i in range(self.no):
            sum = 0.0
            for j in range(self.nh):
                sum += (self.ah[j]*self.wo[j][i])
            self.ao[i] = sigmoid(sum)

    def backPropagate(self, targets, N, M):
        outputDeltas = [0.0] * self.no
        for i in range(self.no):
            error = targets[i] - self.ao[i]
            bias = 1 if targets[i] == 1 else -1
            # print self.ao[i]

            outputDeltas[i] =  error * dsigmoid(self.ao[i])

        for i in range(self.nh):
            for j in range(self.no):
                diff = outputDeltas[j] * self.ah[i]
                self.wo[i][j] -= (N*diff + M*self.co[i][j])*bias
                # print diff
                self.co[i][j] = diff

        hiddenDeltas = [0.0] * self.nh
        for i in range(self.nh):
            error = 0.0
            for j in range(self.no):
                error += outputDeltas[j] * self.wo[i][j]
            hiddenDeltas[i] = error * dsigmoid(self.ah[i])

        for i in range (self.ni):
            for j in range (self.nh):
                diff = hiddenDeltas[j] * self.ai[i]
                self.wi[i][j] -= (N*diff + M*self.ci[i][j])*bias
                self.ci[i][j] = diff

        # error = 0.0
        # for i in range(len(targets)):
        #     error += 0.5 * (targets[i]-self.ao[i])**2
        # error /= len(targets)
        # return error
        return (targets[0], self.ao[0])

    def weights(self):
        self.best.write('I ' + str(self.ni-1) + ' H ' + str(self.nh-1) + '\n')
        for i in range(self.nh-1):
            for j in range(self.ni-1):
                self.best.write(str(self.wi[j][i]) + ' ')
            self.best.write(str(self.wi[j][i]) + '\n')
        self.best.write('H ' + str(self.nh-1) + ' O ' + str(self.no) + '\n')
        for i in range(self.no):
            for j in range(self.nh-1):
                self.best.write(str(self.wo[j][i]) + ' ')
            self.best.write(str(self.wo[j][i]) + '\n')

    def train(self, patterns):
        for i in range(self.max):
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                self.feedForward(inputs)
                error = self.backPropagate(targets, self.n, self.m)
            print error

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def dsigmoid(y):
    return (1 - y)*y

def matrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill]*J)
    return m

def randomMatrix(matrix, a, b):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = random.uniform(a,b)

def main ():
    pattern = []
    dataset = open(sys.argv[1])
    answer = open(sys.argv[2])

    for dLine, aLine in itertools.izip(dataset, answer):
        temp = []
        temp.append(map(int, dLine.split()))
        temp.append(map(int, aLine.split()))
        pattern.append(temp)

    NN = NeuralNetwork (sys.argv[4], sys.argv[5])
    NN.train(pattern)
    NN.weights()

    dataset.close()
    answer.close()

if __name__ == "__main__":
    main()
