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



