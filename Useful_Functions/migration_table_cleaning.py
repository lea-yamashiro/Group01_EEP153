# function assumes the inputted dataset already has columns named "Net Migration" and "Total Population"

def migration_cleaning(data1):
    
    # Make years ints instead of strings
    data1.reset_index(inplace=True)
    data1['date'] = data1['date'].astype(int)

    # index the table by country instead of year 
    data1.set_index(['country'],inplace=True)
    
    mig_table = data1[data1['Net Migration'] < 0] 
    #takes all negative values, we want migration AWAY
    
    mig_table['Net Migration'] = mig_table['Net Migration'].abs() 
    #takes absolute value to get magnitude rather than negative 
    
    mig_table['Migration per Capita'] = mig_table['Net Migration']/mig_table['Total Population'] 
    #creates new column, called 'Migration Per Capita'
    
    mig_table['Migration Rate (%)'] = mig_table['Migration per Capita']*100  
    #takes migration per capita and makes it a rate 

    return mig_table
