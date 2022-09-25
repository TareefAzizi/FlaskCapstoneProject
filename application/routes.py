from application import app
from flask import render_template
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go


@app.route('/')
def index():
  df = pd.read_csv('application/static/unicornsSep2022.csv')
  vc = df['Industry'].value_counts()
  df_ref = df.loc[df['Industry'].isin(vc[vc == 1].index)]
  df_ref
  df.rename(lambda x: x.lower().strip().replace(' ', '_'), axis='columns', inplace=True)
  df.rename(columns = {'valuation_($b)':'valuation'}, inplace = True)
  df_ref.rename(lambda x: x.lower().strip().replace(' ', '_'), axis='columns', inplace=True)
  df.loc[df_ref.index, ['industry']] = df_ref[['city']].values
  df.loc[df_ref.index, ['city']] = df_ref[['investors']].values
  df.loc[df_ref.index, ['investors']] = df_ref[['industry']].values
  df.loc[df_ref.index]
  df['date_joined'] = df['date_joined'].astype('datetime64')
  df['valuation'] = df['valuation'].str.replace('$', '',regex=True)
  df['valuation'] = df['valuation'].astype(float)
  df = pd.concat([df, df['investors'].str.split(', ', expand=True)], axis=1)
  df.industry = df.industry.replace('Artificial Intelligence', 'Artificial intelligence')
  df.industry = df.industry.replace('Internet Software Services', 'Internet software & services')

  df = df.rename(columns =
               {0: 'Investor1',
                1: 'Investor2',
                2: 'Investor3',
                3: 'Investor4'})

  #GRAPH ONE
 
  fig1= px.treemap(df, path = ['country', 'industry'], values='valuation')
  fig1.update_layout(title='<b>Overview of Unicorns<b>',titlefont={'size': 24},template='plotly_dark')
  graph1JSON = json.dumps(fig1, cls= plotly.utils.PlotlyJSONEncoder)
  

  #Graph two 
  fig2 = px.bar(df, x='valuation',y='industry',color ='industry',hover_name='valuation',)
  fig2.update_layout(showlegend=False, yaxis_title='Industry',xaxis=dict(showline=True,showgrid=False,showticklabels=True,linecolor='rgb(204,204,204)',
                             tickfont=dict(family='Arial',size=12), ),
                             yaxis=dict(linecolor='rgb(150,150,150)',showline=True,showgrid=False),template = 'plotly_dark', title='<b>Industries with the highest valuation<b>')
  
  graph2JSON = json.dumps(fig2, cls= plotly.utils.PlotlyJSONEncoder)



  #graph three
  fig3 = px.ecdf(df, x="date_joined", color='industry', ecdfnorm=None)
  fig3.update_layout(showlegend=False,template= 'plotly_dark', title='<b>Yearly Listed Unicorn by Industry<b>',
                  titlefont={'size': 24})
  graph3JSON = json.dumps(fig3, cls= plotly.utils.PlotlyJSONEncoder)


  #graph four
  fig4 = px.bar(df, x='industry',color ='industry',hover_name='country',)
  fig4.update_layout(showlegend=False,yaxis_title='Number of Startups',xaxis=dict(showline=True,showgrid=False,showticklabels=True,linecolor='rgb(204,204,204)',
                             tickfont=dict(family='Arial',size=12)),
                             yaxis=dict(linecolor='rgb(150,150,150)',showline=True,showgrid=False),template = 'plotly_dark', title='<b>Amount of unicorn startups in an industry<b>')
  graph4JSON = json.dumps(fig4, cls= plotly.utils.PlotlyJSONEncoder)


  #graph five
  fig5 = px.histogram(df, x='date_joined',nbins = 15)
  fig5.update_layout(showlegend=False,yaxis_title='Number of Startups',xaxis=dict(showline=True,showgrid=False,showticklabels=True,linecolor='rgb(204,204,204)',
                             tickfont=dict(family='Arial',size=12)),
                             yaxis=dict(linecolor='rgb(150,150,150)',showline=True,showgrid=False),template = 'plotly_dark', title='<b>The Rise of Unicorn Startups<b>')
  graph5JSON = json.dumps(fig5, cls= plotly.utils.PlotlyJSONEncoder)
  #graph six
  fig6 = px.pie(df, values='valuation', names='country',
             title='Percentage of where Unicorn <br>Startups come from', template = 'plotly_dark',)
  fig6.update_layout(showlegend=False,titlefont={'size': 18} )
  fig6.update_traces(textposition='inside', textinfo='percent+label')
  graph6JSON = json.dumps(fig6, cls= plotly.utils.PlotlyJSONEncoder)


  #graph seven
  top5  = df.head(10)
  fig7= px.scatter_3d(top5, x='country', y='industry',z ='valuation',
              color='country')
  fig7.update_layout(showlegend=False,template = 'plotly_dark', title='<b>Top 10 unicorns in the world with the highest valuation<b>',titlefont={'size': 14} )
  graph7JSON = json.dumps(fig7, cls= plotly.utils.PlotlyJSONEncoder)


  #graph eight
  fig8 = px.ecdf(df, x="date_joined", color='country', ecdfnorm=None)
  fig8.update_layout(showlegend=False,template= 'plotly_dark', title='<b>Yearly Listed Unicorn by Country<b>',
                  titlefont={'size': 18} )
  graph8JSON = json.dumps(fig8, cls= plotly.utils.PlotlyJSONEncoder)

  #graph nine
  twentyCountry=df.head(45)

  fig9 = px.bar(twentyCountry, x='city', y='valuation')
  fig9.update_layout(showlegend=False,template = 'plotly_dark', title= "Cities with the highest amount of Unicorn Startups")
  graph9JSON = json.dumps(fig9, cls= plotly.utils.PlotlyJSONEncoder)

  #graph ten
  _= df.groupby(['industry']).valuation.sum().sort_values(ascending=False)
  industries = _.index

  def loop_i(c):
    r = []
    for i in industries:
        r.append(df['valuation'][df.country == c][df.industry == i].sum() )
        
    return r

  fig10 = go.Figure()

  for c in ['United States', 'China']:
    fig10.add_trace(go.Scatterpolar(
        r = loop_i(c),
#             [df['valuation'][df.country == c][df.industry == 'Artificial intelligence'].sum(),
#              df['valuation'][df.country == c][df.industry == 'Other'].sum(),
#              df['valuation'][df.country == c][df.industry == 'E-commerce & direct-to-consumer'].sum()
#             ],
        theta = industries,
        fill = 'toself',
        name = c
        ))

  fig10.update_layout(showlegend=False,title='<b>United States vs China<b>',
                  titlefont={'size': 24},
                  
                  template='plotly_dark',                  
#                   width=700,
#                   height=800
                 )

  graph10JSON = json.dumps(fig10, cls= plotly.utils.PlotlyJSONEncoder)

  return render_template('index.html', graph1JSON = graph1JSON, 
  graph2JSON=graph2JSON,
  graph3JSON = graph3JSON,
  graph4JSON = graph4JSON,
  graph5JSON = graph5JSON,
  graph6JSON = graph6JSON,
  graph7JSON = graph7JSON,
  graph8JSON = graph8JSON,
  graph9JSON = graph9JSON,
  graph10JSON = graph10JSON,)