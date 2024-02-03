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

''' This function is a manual way of creating a dataframe that is usually performed by 
    a "group_by" function. The reason for this distinction is because we used the group_by
    function, but were really struggling to perform table-operations on the group_by frame, 
    as that function creates a special type of dataframe. This method was much faster.'''

def setup_long(dataframe):
    
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
    
