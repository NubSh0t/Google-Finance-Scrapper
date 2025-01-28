from selenium import webdriver
import pyautogui
import time
import plotly.graph_objs as go
import pandas as pd

driver = webdriver.Chrome()

data=[]

driver.maximize_window()
driver.get("https://www.google.com/finance/quote/AAPL:NASDAQ?hl=en&window=1Y")

time.sleep(3)
x=350
pyautogui.moveTo(x,850)

b=True

while x<=1150 and b:
    try:
        value=driver.find_element("class name","hSGhwc-SeJRAd").get_attribute("innerHTML")
        d=driver.find_element("class name","hSGhwc-ZlY4af").get_attribute("innerHTML")
        s=value+str(", ")+d
        s=s.replace("USD $","")
        if s != ', ':
            s=s.split(",")
            s[0]=float(s[0])
            s[2]=s[2].replace('\u202f','')
            s[1]=s[1][1:]
            s[2]=s[2][1:]
            s[1]=s[1].replace(" ","-")+"-"+s.pop()
            data.append(s)
        x+=8
        pyautogui.moveTo(x,850)
    except:
        pass

    try:
        pyautogui.failSafeCheck()
    except:
        b=False

t=open("output.txt","w")
for d in data:
    t.write(str(d[0])+" "+str(d[1])+"\n")


df = pd.DataFrame(data, columns=['price', 'date'])

df['date'] = pd.to_datetime(df['date'], format='%b-%d-%Y')

fig = go.Figure()

fig.add_trace(go.Scatter(
x=df['date'],
y=df['price'],
fill='tozeroy',
mode='lines',
fillcolor='rgba(6, 182, 6, 0.5)', 
line=dict(color='#06b606')
))


fig.update_layout(
showlegend=False,
plot_bgcolor='white', 
paper_bgcolor='white', 
title=None,

xaxis=dict(
    showgrid=False, 
    showticklabels=False,  
    title=None,  
),
yaxis=dict(
    showgrid=False,  
    showticklabels=False,  
    title=None,    
),
margin=dict(l=60, r=60, t=60, b=60),
    

shapes=[
    dict(
        type="rect",
        xref="paper", yref="paper",
        x0=0, y0=0, x1=1, y1=1, 
        line=dict(color="black", width=2) 
    )
]
)


fig.show()