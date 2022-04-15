from email.mime import base
import numpy as np
import matplotlib.pyplot as plt

fileTargets = './IOC-L08-ep8chTargets.dat'
fileNonTargets = './IOC-L08-ep8chNONTargets.dat'

def applyProcessing(path):
    with open(path, 'r') as file:
        channels = int(file.readline().strip())
        samples = int(file.readline().strip())
        trials = int(file.readline().strip())
        _ = int(file.readline().strip())
        sampleRate = int(file.readline().strip())

        dataChar = [x.strip() for x in filter(lambda x: x != '\n', file.readlines())]
        dataChar = [x.split() for x in dataChar]
        data = []
        for d in dataChar:
            data.append([float(x) for x in d])
        

    channelList = []

    for i in range(channels):
        avg = np.zeros(samples)
        j = i
        baseline = np.sum(data[j][:26]) / 26
        while j <= trials:
            avg = np.add(avg, np.subtract(data[j], baseline))
            j += channels
        avg = (1 / trials) * avg
        channelList.append(avg)
    
    return channelList, sampleRate

if __name__ == '__main__':
    channelListTarget, rate = applyProcessing(fileTargets)
    channelListNonTarget, rate = applyProcessing(fileNonTargets)

    for j in range(len(channelListNonTarget)):
        plt.plot(channelListTarget[j])
        plt.plot(channelListNonTarget[j])
        plt.savefig(f'fig{j}.png')
        plt.close()