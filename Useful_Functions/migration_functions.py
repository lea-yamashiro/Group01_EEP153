''' This function is used to clean the data, and in order to calculate per-capita statistics 
    we need specifically for isolating the high-migration population.'''

def migration_organizing(data1):
    
    # Make years ints instead of strings
    data1.reset_index(inplace=True)
    data1['date'] = data1['date'].astype(int)

    # index the table by country instead of year 
    data1.set_index(['country'],inplace=True)
    
    #takes all negative values, we want migration AWAY
    mig_table = data1[data1['Net Migration'] < 0] 
    
    #takes absolute value to get magnitude rather than negative
    mig_table['Net Migration'] = mig_table['Net Migration'].abs() 
    
    #creates new column, called 'Migration Per Capita'
    mig_table['Migration per Capita'] = mig_table['Net Migration']/mig_table['Total Population'] 
    
    #takes migration per capita and makes it a rate
    mig_table['Migration Rate (%)'] = mig_table['Migration per Capita']*100   
    
    # This line of code is initialized because we are interested in a population contingent 
    # on trends in the past ten years (rather than since '64). Additionally, we look at data 
    # from the ESG dataset, which only started being compiled in 2014'''
    mig_table = mig_table[mig_table['date'] > 2013] 

    return mig_table
