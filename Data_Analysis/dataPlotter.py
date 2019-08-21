import matplotlib.pyplot as plt

filename1 = "./flight1/2019-08-10_10_45_46.441775.txt"
telemFilename1 = './flight1/2019-08-10-serial-5013-flight-0003.csv'
telemFilename2 = './flight2/2019-08-10-serial-5013-flight-0004.csv'

def readData(filename, read_start_line=7082, read_end_line=8130):

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
                    dataDict[data].append(float(dataArray[index]))
                except ValueError:
                    dataDict[data].append(0.0)

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


dataDict = readData(filename1)
telemDict = readTelemData(telemFilename1, read_end_time=10)

machIndex = 0
for i, vel in enumerate(telemDict['accel_speed']):
    if vel >= 343:
        machIndex = i
        break

peakAccelIndex = 0
peakAccel = 0
for i, accel in enumerate(telemDict['acceleration']):
    if accel > peakAccel:
        peakAccel = accel
        peakAccelIndex = i

fig, ax = plt.subplots()

ax.plot(telemDict['time'], telemDict['accel_speed'], label="TM_accel_speed")
ax.plot(telemDict['time'], telemDict['acceleration'], label="TM_acceleration")

ax.axvline(telemDict['time'][machIndex], color='r', linewidth = 0.75, label='Mach')
ax.scatter(telemDict['time'][machIndex], telemDict['accel_speed'][machIndex], marker='.', color='r')
ax.text(telemDict['time'][machIndex] + 0.05, telemDict['accel_speed'][machIndex], str(telemDict['accel_speed'][machIndex]), fontsize=8)

secax = ax.secondary_yaxis('right')
ax.axvline(telemDict['time'][peakAccelIndex], color='g', linewidth = 0.75, label='Peak Acceleration')
ax.scatter(telemDict['time'][peakAccelIndex], telemDict['acceleration'][peakAccelIndex], marker='.', color='r')
ax.text(telemDict['time'][peakAccelIndex] + 0.05, telemDict['acceleration'][peakAccelIndex] + 3, str(telemDict['acceleration'][peakAccelIndex]), fontsize=8)

# plt.plot(dataDict['unix_timestamp'], processData(dataDict['pitot'], -0.26, -8188), label="pitot_scaled")
plt.legend()
plt.show()
