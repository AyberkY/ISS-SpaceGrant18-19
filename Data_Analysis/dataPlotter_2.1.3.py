import matplotlib.pyplot as plt
import numpy as np

filename1 = "./flight1/2019-08-10_10_45_46.441775.txt"
telemFilename1 = './flight1/2019-08-10-serial-5013-flight-0003.csv'
telemFilename2 = './flight2/2019-08-10-serial-5013-flight-0004.csv'

def readData(filename, read_start_line=7082, read_end_line=8130, read_start_time=-5, read_end_time=1000):

    filehandle = open(filename, 'r')

    dataTypes = "unix_timestamp,state,latitude,longitude,altitude,satellites,bat1,bat2,bat3,baro_pressure,baro_altitude,cTemp,pitot,mpu_acc_x,mpu_acc_y,mpu_acc_z,mpu_gyr_x,mpu_gyr_y,mpu_gyr_z,mpu_roll,h3_acc_x,h3_acc_y,h3_acc_z,vertical_speed,sep_det"
    dataType_array = dataTypes.split(',')

    dataDict = {}

    for key in dataType_array:
        dataDict[key] = []

    lineNumber = 0
    for line in filehandle:
        lineNumber += 1
        if lineNumber >= read_start_line and lineNumber < read_end_line:
            dataString = filehandle.readline()[1:-2]
            dataArray = dataString.split(", ")
            for index, data in enumerate(dataType_array):
                try:
                    if float(dataArray[0]) >= read_start_time and float(dataArray[0]) <= read_end_time:
                        try:
                            dataDict[data].append(float(dataArray[index]))
                        except ValueError:
                            dataDict[data].append(0.0)
                except:
                    pass

    return dataDict

def readTelemData(filename, read_start_line=0, read_end_line=5000, read_start_time=-5, read_end_time=1000):
    filehandle = open(filename, 'r')
    dataType_array = filehandle.readline()[1:-1].split(',')

    dataDict = {}

    for key in dataType_array:
        dataDict[key] = []

    lineNumber = 0
    for line in filehandle:
        lineNumber += 1
        if lineNumber >= read_start_line and lineNumber < read_end_line:
            dataString = filehandle.readline()[:-1]
            dataArray = dataString.split(',')
            # print(dataArray)
            for index, data in enumerate(dataType_array):
                try:
                    if float(dataArray[4]) >= read_start_time and float(dataArray[4]) <= read_end_time:
                        try:
                            # print(dataArray)
                            dataDict[data].append(float(dataArray[index]))
                        except ValueError:
                            dataDict[data].append(dataArray[index])
                        except:
                            pass
                except:
                    pass
    return dataDict

def processData(points, scale=1.0, offset=0.0):
    newPoints = []
    for point in points:
        newPoints.append((point + offset) * scale)
    return newPoints

def smoothData(points, factor=0.8):
    smoothedData = []
    previousPoint = points[0]
    for point in points:
        if not smoothedData:
            smoothedData.append(previousPoint)
        else:
            smoothedData.append(previousPoint * factor + point * (1 - factor))
    return smoothedData

def baroSmoother(inputPoints):
    newPoints = []
    plateauPoints = []
    for point in inputPoints:
        if not newPoints:
            newPoints.append(point)
        else:
            if point == newPoints[-1]:
                plateauPoints.append(point)
            else:
                for i in range(len(plateauPoints)):
                    newPoints.append(plateauPoints[0] + ((i + 1) * ((point - plateauPoints[0]) / (len(plateauPoints) + 1))))
                newPoints.append(point)
                plateauPoints = []

    newPoints += plateauPoints

    return newPoints

def findPeak(array):
    peakVal = 0
    peakIndex = 0
    for i, val in enumerate(array):
        if val > peakVal:
            peakVal = val
            peakIndex = i

    return peakIndex, peakVal

def integrate(timeSteps, dataArray):
    sum = 0
    outputArray = []
    for i in range(len(timeSteps)):
        sum += dataArray[i] * (timeSteps[i] - timeSteps[i - 1])
        outputArray.append(sum)
    return outputArray

def integrateRoll(timeSteps, dataArray):
    sum = 0
    outputArray = []
    for i in range(len(timeSteps)):
        sum += dataArray[i] * (timeSteps[i] - timeSteps[i - 1])
        if sum > 720:
            sum -= 720
        elif sum < 0:
            sum += 720
        outputArray.append(sum)
    return outputArray

dataDict = readData(filename1, read_end_time=20)

# plt.subplot(211)
plt.plot(dataDict['unix_timestamp'], dataDict['mpu_gyr_x'], label="Roll Rate about Rocket Axis")
peakRollIndex, peakRollRate = findPeak(dataDict['mpu_gyr_x'])
plt.axvline(dataDict['unix_timestamp'][peakRollIndex], color='orange', label="Peak Roll Rate")
plt.scatter(dataDict['unix_timestamp'][peakRollIndex], dataDict['mpu_gyr_x'][peakRollIndex], marker='.', color='orange')
plt.text(dataDict['unix_timestamp'][peakRollIndex] + 0.05, dataDict['mpu_gyr_x'][peakRollIndex], str(dataDict['mpu_gyr_x'][peakRollIndex]), fontsize=9)
plt.grid()
plt.xlabel("Time [s]")
plt.ylabel("Roll Rate [$^{\circ}/s$]")
plt.title("Roll Rate During Flight 1")
plt.legend()

# plt.subplot(212)
# plt.plot(dataDict['unix_timestamp'], integrate(dataDict['unix_timestamp'], dataDict['mpu_gyr_x']), linestyle=':', label="Cumulative Roll about Rocket Axis")
# plt.grid()

plt.show()
