import plotly.express as px
import yfinance as yf
import plotly.graph_objects as go
#Global time series chart for daily new cases, recovered, and deaths
df = yf.download('AAPL', start='2020-01-01', end='2021-05-21') #global time series data frame
print(df.index)
#fig = px.line(df, x=df.index, y=['High','Low', 'Close'], title='Global daily new cases' , template='ggplot2')

fig = go.Figure()
fig.update_layout(font_family="Rockwell")
fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines+markers', name='Preco'))
fig.update_xaxes(rangeslider_visible=True)
fig.show()