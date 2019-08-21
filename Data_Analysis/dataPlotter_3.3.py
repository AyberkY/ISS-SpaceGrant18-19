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

dataDict = readData(filename1, read_end_time=6)
telemDict1 = readTelemData(telemFilename1, read_start_time=-0.1, read_end_time=6)
telemDict2 = readTelemData(telemFilename2, read_start_time=-0.1, read_end_time=6)

plt.subplot(211)
plt.plot(dataDict['unix_timestamp'], processData(dataDict['pitot'], -0.26, -8188), label="Non-Commercial Pitot Sensor Speed")
plt.plot(dataDict['unix_timestamp'], processData(dataDict['h3_acc_x'], 9.81), label="Non-Commercial Vertical Acceleration")
plt.plot(telemDict1['time'], telemDict1['accel_speed'], label="TM Accel Speed")
plt.plot(telemDict1['time'], telemDict1['acceleration'], label="TM Acceleration")
plt.legend()
plt.grid()
plt.title("FLIGHT 1")

plt.subplot(212)
plt.plot(telemDict2['time'], telemDict2['accel_speed'], label="TM Accel Speed")
plt.plot(telemDict2['time'], telemDict2['acceleration'], label="TM Acceleration")
plt.legend()
plt.grid()
plt.title("FLIGHT 2")

plt.show()
