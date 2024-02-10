# for many WBdata population pyramids at once based on a single dataframe

def pyramid_all(yrstring):
    
    py.init_notebook_mode(connected=True)
    
    for code in codes: 
        
        pop_df = wbdata.get_dataframe(variables, country=[code])
        

        layout = go.Layout(barmode='overlay', title = countries_4plot[code] + ' Population, 2019',
                   width=600, height=600,
                   yaxis=go.layout.YAxis(range=[0, 90], title='Age'),
                   xaxis=go.layout.XAxis(title='Number'))

        bins = [go.Bar(x = pop_df.loc[yrstring,:].filter(regex="Male").values,
               y = [int(s[:2])+1 for s in age_ranges],
               orientation='h',
               name='Men',
               marker=dict(color='orange'),
               hoverinfo='skip'
               ),

               go.Bar(x = -pop_df.loc[yrstring,:].filter(regex="Female").values,
               y=[int(s[:2])+1 for s in age_ranges],
               orientation='h',
               name='Women',
               marker=dict(color='skyblue'),
               hoverinfo='skip',
               )]
        
        py.iplot(dict(data=bins, layout=layout))

# scatter a whole bunch of plots

def scatter_all(frame, dependent_variable, xrange = [int,int], yrange = [int,int]):
    columns = frame.columns
    for column in columns: 
        frame.iplot(kind='scatter', mode='markers', symbol='symboltype',
         y=dependent_variable,x=str(column), 
         text=frame.reset_index('qualitative_index')['qualitative_index'].values.tolist(), # for whatever is the qualitative index sorting by to be interactive
         yTitle=str(dependent_variable),xTitle=str(column), 
         categories= 'color_column', # column in dataframe you want things to be automatically color-coded by
         title= str(column)+' versus Migration Rate (%)')
