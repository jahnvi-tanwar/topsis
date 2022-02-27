import sys
import os 
import pathlib
import pandas as pd
import math
import numpy as np

# Lambda functions

den = lambda ser : math.sqrt(sum(ser*ser))

CLargs = sys.argv[1:]

#validate arguments
# print(len(CLargs))
# print(CLargs)
if len(CLargs) != 4 :
    raise Exception("Incorrect Number Of Parameters")

inputFilePath = CLargs[0]
weights_str = CLargs[1]
impacts_str = CLargs[2]
outputFile = CLargs[3] 

def validateString(filePath):
    val = filePath

    try:
        val = float(filePath)
    except:
        pass

    if type(val) != type('str'):
        raise Exception("Given argument is not a String")

def validatePath(filePath):
    if os.path.isfile(filePath) == False :
        raise Exception("File Not Found")

def validateFile(filePath):
    if pathlib.Path(filePath).suffix != ".csv" and pathlib.Path(filePath).suffix != ".xlsx":
        raise Exception("Not a csv or file")

def validateDatabase(dataframe):
    n = dataframe.shape[1]
    if n < 3:
        raise Exception("Input file must contain three or more columns.\n Given file has {} columns.".format(n))
    
    # print(type(dataframe[1]))

def validEntry(entry):

    if type(entry) == type('str'):
        entry = entry.strip()

    if entry == '-' or entry == 'X' or pd.isna(entry)==True or entry == 'NAN':
        return False
    else:
        return True

def matchCheck(colNo, weightl, impactl):

    # print(colNo)
    # print(weightl)
    # print(impactl)
    if colNo != weightl or colNo != impactl or impactl != weightl:
        raise Exception("Number of weights, number of impacts and number of columns (from 2nd to last columns) must be same")

def checkNumeric(df):

    columns = list(df)[1:]

    for col in columns:
        if not pd.api.types.is_integer_dtype(df[col].dtypes) and not pd.api.types.is_float_dtype(df[col].dtypes) :
            # print()
            raise Exception("From 2nd to last columns must contain numeric values only.")
    
    return True

def validateWeight(weights):

    for wt in weights:
        r_wt = wt.replace(".","",1)
        if wt.isnumeric() == False:
            raise Exception("weights must be separated by ','")

def validateImpact(impacts):

    # print(impacts)

    for imp in impacts:
        # print(imp)
        if imp!='-' and imp!='+':
            raise Exception("Impacts must be either +ve or -ve")

def euclidean(series,value):
    return math.sqrt(sum((series-value)**2))

def topsis(df,weights,impacts):
    columns = list(df)[1:]
    df_norm = pd.DataFrame()
    i = 0

    Vp = []
    Vn = []

    for col in columns:
        div = den(df[col])
        df_norm[col] = df[col].apply(lambda x: (x/div)*weights[i])

        if impacts[i] == '+':
            Vp.append(df_norm[col].max())
            Vn.append(df_norm[col].min())
        else:
            Vn.append(df_norm[col].max())
            Vp.append(df_norm[col].min()) 

        i+=1

    score = []
    
    for r in range(0,len(df_norm)):
        Sp = euclidean(df_norm.iloc[r,:],Vp)
        Sn = euclidean(df_norm.iloc[r,:],Vn)

        # print(Sp,Sn)


        sc = Sn/(Sp+Sn)
        score.append(sc)
    

    # print(score)


    # print(df_norm)

    # print(Vp)
    # print(Vn)

    score = np.array(score)
    indices = np.sort(score)

    df["P"] = score
    df["Score"] = (df['P'].rank(method='max', ascending=False))

validateString(inputFilePath)
validatePath(inputFilePath)
validateFile(inputFilePath)

df = pd.read_excel(inputFilePath)

validateDatabase(df)

weights = weights_str.split(",")
impacts = impacts_str.split(",")

validateWeight(weights)
validateImpact(impacts)

matchCheck(df.shape[1]-1,len(weights), len(impacts))
checkNumeric(df)

topsis(df,np.float_(weights),impacts)

# df.drop("Factor",axis=1,inplace=True)

df.to_csv(outputFile)
