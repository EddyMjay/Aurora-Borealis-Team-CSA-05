import csv
import math
import statistics
import matplotlib.pyplot as plt

from numpy import array
from numpy import cov,var

day = 25
month = 12
yearStr = '2017'

#//////////////////////////////////////////////

dataType = 'mag_1m'


if day < 10:
    dayStr = '0'+str(day)
else:
    dayStr = str(day)

if month < 10:
    monthStr = '0'+str(month)
else:
    monthStr = str(month)


#File name for ground readings
aceFileName = 'daily\\' +yearStr+monthStr+dayStr+'_ace_'+dataType+'.txt'
#print('NEW : '+ aceFileName)

tempFile = open(aceFileName, 'r', newline = '')

dataz = tempFile.readlines()
dataz = dataz[20:]

usable = []
magnitudes = []
date = []
time = []

for line in dataz:
    if(line[36] == '0'):
        usable.append(True) #useable?
        magnitudes.append(float(line[72:77]))
    else:
        usable.append(False)
        magnitudes.append(float(line[72:77]))
    date.append(line[0:4]+line[5:7]+line[8:10])
    time.append(line[10:19])
    
new_csv = csv.writer(open("CSV_"+yearStr+monthStr+dayStr+'_ace_'+dataType+".csv", "w"), lineterminator = '\n')
csv_export = [date, time, magnitudes]
csv_export = zip(*csv_export)
csv_export = list(csv_export)



for x in range(len(csv_export)):
    new_csv.writerow(csv_export[x])



#/////////////////////////////////////////////////////////////////

station = "KAPU"
# file name for ground-based readings
GroupFileName = yearStr+'\\'+monthStr+'\\'+dayStr+'\\'+station+'17'+monthStr+dayStr+'_MAG_00_00.HKD'


file = open(GroupFileName, 'r')

rows = file.readlines()
rows = rows[1:]

# the month/day/year of the data
date=[]
# the time of each data line
time=[]
# the magnitude of the magnetic field in nanoteslas
b_total=[]

for line in rows:
    date.append(line[0:8])
    
    time.append(line[11:13]+line[14:16])
    b_north = float(line[42:50])
    b_west = float(line[53:60])
    b_ground = float(line[62:70])
    #b_total.append(math.sqrt(b_north**2 + b_west**2 + b_ground**2))
    b_total.append(math.sqrt(b_north**2 + b_west**2))

# exporting to Excel
new_csv = csv.writer(open("CSV_"+yearStr+monthStr+dayStr+'GMAG'+".csv", "w"), lineterminator = '\n')
csv_export = [date, time, b_total]
csv_export = zip(*csv_export)
csv_export = list(csv_export)
#print(csv_export)

for x in range(len(csv_export)):
    new_csv.writerow(csv_export[x])
#    wr.writerow(csv_export[x])
file.close()
    
#List for ACE axis: magnitudes
#List for gmag axis: b_total


new_mags = []
new_b_total = []
new_1_time = []
new_2_time = []


for st in time:
    
    new_t = int(st[0:2])*60+int(st[2:4])
    new_1_time.append(new_t)

for i in range(len(magnitudes)-1):
   
    if(usable[i] == True):
        new_mags.append(magnitudes[i])
        new_b_total.append(b_total[i])
        new_2_time.append(new_1_time[i])


plt.title('Ground Measurements With Respect to Time')
plt.plot(new_2_time,new_b_total)
plt.show()
plt.title('ACE Measurements With Respect to Time')
plt.plot(new_2_time,new_mags)
plt.show()
plt.title('Ground Measurements With Respect ACE measurments')
plt.plot(new_b_total,new_mags)
plt.show()


def func01(a,b,c,d):
    x=math.log(d/c)/(b-a)
    y=c*math.exp(-x*a)
    return [x,y]
def func1(x,y,l):
    d,ye=list(),list()
    for p in range(len(x)-1):
        for i in range(len(x)-1):
            if i!=p:
                if x[p]!=x[i]:
                    a,b=func01(x[p],x[i],y[p],y[i])[0],func01(x[p],x[i],y[p],y[i])[1]
                    for j in range(len(x)-1):
                        try:
                            ye.append(a*math.exp(b*x[p]))
                            d.append(abs(ye[j]-y[j]))
                        except:
                            ye.append(99999)
                            d.append(99999)
                else:
                    d.append(0)
        
        m=sum(d)/len(d)
        if m<l[2]:
            l=[a,b,m,'1']
    return l
def func02(a,b,c,d):
    x=(c-d)/math.log(a/b)
    y=math.exp(b/x)/a
    return [x,y]
def func2(x,y,l):
    for p in range(len(x)-1):
        for i in range(len(x)-1):
            if i!=p:
                try:
                    a,b,d,ye=func02(x[p],x[i],y[p],y[i])[0],func02(x[p],x[i],y[p],y[i])[1],list(),list()
                    for j in range(len(x)-1):
                        try:
                            ye.append(a*math.ln(b*x[p]))
                            d.append(abs(ye[j]-y[j]))
                        except:
                            ye.append(99999)
                            d.append(999999)
                except:
                    d.append(0)
        m=sum(d)/len(d)
        if m<l[2]:
            l=[a,b,m,'2']
    return l
def func03(a,b,c,d):
    y=math.log(c/d)/math.log(a/b)
    x=c/(a**y)
    return [x,y]
def func3(x,y,l):
    for p in range(len(x)-1):
        for i in range(len(x)-1):
            if i!=p:
                try:
                    a,b,d,ye=func03(x[p],x[i],y[p],y[i])[0],func03(x[p],x[i],y[p],y[i])[1],list(),list()
                    for j in range(len(x)-1):
                        try:
                            ye.append((a*(x[p]**b)))
                            d.append(abs(ye[j]-y[j]))
                        except:
                            ye.append(99999)
                            d.append(999999)
                except:
                    d.append(0)
            m=sum(d)/len(d)
            if m<l[2]:
                l=[a,b,m,'3']
    return l
def func04(a,b,c,d):
    y=math.exp(math.log(d/c)/(a-c))
    x=c/(y**a)
    return [x,y]
def func4(x,y,l):
    for p in range(len(x)-1):
         for i in range(len(x)-1):
            if i!=p:
              a,b,d,ye=func04(x[p],x[i],y[p],y[i])[0],func04(x[p],x[i],y[p],y[i])[1],list(),list()
              for j in range(len(x)-1):
                  try:
                      ye.append((a*(b**x[p])))
                      d.append(abs(ye[j]-y[j]))
                  except:
                      ye.append(99999)
                      d.append(999999)
              m=sum(d)/len(d)
              if m<l[2]:
                  l=[a,b,m,'4']
    return l
def func5(x,y,l):
    x = array(x)
    y = array(y)
    co=cov(x)
    M = array([x,y])
    variance= var(M, ddof=1, axis=0)
    a=co/variance
    for p in range(len(x)-1):
              b,ye,d,m=y[p]-a*x[p],list(),list(),9999
              for j in range(len(x)-1):
                if p!=j:
                  try:
                      ye.append((a*(b**x[p])))
                      d.append(abs(ye[j]-y[j]))
                  except:
                      ye.append(99999)
                      d.append(999999)
              m=sum(d)/len(d)
              if m<l[2]:
                  l=[a,b,m,'5']
    return l
'''importing the data from the database and stocking it in x and y'''
'''this is just a sample since we don't have time to sort out the data'''
x=[10,2,8,5,6,12,7]
y=[8,9,5,2,16,4,19]
l=['','',9999,'']
mes='''la fonction qu on peut utiliser pour prevenir l evenement qui Ã  pour variable d entrer 
la valeur lise par le satellite ace et pour variable do sortie existance si l aurora est visible
sinon inexistance'''
l=func1(new_mags,new_b_total,l)
l=func2(new_mags,new_b_total,l)
l=func3(new_mags,new_b_total,l)
l=func4(new_mags,new_b_total,l)
l=func5(new_mags,new_b_total,l)
'''function threshold that will take all the information from the database sort it into 2 groups 
1 for the ones with aurora and ones without using the images and compare the maximum of the graph without and 
the minimum of the one with aurora (approximations of course ) as well as take into account the energy reading 
and will determine the threshold based on that'''
magace=float(input())
#print(mes)
if l[3]=='1':
    res=l[0]*math.exp(l[1]*magace)-40
if l[3]=='2':
    res=l[0]*math.log(l[1]*magace)
if l[3]=='3':
    res=l[0]*(magace**l[1])
if l[3]=='4':
    res=l[0]*(l[1]*magace)
if l[3]=='5':
    res=l[0]*magace+l[1]
#print(res)
val=threshold(data1,data2)#data 1 and 2 are lists of lists 
#testexistance(res,val) val is the threshold
#this function will print existe if res>val
#and inxiste if val>res