
def migration_organizing(data1):
    
    ''' This function is used to clean the data, and in order to calculate per-capita statistics 
    we need specifically for isolating the high-migration population.'''
    
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


def setup_long(dataframe):
    
    ''' This function is a manual way of creating a dataframe that is usually performed by 
    a "group_by" function. The reason for this distinction is because we used the group_by
    function, but were really struggling to perform table-operations on the group_by frame, 
    as that function creates a special type of dataframe. This method was much faster.'''
    
    #percentiles = {'values': [50, 75, 80, 90]}
    unique_country_indices = dataframe.index.unique()

    if not unique_country_indices.empty:
        
        # Create an empty DataFrame with columns
        results = pd.DataFrame(columns=['Net Migration', 'Migration Rate (%)'])

        for country_index in unique_country_indices:
            country_data = dataframe.loc[country_index]
            mig_net_avg = country_data['Net Migration'].mean()
            mig_percap_avg = country_data['Migration Rate (%)'].mean()

            # Append the computed averages to the results DataFrame
            results.loc[country_index] = [mig_net_avg, mig_percap_avg]
        
        # calculate the percentiles for the migration rates 
        results['Percentile Rank'] = results['Migration Rate (%)'].apply(
            lambda x: stats.percentileofscore(results['Migration Rate (%)'], x))

        return results 



def population(year, sex, age_low, age_high, country_code):
    
    ''' This is the function that we use to retrieve population statistics, as outlined in the 
    [A] deliverables posted on Ed.'''
    
    # reconstruct the strings for population codes associated 
    # as entered in "age_low" and "age_high" arguments
    
    if sex == "Male":
        column_names = {"SP.POP." + str(age_low)+str(age_high) + ".MA": sex}
    elif sex == "Female":
        column_names = {"SP.POP." + str(age_low)+str(age_high) + ".FE": sex}
    
    # construct new dataframe for function to index, isolating 
    # the country by the function's country-code argument
    pop_stats = wbdata.get_dataframe(column_names, country = country_code)
    
    # filter the table by the function's year' argument
    
    pop_stats = pop_stats.filter(like=str(year), axis=0)
    # return population number by indexing the function-generated 
    # dataframe by the function's 'sex' argument, and making it an integer

    return int(pop_stats[sex].iloc[0])



def population_dataframe(year, country_code, pop_indicators):
    
    ''' This function retrieves a dataframe for specific year, country, and indicators selected. 
    The function assumes that the argument pop_indicators has already been defined with a 
    relevant WBData code dictionary.'''
        
    pop_df = wbdata.get_dataframe(pop_indicators, country = country_code)
    
    # filter the table by the function's year' argument
    
    pop_df = pop_df.filter(like=str(year), axis=0)
    
    # return population dataframe by indexing  
    # by the function's 'sex' argument

    return pop_df
