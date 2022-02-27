# TOPSIS

TOPSIS is a method of compensatory aggregation that compares a set of alternatives by identifying weights for each criterion, normalising scores for each criterion and calculating the geometric distance between each alternative and the ideal alternative, which is the best score in each criterion.

# Function

    performTopsis(dataframe,weight,impact)
    
    Parameters:
        DataFrame : Pandas DataFrame on which TOPSIS is to be applied
        weight : python string, numeric values separated by comma
        impact : python string, + or - separated by comma

    Return Value:
        pandas DataFrame containing addition columns - TOPSIS score and TOPSIS rank
        
