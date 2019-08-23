import matplotlib.pyplot as plt
import numpy as np

filename1 = "./flight1/2019-08-10_10_45_46.441775.txt"
stratFilename1 = "./flight1/strat_flight_1.pf2"
stratFilename2 = "./flight2/strat_flight_2.pf2"
telemFilename1 = './flight1/2019-08-10-serial-5013-flight-0003.csv'
telemFilename2 = './flight2/2019-08-10-serial-5013-flight-0004.csv'
simFilename1 = './flight1/sim1.csv'
simFilename2 = './flight2/sim2.csv'

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

dataDict = readData(filename1, read_end_time=6)
telemDict = readTelemData(telemFilename1, read_end_time=6)
simDict = readSimData(simFilename1, read_end_time=6)

machIndex = 0
for i, vel in enumerate(telemDict['accel_speed']):
    if vel >= 343:
        machIndex = i
        break

fig, ax = plt.subplots()

ax.plot(telemDict['time'], telemDict['accel_speed'], color='r', label="TM Accel Speed")
# ax.plot(dataDict['unix_timestamp'], processData(dataDict['pitot'], -0.26, -8188), label="pitot_scaled")

scaleFactor = (8175 - 8182) / 31.7398
ax.plot(dataDict['unix_timestamp'], processData(dataDict['pitot'], scaleFactor, -8188), label="pitot_scaled (" + str(scaleFactor) + ")")
plt.xlabel("Time [s]")
plt.ylabel("Vertical Speed [m/s]")
plt.grid()
# ax.plot(telemDict['time'], telemDict['acceleration'], label="TM_acceleration")

# ax.axvline(telemDict['time'][machIndex], color='b', label='Mach')
# ax.scatter(telemDict['time'][machIndex], telemDict['accel_speed'][machIndex], marker='.', color='b')
# ax.text(telemDict['time'][machIndex] + 0.03, telemDict['accel_speed'][machIndex] - 5, str(telemDict['accel_speed'][machIndex]), fontsize=9)
#
# peakVelIndex, peakVel = findPeak(telemDict['accel_speed'])
# ax.axvline(telemDict['time'][peakVelIndex], color='orange', label='Peak Speed')
# ax.scatter(telemDict['time'][peakVelIndex], telemDict['accel_speed'][peakVelIndex], marker='.', color='orange')
# ax.text(telemDict['time'][peakVelIndex] + 0.05, telemDict['accel_speed'][peakVelIndex], str(telemDict['accel_speed'][peakVelIndex]), fontsize=9)

# xt = range(7)
# xt = np.append(xt, telemDict['time'][machIndex])
# xt = np.append(xt, telemDict['time'][peakVelIndex])
# xtl=xt.tolist()
# xtl[-1]=str(telemDict['time'][peakVelIndex])
# xtl[-2]=str(telemDict['time'][machIndex])
# ax.set_xticks(xt)
# ax.set_xticklabels(xtl)

plt.legend()
plt.show()
