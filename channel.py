import os
import pathlib
import requests
import flask
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import sqlite3
from flask import Flask, request,render_template
from flask_restful import Api
from flask_restful import Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
import dash_daq as daq
#from models import User
import paho.mqtt.client as mqtt
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, Response
from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
#import argparse
from datetime import timedelta
#import sqlite3

#import click
#from flask import current_app, g
#from flask.cli import with_appcontext


"""def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()"""
num=0

FA ="https://use.fontawesome.com/releases/v5.8.1/css/all.css"
LOGO ="https://www.tirumala.org/NewImages/TTD-Logo.png"
LOGO1="https://www.tirumala.org/NewImages/HD-TXT.png"
#client = mqtt.Client()

connection = sqlite3.connect('data.db',check_same_thread=False)

#client.loop_start()
server = flask.Flask(__name__)

server.config['DEBUG'] = True

#server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
#server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

server.secret_key = 'smarttrak'
#app = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite3')#
db = SQLAlchemy(server)
#db_URI = os.environ.get('DATABASE_URL', 'sqlite3:///data.db')
#engine = create_engine(db_URI)

api = Api(server)
#db = SQLAlchemy()

db.init_app(server)

#def stamp1():
#    return str(datetime.now())

def on_connect(client, userdata, flags, rc):
    print("Connected!", rc)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(granted_qos))

def on_unsubscribe(client, userdata, mid):
    print("Unsubscribed:", str(mid))

def on_publish(client, userdata, mid):
    print("Publish:", client)

def on_log(client, userdata, level, buf):
    print("log:", buf)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

#broker_address = "192.168.1.38"

#port =443 
#connection = sqlite3.connect('data.db',check_same_thread=False)
cursor = connection.cursor()
#if cursor.fetchall() is None:
#if cursor.fetchone()[0]!=1 :
connection.execute("CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT,stamp VARCHAR(15), devId VARCHAR(15), SPA VARCHAR(15),TA VARCHAR(15) )")

#cursor.execute("CREATE TABLE data (id INTEGER PRIMARY KEY AUTOINCREMENT,stamp VARCHAR(15), devId VARCHAR(15), SPA VARCHAR(15),TA VARCHAR(15) )")


#def text(data):
#    html.Div([html.H4("{}".format(data))])

#text={}
def on_message(client, userdata, message):
  #global num
  #global n
  #if num!=n:  
    print("on_message=",message)
    if str(message.topic) != pubtop:
        print(str(message.topic), str(message.payload.decode("utf-8")))
    payload = str(message.payload.decode("utf-8"))
    print("payload=",payload)
    data = dict(x.split(": ") for x in payload.split(" , "))
    x=["stamp"]
    y=[str(datetime.now()+ timedelta(minutes=330))]

#    y=[str(datetime.now())]
    print(x)
    print(y)
    print("len dict=",len(data))
    for columns,placeholders in data.items():
          x.append(columns)
          y.append(placeholders)
          print(x)
          print(y)
    print(data)
    if  len(data)>2:
        sql = "INSERT INTO data ('%s','%s','%s','%s') VALUES ('%s','%s','%s','%s')" % (x[0],x[1],x[2],x[3],y[0],y[1],y[2],y[3])

        try:
            print("try block")
            connection.execute(sql)
        except sqlite3.Error as error:
            print("Error: {}".format(error))
        connection.commit()
   # else:
 #       text.update(data)
  #      """{}""".format(text)
   #     print("text update",text)

  #num=num+1
  #n=num
  #print("num=",num)



#def mqtt1():
#newpid=os.fork()
#stamp=stamp1()

#def child():
client = mqtt.Client()
print("client=",client)

client.on_subscribe = on_subscribe 
client.on_unsubscribe = on_unsubscribe
client.on_connect = on_connect
client.on_message = on_message
time.sleep(1)

subtop="tracker/device/sub"
pubtop="tracker/device/pub"
#link=""
#if link!="":
#client.connect("ec2-35-162-194-10.us-west-2.compute.amazonaws.com",1883)
#client.connect("env-5116852.gpuoncloud.in",11002)
#client.connect("iot.smarttrak.info",1883)
client.username_pw_set("cbocdpsu", "3_UFu7oaad-8")
client.connect('soldier.cloudmqtt.com', 14035,60)
client.loop_start()
print("in loop")
#def parent():
#     client.on_message = on_message

client.subscribe(subtop)

#def child():
#    while True:
#    client.loop_start()
  
 #   client.on_message = on_message
#        chat = input()
#        client.publish(pubtop, chat)

#if newpid == 0:
        # print("start child")
#         child()
        # print("stop child")
#else:
         #print("start parent")
#         parent()
         #print("start parent")
         #pids = (os.getpid(), newpid)
        
#client.disconnect()
client.loop()


#api.add_resource(Device, '/device/<string:devId>')
#api.add_resource(DeviceList, '/devices')

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "15rem",
    "padding": "2rem 2rem",
    "fontSize":"30rem"
}

collapse = html.Div(
    [
        dbc.Button("Menu",id="collapse-button",className="mb-4",color="primary"),
        dbc.Container(dbc.Collapse(
            children=[dbc.DropdownMenu(nav=True,in_navbar=True,label="Substations",
            children=[
                dbc.DropdownMenu(nav=True,in_navbar=True,label="SUB 1",
                    children=[
                        dbc.DropdownMenuItem(dbc.NavLink("Dev 1",href="/Dev-1",id="dev-1")),dbc.DropdownMenuItem(divider=True),dbc.DropdownMenuItem(dbc.NavLink("Dev 2",href="/Dev-2",id="dev-2")),dbc.DropdownMenuItem(divider=True),
                            dbc.DropdownMenuItem(dbc.NavLink("Dev 3",href="/Dev-3",id="dev-3"))]),
                           dbc.DropdownMenu(nav=True,in_navbar=True,label="SUB 2",
                               children=[
                                   dbc.DropdownMenuItem(dbc.NavLink("SVM 1",href="/SVM-1",id="svm-1")),dbc.DropdownMenuItem(divider=True),dbc.DropdownMenuItem(dbc.NavLink("SVM 2",href="/SVM 2",id="svm-2")),dbc.DropdownMenuItem(divider=True),
                            dbc.DropdownMenuItem(dbc.NavLink("SVM 3",href="/SVM-3",id="svm-3"))])]),
                    dbc.DropdownMenu(nav=True,in_navbar=True,label="Streetlights",
                        children=[
                dbc.DropdownMenu(nav=True,in_navbar=True,label="SL 1",
                    children=[
                        dbc.DropdownMenuItem(dbc.NavLink("JEO 1",href="/jeo-1")),dbc.DropdownMenuItem(divider=True),dbc.DropdownMenuItem(dbc.NavLink("JEO 2",href="/jeo 2")),dbc.DropdownMenuItem(divider=True),
                            dbc.DropdownMenuItem(dbc.NavLink("JEO 3",href="/jeo 3"))]),
                           dbc.DropdownMenu(nav=True,in_navbar=True,label="SL 2",
                               children=[
                                   dbc.DropdownMenuItem(dbc.NavLink("SVSD 1",href="/SVSD-1")),dbc.DropdownMenuItem(divider=True),dbc.DropdownMenuItem(dbc.NavLink("SVSD 2",href="/SVSD 2")),dbc.DropdownMenuItem(divider=True)])])],                                                                  
                                
    id="collapse"),style={"backgroundColor":"grey","width":"auto"})])     

sidebar = html.Div(
        [
       dbc.Row(
            html.Img(src=LOGO,height="100px",width="auto"),style={"padding-left":0}),
                
            dbc.Nav(collapse, vertical=True)
  ] ,

style={
    "position": "absolute",
    "top": 0,
    "left":"2rem",
    "bottom": 0,
    "width": "12rem",
    "padding": "1rem 0rem",
    "backgroundColor":"light"},
     id="sidebar",
)

button =html.Div(
           dbc.Row(
              [
                  dbc.Col(dbc.Button("Login",color="primary",className="mb-3",href="#"),style={"padding-left":"20rem","width":"15rem"})]))
navbar = dbc.Navbar(
           html.Div(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.NavbarBrand(
                                html.H2((html.Img(src=LOGO1,height="60px",width="auto"))),style={"fontSize":"50px","padding-left":"10rem"})),
                        dbc.NavbarToggler(id="navbar-toggler"),
                         dbc.Collapse(sidebar,id="sidebar-collapse",navbar=True),
                         dbc.Collapse(button,id="button-collapse",navbar=True)
                        ],
                    align="center",
                    no_gutters=True,
                ),
             ),
          )

content = html.Div(id="page-content", style=CONTENT_STYLE)

buttons=html.Div([html.Button('longitude', id='button1'),html.Button('latitude', id='button2'),html.Button('rtc', id='button3'),html.Button('sun', id='button4')])


data1= html.Div([
        #html.H4('Substation Data Live Feed'),
        html.Table(id="live-update-text"),],style={"overflowX":"scroll"}) 

app = dash.Dash(__name__,server=server,external_stylesheets=[dbc.themes.BOOTSTRAP, FA])

app.config['suppress_callback_exceptions']=True

def table(devices):
    #global reading
    print("table devices=",devices)
    #reading=reading+1
    table_header=[
        html.Thead(html.Tr([html.Th('stamp'),html.Th('devId'),html.Th('sun angle') ,html.Th('tracker angle')#, html.Th('motor status') ,
         ]))]
    table_body=[
        html.Tbody(html.Tr([html.Td(dev[1]),html.Td(dev[2]),html.Td(dev[3]),html.Td(dev[4])]))for dev in devices]
    table=dbc.Table(table_header+table_body,bordered=True,striped=True,hover=True,style={"backgroundColor":"white"})
    return table

#df=pd.read_sql("select * from data",connection)

dropdowns=html.Div([
    html.H4('You can read the data from device using these dropdown buttons'),
    dcc.Dropdown(
        id='devices1',
        options=[
            {'label': 'R1', 'value': 'R1'},
            {'label': 'G2', 'value': 'G2'},
            {'label': 'R2', 'value': 'R2'}
        ],
        value='', style={"width":"auto"}),
    dcc.Dropdown(
        id='options1',
        options=[
            {'label': 'GETALL', 'value': 'GETALL'},
            {'label': 'LAT', 'value': 'LAT'},
            {'label': 'LONGITUDE', 'value': 'LONGITUDE'}, 
            {'label': 'RTC', 'value': 'RTC'},
            {'label': 'SUN', 'value': 'SUN'},
            {'label': 'TRACKER', 'value': 'TRACKER'},
            {'label': 'ZONE', 'value': 'ZONE'},
            {'label': 'MODE', 'value': 'MODE'},
            {'label': 'HR', 'value': 'HR'},
            {'label': 'MIN', 'value': 'MIN'},
            {'label': 'SEC', 'value': 'SEC'},
            {'label': 'DATE', 'value': 'DATE'},
            {'label': 'MONTH', 'value': 'MONTH'},
            {'label': 'YEAR', 'value': 'YEAR'},

        ],
        value='', style={"width":"auto"}),
    #inline=True,
    dbc.Button("Read", id="buttons1"),

html.Div(id='display')
])

graph=html.Div([
    dcc.Dropdown(
        id='devices',
        options=[
            {'label': 'R1', 'value': 'R1 '},
            {'label': 'G2', 'value': 'G2 '},
            {'label': 'R2', 'value': 'R2 '}
        ],
        value='R1 ', style={"width":"auto"}),
html.Div(id='dd-output-container')
    ,


 #style={"backgroundColor":"grey","width":"auto"},
    dcc.Graph(id='graph-with-slider'),
    dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
        ])

select=html.Div([
    html.H4('Using these you can write the commands for setting the values in the device'),
    dcc.Dropdown(
        id='device',
        options=[
            {'label': 'R1 ', 'value': 'R1'},
            {'label': 'G2 ', 'value': 'G2'},
            {'label': 'R2 ', 'value': 'R2'}
        ],
        value='',style={"width":"auto"}
    ),
    #html.H4(''),
    dcc.Dropdown(
        id='options',
        options=[
            {'label': 'LAT', 'value': 'LAT'},
            {'label': 'LONGITUDE', 'value': 'LONGITUDE'},
            {'label': 'SEC', 'value': 'SEC'},
            {'label': 'MIN', 'value': 'MIN'},
                        {'label': 'HOUR', 'value': 'HR'},
            {'label': 'DATE', 'value': 'DATE'},
            {'label': 'MONTH', 'value': 'MONTH'},
            {'label': 'YEAR', 'value': 'YEAR'},
            {'label': 'EAST', 'value': 'EAST'},
            {'label': 'WEST', 'value': 'WEST'},
            {'label': 'TIMEZONE', 'value': 'TIMEZONE'},
            {'label': 'REVLIMIT', 'value': 'REVLIMIT'},
            {'label': 'FWDLIMIT', 'value': 'FWDLIMIT'},
            {'label': 'AUTOMODE', 'value': 'AUTOMODE'},
            {'label': 'MANUALMODE', 'value': 'MANUALMODE'},
        ],
        value='',style={"width":"auto"}
    ),
   # html.Div(id='dd-output-container2'),
    dcc.Input(id="input2", type="text"),# placeholder="", debounce=True),
        html.Div(id="output"),
        dbc.Button("Write", id="write button"),
        ],#, className="mr-2")
)

form = dbc.Form([
    dcc.Dropdown(
        id='formdevice',
        options=[
            {'label': 'R1 ', 'value': 'R1'},
            {'label': 'G2 ', 'value': 'G2'},
            {'label': 'R2 ', 'value': 'R2'}
        ],
        value='',style={"width":"auto"}
    ),
        dcc.Dropdown(
        id='formoptions',
        options=[
            {'label': 'LAT', 'value': 'LAT'},
            {'label': 'LONGITUDE', 'value': 'LONGITUDE'},
            {'label': 'SUN', 'value': 'SUN'},
            {'label': 'RTC', 'value': 'RTC'},
                        {'label': 'TRACKER', 'value': 'TRACKER'},
            {'label': 'ZONE', 'value': 'ZONE'},
            {'label': 'MODE', 'value': 'MODE'},
            {'label': 'HR', 'value': 'HR'},
            {'label': 'MIN', 'value': 'MIN'},
            {'label': 'SEC', 'value': 'SEC'},
            {'label': 'DATE', 'value': 'DATE'},
            {'label': 'MONTH', 'value': 'MONTH'},
            {'label': 'YEAR', 'value': 'YEAR'},
        ],
        value='',style={"width":"auto"}
    ),
        dbc.FormGroup(
            [
#                dbc.Label("Enter value here", className="mr-2"),
                dbc.Input(type="text",id="input", placeholder="Enter value"),
            ],
            className="mr-3",
        ),
        dbc.Button("Write",id="form button", color="primary"),
    ],
    inline=True,
)

app.layout = html.Div([navbar,content,dropdowns,select,data1,graph,dcc.Location(id="url",refresh=True)])

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('devices', 'value')])#,Input('interval-component', 'n_intervals')])
def update_figure(selected_device):
    connection = sqlite3.connect('data.db')#,check_same_thread=False)
    df=pd.read_sql("select * from data",connection)

    filtered_df = df[df.devId == selected_device]
    print("filtered df=",filtered_df)

    return {
                                'data': [
                                    {'x': filtered_df.stamp, 'y':filtered_df.SPA
                                    #.where(df.devname=='dev_01')
                                    , 'name': 'SPA'},
                                    {'x': filtered_df.stamp, 'y':filtered_df.TA
                                                                  , 'name': 'TA'},

                                  #  {'x': df['tStamp'], 'y': df['yphvol'], 'z':df['devname'],  'name': 'yphvol'},
                                #    {'x': df['tStamp'], 'y': df['bphvol'], 'z':df['devname'],  'name': 'bphvol'},
                                   # {'x': df['tStamp'], 'y': df['avgvol'], 'type': 'bar', 'name': 'avgvol'}#if df['devId']  =="1",
                                   ],
            'layout': {
                'title': 'SPA and TA'
                }}
                    
@app.callback(
        Output('display', 'children'),
        [Input('devices1', 'value'),Input('options1', 'value'),Input('buttons1','n_clicks')])
def output(val1,val2,n):
    if n:
        client.publish(pubtop,"{} READ:{}".format(val1,val2))
        return "published for getting {}".format(val2)
@app.callback(
        Output('output', 'children'),
        [Input('device', 'value'),Input('options', 'value'),Input('input2','value'),Input('write button', 'n_clicks')])

def update_output(valueDEV,valueOP,value2,x):
    print("dev=",valueDEV,"options=",valueOP,"value=",value2)
    list1=["EAST","WEST","AUTOMODE","MANUALMODE","STOP"]
    if ((valueOP in list1) and (x is not None)):
        client.publish(pubtop,"{} WRITE:{}".format(valueDEV,valueOP))


        print("executing")
        return 'You have published "{} write {}"'.format(valueDEV,valueOP)

    elif((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:{}_{}".format(valueDEV,valueOP,value2))
    
  
        return 'You have published "{} {} write {}"'.format(valueDEV,valueOP,value2)

        

"""@app.callback(
    dash.dependencies.Output('button1', 'children'),
    [dash.dependencies.Input('button1', 'n_clicks')])
def update_output(n_clicks):
    if client.publish(pubtop, "R1 Read:longitude"):
        return html.Div("longitude")

@app.callback(
    dash.dependencies.Output('button2', 'children'),
    [dash.dependencies.Input('button2', 'n_clicks')])
def update_output(n_clicks):
    if client.publish(pubtop, "R1 Read:lat"):
        return html.Div("latitude")

@app.callback(
    dash.dependencies.Output('button3', 'children'),
    [dash.dependencies.Input('button3', 'n_clicks')])
def update_output(n_clicks):
    if client.publish(pubtop, "R1 Read:rtc"):
        return html.Div("rtc")

@app.callback(
    dash.dependencies.Output('button4', 'children'),
    [dash.dependencies.Input('button4', 'n_clicks')])
def update_output(n_clicks):
    if client.publish(pubtop, "R1 Read:sun"):
        return html.Div("sun")"""
   
@app.callback(Output("live-update-text", "children"),
              [Input("live-update-text", "className")])


def update_output_div(input_value):
    cursor.execute("SELECT * FROM data")

    rows = cursor.fetchall()
    print("rows=",rows)

    for row in rows:
        print("row=",row)
    #devices = DeviceModel.query.all()
    return [html.Table(table(rows)
        )]
                      
#@app.callback(
#    Output("collapse", "is_open"),
#    [Input("collapse-button", "n_clicks")],
#    [State("collapse", "is_open")],)

def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in range(1,4):
    @app.callback(
         Output("dev-{%d}"%i, "active"),
         [Input("url", "pathname")],
         )
    def toggle_active_links(pathname):
        if pathname == "/":
        # Treat page 1 as the homepage / index
            return True, False, False
        return [pathname == "/Dev-{%d}"%i]

#@app.callback([Output("page-content", "children")],
#        [Input("url", "pathname")])

def render_page_content(pathname):
    if pathname in ["/", "/Dev-1"]:
        return [
                html.H4("Displays Device 1 Graph")]

    elif pathname in ["/", "/Dev-2"]:
        return [
                html.H4("Displays Device 2 Graph")]

    elif pathname in ["/", "/Dev-3"]:
        return [
                html.H4("Displays Device 3 Graph")]
    
   # If the user tries to reach a different page, return a 404 message
    return [404]

print("global end")
connection.close()
if __name__=="__main__":
    print("main starts")
    app.run_server(debug=True,port=443)
    #mqtt1()
    #app1.run(debug=True)
    print("main end")
