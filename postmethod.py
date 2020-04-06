import os
import pathlib
import requests
import flask
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

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
import argparse



FA ="https://use.fontawesome.com/releases/v5.8.1/css/all.css"
LOGO ="https://www.tirumala.org/NewImages/TTD-Logo.png"
LOGO1="https://www.tirumala.org/NewImages/HD-TXT.png"
#client = mqtt.Client()

#client.loop_start()
server = flask.Flask(__name__)

server.config['DEBUG'] = True

server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

server.secret_key = 'smarttrak'

db_URI = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
engine = create_engine(db_URI)

api = Api(server)
db = SQLAlchemy()

db.init_app(server)

def stamp1():
    return str(datetime.now())

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


@server.before_first_request
def create_tables():
    print("create table")
    db.create_all()

class DeviceModel(db.Model):
    __tablename__ = 'devices'

    print("Dev modelinit")
    stamp = db.Column(db.String(25),primary_key=True)
    devId = db.Column(db.String(15),primary_key=True)
    sun = db.Column(db.String(15))
    ta= db.Column(db.String(15))
    print("after table")
    #motor = db.Column(db.String(20))
        
    def __init__(self,stamp,devId,sun,ta):#,motor):
        print("init")
        stamp=stamp1()
        self.stamp = stamp
        self.devId = devId
        self.sun = sun

        self.ta = ta
        print("after init")
        #self.motor = motor
            
        def json(self):
            print("json")
            return {'stamp':self.stamp,'devId':self.devId,'sun':self.sun,'ta':self.ta}
    #'motor': self.motor}

    @classmethod
    def find_by_name(cls, stamp):
        print("find by name")
        x=cls.query.filter_by().first()
        print (x)
        return x

    def save_to_db(self):
        print("save to db")
        db.session.add(self)
        db.session.commit()
        print("after saving to db")

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class Device(Resource):

#    parser = argparse.ArgumentParser(description='Process some integers.')
    parser = reqparse.RequestParser()
    print("parser=",parser) 
    parser.add_argument('stamp',type=str)
    parser.add_argument('devId',type=str)
   
    parser.add_argument('sun',type=str)

    parser.add_argument('ta',type=str)

   #parser.add_argument('mode',type=str)
#    parser.add_argument('motor',type=str)
    #print("after parseing")
    def get(self):
        stamp=stamp1()
        device = DeviceModel.find_by_name(stamp)
        if device:
            return device.json()
        return {'message': 'Device not found'}, 404

    def post(self, message):
        
        #data={}    
        
        stamp=str(stamp1())
        
        x=message
        x.append(stamp)
        print("post-split=",x)
        
        data = Device.parser.parse_args()
        data['stamp']=str(stamp)
        
        data['devId']=str(x[1])
        data['sun']=str(x[4])
        data['ta']=str(x[7])
        #data1=data
        #data['motor']=x[6]

        device = DeviceModel.find_by_name(stamp)
        #print(data) 
        #device = DeviceModel(stamp,data1['devId'],data1['sun'],data1['ta'])#,data['motor'])#,data['bphvol'])
        print("device=",device) 

        if device is None:
            print("if block")

            #device = DeviceModel(stamp,x[0],x[2],x[4],x[6])
            device = DeviceModel(stamp,data['devId'],data['sun'],data['ta'])#,data['motor'])#,data['bphvol'])
            print("device=",device)
            print("if end")
        elif device is None and devId!=stamp:
            print("else if block")
            device = DeviceModel(stamp,data['devId'],data['sun'],data['ta'])#,data['motor'])#,data['bphvol'])

            print("device=",device)
            print("elif end")

        else:
            print("else block")
           # device = DeviceModel.find_by_name(stamp)
            device.devId= data['devId']
            device.stamp = data['stamp']
            device.sun = data['sun']
            device.ta = data['ta']
            #device.bphvol = data['bphvol']
            print("else end")
                       
        try:
            print("try")
            device.save_to_db()
            print("after try")       
        except:
            return {"message": "An error occurred inserting the device data."}, 500

        return device.json(), 201


class DeviceList(Resource):
    def get(self):
        x= {'devices': [x.json() for x in DeviceModel.query.all()]}
        return x
#cls =mqtt
#y=cls.MQTTMessage.payload

#print("y=",y)

def on_message(client, userdata, message):

    print ("on_message=",message)
    stamp=stamp1()
    cls=Device()
    x=message.payload.encode("utf-8")
    x=x.split()
    cls.post(x)

    if str(message.topic) != pubtop:
        print(str(message.topic), str(message.payload.decode("utf-8")))
    #return message


#def mqtt1():
newpid=os.fork()
stamp=stamp1()

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
client.connect("datastoragetest.herokuapp.com",1883)
client.connect("github.com",1883)
#client.connect("exmqtt.herokuapp.com",1883)
#client.connect("ec2-35-162-194-10.us-west-2.compute.amazonaws.com",1883)
#client.connect("iot.smarttrak.info",1883)
client.loop_start()
print("in loop")
def parent():
#     client.on_message = on_message

     client.subscribe(subtop)

def child():
  while True:
#    client.loop_start()
  
 #   client.on_message = on_message
    chat = input()
    client.publish(pubtop, chat)

if newpid == 0:
        # print("start child")
         child()
        # print("stop child")
else:
         #print("start parent")
         parent()
         #print("start parent")
         #pids = (os.getpid(), newpid)
        
#client.disconnect()
client.loop()


api.add_resource(Device, '/device/<string:devId>')
api.add_resource(DeviceList, '/devices')

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
        html.H4('Substation Data Live Feed'),
        html.Table(id="live-update-text"),],style={"overflowX":"scroll"}) 

app = dash.Dash(__name__,server=server,external_stylesheets=[dbc.themes.BOOTSTRAP, FA])

app.config['suppress_callback_exceptions']=True

def table(devices):
    #global reading
    #reading=reading+1
    table_header=[
        html.Thead(html.Tr([html.Th('time'),html.Th('devId'),html.Th('sun angle') ,html.Th('tracker angle')#, html.Th('motor status') ,
         ]))]
    table_body=[
        html.Tbody(html.Tr([html.Td(dev.stamp),html.Td(dev.devId),html.Td(dev.sun),html.Td(dev.ta)]))for dev in devices]
    table=dbc.Table(table_header+table_body,bordered=True,striped=True,hover=True,style={"backgroundColor":"white"})
    return table

"""def graph():
 #if df["devname"]=="dev_30":
  return dbc.Container([
                        html.H2("Graph"),
                        dcc.Graph(
       #  figure = go.Figure(go.Scatter(x = df['dateandtime'], y = df['rphvol'],)),
       #figure={"data": {"x":df["dateandtime"], "y": df["rphvol"]}}
                             figure={
                                'data': [
                                    {'x': df.tStamp, 'y':df.rphvol.where(df.devname=='dev_01'), 'name': 'rphvol'},
                                  #  {'x': df['tStamp'], 'y': df['yphvol'], 'z':df['devname'],  'name': 'yphvol'},
                                #    {'x': df['tStamp'], 'y': df['bphvol'], 'z':df['devname'],  'name': 'bphvol'},
                                   # {'x': df['tStamp'], 'y': df['avgvol'], 'type': 'bar', 'name': 'avgvol'}#if df['devId']  =="1",
                                   ],
            'layout': {
                'title': 'Voltage Visualization'
                }}
                        )])"""

#print("In between")
app.layout = html.Div([navbar,content,data1,buttons,dcc.Location(id="url",refresh=True)])
#@app1.route('/')
#def layout():
#    global x

@app.callback(
    dash.dependencies.Output('button1', 'children'),
    [dash.dependencies.Input('button1', 'n_clicks')])
def update_output(n_clicks):
    if client.publish(pubtop, "R1 Read:longitude"):
        return html.Div("longitude")

@app.callback(
    dash.dependencies.Output('button2', 'children'),
    [dash.dependencies.Input('button2', 'n_clicks')])
def update_output(n_clicks):
    if client.publish(pubtop, "R1 Read:latitude"):
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
        return html.Div("sun")
   
@app.callback(Output("live-update-text", "children"),
              [Input("live-update-text", "className")])

def update_output_div(input_value):
    devices = DeviceModel.query.all()
    return [html.Table(table(devices)
        )]
                      
@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],)

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

@app.callback([Output("page-content", "children")],
        [Input("url", "pathname")])

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
#def parent():
#     client.on_message = on_message

#client.subscribe(subtop)

#def child():
#  while True:
#    client.loop_start()

 #   client.on_message = on_message
"""chat = input()
client.publish(pubtop, chat)

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
client.loop()"""


#mqtt1()
print("global end")
if __name__=="__main__":
    print("main starts")
    app.run_server(debug=True,port=443)
    #mqtt1()
    #app1.run(debug=True)
    print("main end")
