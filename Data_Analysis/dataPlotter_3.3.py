import matplotlib.pyplot as plt
import numpy as np

filename1 = "./flight1/2019-08-10_10_45_46.441775.txt"

stratFilename1 = "./flight1/strat_flight_1.pf2"
stratFilename2 = "./flight2/strat_flight_2.pf2"
telemFilename1 = './flight1/2019-08-10-serial-5013-flight-0003.csv'
telemFilename2 = './flight2/2019-08-10-serial-5013-flight-0004.csv'
simFilename1 = './flight1/sim1.csv'
simFilename2 = './flight2/sim2.csv'

def readData(filename, read_start_line=7078, read_end_line=8130, read_start_time=-5, read_end_time=1000):

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

def readStratData(filename, read_start_line=18, read_end_line=5000, read_start_time=-5, read_end_time=1000):
    filehandle = open(filename, 'r')
    dataType_array = ["time", "altitude", "velocity", "temperature", "voltage"]

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

def readSimData(filename, read_start_line=9, read_end_line=5000, read_start_time=-5, read_end_time=1000):
    filehandle = open(filename, 'r')
    dataType_array = ["time", "altitude", "velocity", "acceleration"]

    dataDict = {}

    for key in dataType_array:
        dataDict[key] = []

    lineNumber = 0
    for line in filehandle:
        lineNumber += 1
        if line[0] != '#':
            if lineNumber >= read_start_line and lineNumber < read_end_line:
                dataString = filehandle.readline()[:-1]
                dataArray = dataString.split(',')
                # print(dataArray)
                for index, data in enumerate(dataType_array):
                    try:
                        if float(dataArray[0]) >= read_start_time and float(dataArray[0]) <= read_end_time:
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

def differentiate(timeSteps, data):
    outputArray = [0]
    for i in range(len(timeSteps) - 1):
        delta = data[i + 1] - data[i]
        timeDelta = timeSteps[i + 1] - timeSteps[i]
        if timeDelta == 0.0:
            timeDelta = 0.0001
        outputArray.append(delta/timeDelta)
    return outputArray

dataDict1 = readData(filename1, read_end_time=6)
telemDict1 = readTelemData(telemFilename1, read_end_time=6)
simDict1 = readSimData(simFilename1, read_end_time=6)

plt.subplot(211)

plt.title("FLIGHT #1 (SUBSONIC)", fontsize=15)

plt.plot(telemDict1['time'], processData(telemDict1['acceleration'], scale=(1/0.3048)), color='orange', label="Telemetrum Acceleration")
plt.plot(dataDict1['unix_timestamp'], processData(processData(dataDict1['h3_acc_x'], scale=9.81, offset=-0.8764), scale=(1/0.3408)), color='r', label="Non-Commercial Acceleration")
plt.plot(simDict1['time'], simDict1['acceleration'], color='b', label="Simulated Acceleration")
plt.ylabel("Vertical Acceleration [$ft/s^2$]", fontsize=14)
plt.grid()
plt.legend(prop={'size':15})

plt.subplot(212)
plt.plot(telemDict1['time'], processData(telemDict1['accel_speed'], scale=(1/0.3048)), color='orange', label="Telemetrum Acceleration Speed")
plt.plot(dataDict1['unix_timestamp'], integrate(dataDict1['unix_timestamp'], processData(processData(dataDict1['h3_acc_x'], scale=9.81, offset=-0.8764), scale=(1/0.3048))), color='r', label="Non-Commercial Acceleration Speed")
scaleFactor = (8175 - 8182) / 31.7398
plt.plot(dataDict1['unix_timestamp'], processData(processData(dataDict1['pitot'], scaleFactor, -8188), scale=(1/0.3048)), color='g', label="Non-Commercial Pitot Measurement")
plt.plot(simDict1['time'], simDict1['velocity'], color='b', label="Simulated Speed")
plt.ylabel("Vertical Speed [$ft/s$]", fontsize=14)
plt.legend(prop={'size':15})
plt.xlabel("Time [s]", fontsize=14)
plt.grid()
plt.show()

# peakVal, pitotPeak = findPeak(processData(processData(dataDict1['pitot'], scaleFactor, -8188), scale=(1/0.3048)))
# print("Pitot Measurement Peak = " + str(pitotPeak))

telemDict2 = readTelemData(telemFilename2, read_end_time=6)
simDict2 = readSimData(simFilename2, read_end_time=6)

plt.subplot(211)

plt.title("FLIGHT #2 (SUPERSONIC)", fontsize=15)

plt.plot(telemDict2['time'], processData(telemDict2['acceleration'], scale=(1/0.3048)), color='orange', label="Telemetrum Acceleration")
plt.plot(simDict2['time'], simDict2['acceleration'], color='b', label="Simulated Acceleration")
plt.ylabel("Vertical Acceleration [$ft/s^2$]", fontsize=14)
plt.grid()
plt.legend(prop={'size':15})

plt.subplot(212)
plt.plot(telemDict2['time'], processData(telemDict2['accel_speed'], scale=(1/0.3048)), color='orange', label="Telemetrum Acceleration Speed")
# plt.plot(telemDict2['time'], differentiate(telemDict2['time'], processData(telemDict2['gps_altitude'], scale=(1/0.3048))), color='g', label="Telemetrum GPS Speed")
plt.plot(simDict2['time'], simDict2['velocity'], color='b', label="Simulated Speed")
plt.ylabel("Vertical Speed [$ft/s$]", fontsize=14)
plt.legend(prop={'size':15})
plt.xlabel("Time [s]", fontsize=14)
plt.grid()
plt.show()
