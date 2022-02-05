import argparse
import subprocess
import time
import sys
import os
import json
#How can we save the running result of tracerout into txt files?
#Here is an example



#def parseArgument():
#ArgumentParse() and add_argument() are all build_in functions under argparse module
parser = argparse.ArgumentParser()
parser.add_argument("-n", help='Number of times traceroute will run',  dest = 'NUM_RUNS' , type=int, default=3)
parser.add_argument("-d", help='Number of seconds to wait between two consecutive runs',  dest = 'RUN_DELAY' , type=float,default=0.)
parser.add_argument("-m", help='Max number of hopes that traceroute will probe',  dest = 'MAX_HOPS' , default="20")
parser.add_argument("-o", help='Path and Name (without extension) of the .json output file', dest = 'OUTPUT', type=str)
parser.add_argument("-t", help='A target domain or IP address',  dest = 'TARGET', default="www.google.com")
parser.add_argument("--test", help='Directory containing num_runs text files, each of which contains the output of a traceroute run. If present, this will override all other options and traceroute will not be invoked. Statistics will be computed over the traceroute outp\
ut stored in the text files only.',  dest = 'TEST_DIR', nargs=1)

args = parser.parse_args()
    #return args


num_runs = args.NUM_RUNS
delay = args.RUN_DELAY
max_hops = args.MAX_HOPS
output_path = args.OUTPUT
target_host = args.TARGET
test_dir = args.TEST_DIR

count = 0
avgArray = [""] * int(max_hops)*3
hostslst = []
medtempPLus = []
hostslstplus = [""] * int(max_hops)*3
maxArray = [0] * int(max_hops)*3
minArray = [0] * int(max_hops)*3
medArray = [""] * int(max_hops)*3
finalmedArray = []

def layout():
           hosts()
           avg()
           min()
           max()
           med()
           text_file = open("output.json", "w")
           for i in range(int(max_hops)):
                      text_file.write('{\'avg\': ' + str(avgArray[i]) + "\n")
                      text_file.write('\'hop\': ' + str((1+i)) + "\n")
                      text_file.write('\'hosts\': [(' + str(hostslst[i]) + ')],\n')
                      text_file.write('\'max\': ' + str(maxArray[i]) + "\n")
                      text_file.write('\'med\': ' + str(finalmedArray[i]) + "\n")
                      if i  == int(max_hops)-1:
                          text_file.write('\'min\': ' + str(minArray[i]) + "}]\n")
                      else:
                        text_file.write('\'min\': ' + str(minArray[i]) + "\n")
           text_file.close()
def save_result_in_txt():
        test_folder = sys.path[0] + "/test_dir"

        if not os.path.exists(test_folder):
                   os.makedirs(test_folder)
        
        for i in range(num_runs):
            with open("test_dir" + "/run" +str(i), "w") as file_output:
                subprocess.Popen(["traceroute", "-m", str(max_hops), target_host], stdout = file_output, stderr=subprocess.STDOUT,)
            time.sleep(delay)
            file_output.close()

        #filename ='output.json'
        layout()
        #total = layout()
        #with open(filename, 'w') as f:
               #f.write(f'{total}')

def create_txt_and_json():
    total = layout()
    test_folder = sys.path[0] + "/test_dir"  
    
    if not os.path.exists(test_folder):   
        os.makedirs(test_folder)          

    for i in range(num_runs):
        filename = "test_dir" + "/" +str(i)
        with open(filename, "w") as file_output:
           subprocess.Popen(["traceroute", "-m", str(max_hops), target_host], stdout = file_output, stderr=subprocess.STDOUT,)
        time.sleep(delay)
        file_output.close()
            
    filename ='output.json' 
    with open(filename, 'w') as f:
               f.write(f'{total}')

def hosts():
        hop = 0
        substring = ")"
        hoststemp = hostslstplus

        for q in range(num_runs):
               filename ="test_dir" + "/run" +str(q)
               with open(filename, 'r') as f:
                          count = len(open(filename).readlines(  ))
                          while hop != 1:
                              data = f.readline().split()
                              if len(data) > 0:
                                  try:
                                     if not isinstance(data[0], int):
                                          hop = int(data[0])
                                  except ValueError:
                                     pass
                          for i in range(count):
                              for z in range(len(data)):
                                                    if substring in data[z]:
                                                        substringplus = data[z]
                                                        if len(hoststemp) > 0:
                                                           if substringplus not in hoststemp[hop-1]:
                                                               #hoststemp[hop-1] += " \'" + (data[z-1]) + "\', "
                                                               #hoststemp[hop-1] += '\'' + (data[z] + "\',")
                                                               hoststemp[hop-1] += "\'" + (data[z-1]) + "\', "
                                                               hoststemp[hop-1] += "\'" + (data[z]) + "\'"

                              data = f.readline().split()
                              if len(data) > 0:
                                             try:
                                                if not isinstance(data[0], int):
                                                     hop = int(data[0])
                                             except ValueError:
                                                pass
                              hostslstplus.append(hoststemp)

        #return hostslstplus
        for l in range(len(hostslstplus)):
            hostslst.append(hostslstplus[l])

        return hostslst

def med():
    medtemp = medArray
    medtemp1 = medArray
    hop = 0
    for q in range(num_runs):
           filename = "test_dir" + "/run" +str(q)
           with open(filename, 'r') as f:
                      count = len(open(filename).readlines(  ))
                      while hop != 1:
                          data = f.readline().split()
                          if len(data) > 0:
                              try:
                                 if not isinstance(data[0], int):
                                      hop = int(data[0])
                              except ValueError:
                                 pass
                      for i in range(count):
                                 temphop = hop
                                 floats = []
                                 for elem in data:
                                            if len(elem) > 2:
                                                       try:
                                                                  floats.append(float(elem))
                                                       except ValueError:
                                                                  pass
                                 for w in range(len(floats)):
                                     #medtempPLus.append(float(floats[w]))
                                 #print("medtemPLus:    " + str(medtempPLus))
                                     medtemp[hop-1] += " " + str(floats[w])
                                 data = f.readline().split()
                                 if len(data) > 0:
                                     try:
                                        if not isinstance(data[0], int):
                                             hop = int(data[0])
                                     except ValueError:
                                        pass
    for l in range(len(medtemp)):
        #medArray.append(medtemp[l])
        #medtemp[l].split()
        medtemp[l] = sorted(medtemp[l].split())

    #for e in range(len(medArray)):
        #medArray[e] = (medArray[e]).split()
        #medtemp[e] = medtemp[e].split(" ")
      #medtemp[p] = medtemp[p].sort()
    results = []
    medarrayResults = []
    for u in range(len(medArray)):
        t = 0
        l = 0.000
        if ((len(medArray[u]) % 2) == 0) & (len(medArray[u]) > 2):
            t = len(medArray[u]) // 2
            l += float(medArray[u][t-1])
            l += float(medArray[u][t])
            l = l / 2.000
        elif (len(medArray[u]) > 0):
            t = len(medArray[u])
            t = t / 2.00
            t = int(round(t))
            l += float(medArray[u][t-1])
        med = round(l, 3)
        finalmedArray.append(med)
        #medarrayResults[u] = [item[t] for item in medArray[u]]


    return finalmedArray

def max():
    tempArray = [0] * int(max_hops)
    tempArray2 = [0] * int(max_hops)
    temphop = 0
    hop = -1
    a = 0
    for q in range(num_runs):
           filename = "test_dir" + "/run" +str(q)
           with open(filename, 'r') as f:
                      count = len(open(filename).readlines(  ))
                      while hop != 1:
                          data = f.readline().split()
                          if len(data) > 0:
                              try:
                                 if not isinstance(data[0], int):
                                      hop = int(data[0])
                              except ValueError:
                                 pass
                      for i in range(count):
                                 temphop = hop
                                 floats = []
                                 for elem in data:
                                            if len(elem) > 2:
                                                       try:
                                                                  floats.append(float(elem))
                                                       except ValueError:
                                                                  pass

                                 for z in range(len(floats)):
                                           t= floats[0]
                                           if t <= floats[z]:
                                               t = floats[z]
                                               if maxArray[hop-1] <= t:
                                                maxArray[hop-1] = t
                                 data = f.readline().split()
                                 if len(data) > 0:
                                     try:
                                        if not isinstance(data[0], int):
                                             hop = int(data[0])
                                     except ValueError:
                                        pass

    return maxArray
def avg():
    tempArray = [0] * int(max_hops)
    tempArray2 = [0] * int(max_hops)
    temphop = 0
    hop = -1
    for q in range(num_runs):
           filename = "test_dir" + "/run" +str(q)
           count = len(open(filename).readlines(  ))
           with open(filename, 'r') as f:
                      while hop != 1:
                          data = f.readline().split()
                          if len(data) > 0:
                              try:
                                 if not isinstance(data[0], int):
                                      hop = int(data[0])
                              except ValueError:
                                 pass
                      i = 0
                      for i in range(count):
                                 t = 0
                                 z = 0
                                 if len(data) > 0:
                                     try:
                                        if not isinstance(data[0], int):
                                             hop = int(data[0])
                                     except ValueError:
                                        pass
                                 if temphop != hop:
                                     a = 0
                                 floats = []
                                 for elem in data:
                                            if len(elem) > 2:
                                                       try:
                                                                  floats.append(float(elem))
                                                       except ValueError:
                                                                  pass
                                 data = f.readline().split()
                                 for z in range(len(floats)):
                                           t+= floats[z]
                                           a += 1

                                 if (len(floats) > 0) & (temphop != hop):
                                    t = t / a
                                    h = round(t, 3)
                                    tempArray[hop-1] += h
                                    temphop = hop

    for t in range(int(max_hops)):
        m = tempArray[t] / num_runs
        n = round(m, 3)
        avgArray[t] =  n

    return(avgArray)

def min():
    tempArray = [0] * int(max_hops)
    tempArray2 = [0] * int(max_hops)
    temphop = 0
    hop = -1
    a = 0
    for q in range(num_runs):
           filename = "test_dir" + "/run" +str(q)
           with open(filename, 'r') as f:
                      count = len(open(filename).readlines(  ))
                      while hop != 1:
                          data = f.readline().split()
                          if len(data) > 0:
                              try:
                                 if not isinstance(data[0], int):
                                      hop = int(data[0])
                              except ValueError:
                                 pass
                      for i in range(count):
                                 temphop = hop
                                 floats = []
                                 for elem in data:
                                            if len(elem) > 2:
                                                       try:
                                                                  floats.append(float(elem))
                                                       except ValueError:
                                                                  pass

                                 for z in range(len(floats)):
                                           t = float(floats[0])
                                           if float(floats[z]) <= float(t):
                                               t = floats[z]
                                               if (minArray[hop-1] >= t):
                                                   minArray[hop-1] = t
                                               elif (minArray[hop-1] == 0):
                                                   minArray[hop-1] = t
                                 data = f.readline().split()
                                 if len(data) > 0:
                                     try:
                                        if not isinstance(data[0], int):
                                             hop = int(data[0])
                                     except ValueError:
                                        pass

    return minArray
if __name__ == '__main__':
           save_result_in_txt()
           #layout()
           #print(maxArray)
