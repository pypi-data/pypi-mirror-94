# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 17:05:39 2020

@author: HEDI
"""

import sys 
import wx
import wx.grid as gridlib
import wx.adv
import uuid
import json
import os
import wx.html as html
from numpy import zeros,chararray,arange,array
import datetime
import matplotlib.pyplot as plt
from pymoo.model.problem import Problem
import autograd.numpy as anp
import os.path
from os import path
from numpy import reshape, zeros, dot,concatenate,column_stack,sum,mean
from cryptography.fernet import Fernet, InvalidToken
from numpy import array,append,cumsum,diff,multiply,polyfit,polyval,concatenate,unique,linspace,argmin,sort
from base64 import b64decode
from io import BytesIO
from json import JSONEncoder,JSONDecoder
import copy
import wx.lib.mixins.listctrl  as  listmix
from .wpinch_mono import __pinch__ as pinch1
import re
"""
"""
def formatting(val,d=0,unit=''):
    if unit:
        unit=" "+unit
    return ('{:.'+str(d)+'f}').format(val)+unit
def uuid_gen(uuids=[],n=8):
    def gen():
        return str(str(uuid.uuid1())[:n])
    s=gen()
    while s in uuids:
        s=gen()
    uuids.append(s)
    return s
def is_number(n):
    try:
        float(n)   # Type-casting the string to `float`.
                   # If string is not a valid `float`, 
                   # it'll raise `ValueError` exception
    except ValueError:
        return False
    return True
def str2num(val):
    if is_number(val):
        return float(val)
    return 0
class box_input(wx.TextCtrl):
    def __init__(self,parent,label,expand,**args):
            super().__init__(parent,**args)
            label_sbox = wx.StaticBox(parent, -1, label) 
            self.sizer = wx.StaticBoxSizer(label_sbox, wx.VERTICAL) 
            hbox = wx.BoxSizer(wx.HORIZONTAL,) 
            hbox.Add(self, expand, wx.EXPAND)
            self.sizer.Add(hbox, expand, wx.EXPAND)   
            
class box_lst(wx.ComboBox):
    def __init__(self,parent,label,**args):
        super().__init__(parent,**args)
        label_sbox = wx.StaticBox(parent, -1, label) 
        self.sizer = wx.StaticBoxSizer(label_sbox, wx.VERTICAL) 
        hbox = wx.BoxSizer(wx.HORIZONTAL,) 
        hbox.Add(self)
        self.sizer.Add(hbox) 
class box_check_lstct(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self,parent,label, *args, **kwargs):
        super().__init__(parent,*args, **kwargs)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        #self.setResizeColumn(0)
        label_sbox = wx.StaticBox(parent, -1, label) 
        self.sizer = wx.StaticBoxSizer(label_sbox, wx.VERTICAL) 
        hbox = wx.BoxSizer(wx.HORIZONTAL,) 
        hbox.Add(self)
        self.sizer.Add(hbox) 
class box_html(html.HtmlWindow):
    def __init__(self,parent,**args):
        super().__init__(parent,**args)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

class popup(wx.PopupWindow):
    def __init__(self, parent, ):
        """Constructor"""
        wx.PopupWindow.__init__(self, parent,wx.BORDER_SIMPLE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        htm = html.HtmlWindow(self,pos=(0,0))
        htm.SetHTMLBackgroundColour (wx.Colour(254, 249, 231))
        self.SetBackgroundColour(wx.Colour(254, 249, 231))
        self.SetSize( (240,180) )

        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

        htm.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        htm.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        htm.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        htm.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

        wx.CallAfter(self.Refresh)  
        sizer.Add(htm,1,wx.EXPAND,1)
        self.htm=htm
        self.SetSizer(sizer)
        self.Layout()


    def OnMouseLeftDown(self, evt):
        self.Refresh()
        self.ldPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
        self.wPos = self.ClientToScreen((0,0))
        self.CaptureMouse()

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            dPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
            nPos = (self.wPos.x + (dPos.x - self.ldPos.x),
                    self.wPos.y + (dPos.y - self.ldPos.y))
            self.Move(nPos)

    def OnMouseLeftUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()

    def OnRightUp(self, evt):
        self.Show(False)
        self.Destroy()
        
class sim_dyn_popup(wx.PopupWindow):
    def __init__(self, parent, key):
        """Constructor"""
        self.parent=parent
        self.key=key
        parent.sim_dyn[key]=self
        wx.PopupWindow.__init__(self, parent,wx.BORDER_SIMPLE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        htm = html.HtmlWindow(self,pos=(0,0))
        htm.SetHTMLBackgroundColour (wx.Colour(242, 243, 244))
        self.SetBackgroundColour(wx.Colour(254, 249, 231))
        self.SetSize( (240,180) )

        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

        htm.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        htm.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        htm.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        htm.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

        wx.CallAfter(self.Refresh)  
        sizer.Add(htm,1,wx.EXPAND,1)
        self.htm=htm
        self.SetSizer(sizer)
        self.Layout()


    def OnMouseLeftDown(self, evt):
        self.Refresh()
        self.ldPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
        self.wPos = self.ClientToScreen((0,0))
        self.CaptureMouse()

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            dPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
            nPos = (self.wPos.x + (dPos.x - self.ldPos.x),
                    self.wPos.y + (dPos.y - self.ldPos.y))
            self.Move(nPos)

    def OnMouseLeftUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()

    def OnRightUp(self, evt):
        self.Show(False)
        self.parent.sim_dyn[self.key]=None
        self.Destroy()
        
        
class EditableListCtrl(wx.ListCtrl, listmix.TextEditMixin):
    def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition,size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.TextEditMixin.__init__(self)
    
class obj__(object):
    def __init__(self, d):
            for a, b in d.items():
                if isinstance(b, (list, tuple)):
                    setattr(self, a, [obj__(x) if isinstance(x, dict) else x for x in b])
                else:
                    setattr(self, a, obj__(b) if isinstance(b, dict) else b)                
    def toJSON(self):
            return json.loads(json.dumps(self, default=lambda o: o.__dict__, ))
    def get(self,lst,k,val):
        return next(x for x in lst if getattr(x,k)== val)
    def toHTM(self,project,tp=''):
        if tp=='post':
            s="<html><body bgcolor=#FEF9E7><font size=1 face= 'courrier'>"
            s+="<center><b><font color=#707B7C >"+getattr(self,'name')+"</b></center>"
            loc=getattr(self,'loc')
            if loc:
                s+=self.get(project.data.loc,'id',loc).name
            s+='<br><br>'
            s+='<p4>Wastewater Treatment</p4><br>'
            s+="<table border=1 width=100%><thead><tr>"
            s+="<th>Pollutant</th><th>Removal ratio</th><th>Cout min</th><th>Workshop</th></tr>"
            for k in project.data.subs:
                s+='<tr>'+'<td><b><font color=#1E8449>'+k.name+"</b></font></td>"
                s+='<td>'+str(getattr(self.regen.R,k.id))+"</td>"
                s+='<td>'+str(getattr(self.regen.f,k.id))+"</td>"
                loc=getattr(self.regen.loc,k.id)
                if loc:
                    loc="<font color=#1B4F72>"+self.get(project.data.loc,'id',loc).name+"</font>"
                s+='<td>'+loc+"</td>"
                s+='</tr>'
            s+="</table>"
            s+="</font>"
            return s
        return ''

class var__(obj__):
    def __init__(self,main_frame,attr={}):
        super().__init__(copy.deepcopy(main_frame.config.var_schema.toJSON()))
        if attr:
            for k,v in attr.items():
                setattr(self,k,v)
        
class VarCellDialog(wx.Dialog):
    def __init__(self, parent,project,inventaire,var,var_type): 
        if not var.name:
            pass
            #var.name=inventaire.name.replace(" ","")+"_"+var_type
        super(VarCellDialog, self).__init__(parent, title = project.name+" >> "+inventaire.name+" >> "+var.name, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,size=(-1,-1)) 
        self.var=var
        self.project=project
        panel = wx.Panel(self) 
        sizer = wx.BoxSizer(wx.VERTICAL) 
        bd_sizer = wx.BoxSizer(wx.HORIZONTAL) 
        self.lb=box_input(panel,parent.main_frame.dict.lb.encode('cp1252'),0)
        self.ub=box_input(panel,parent.main_frame.dict.ub.encode('cp1252'),0)
        bd_sizer.Add(self.lb.sizer)
        bd_sizer.Add(self.ub.sizer)
        
        enable_sizer=wx.BoxSizer(wx.HORIZONTAL) 
        self.enable = wx.CheckBox(panel,-1,label=parent.main_frame.dict.enable)
        enable_sizer.Add(self.enable,0, wx.ALL|wx.CENTER)
        
        self.name=box_input(panel,"variable",0)
        
        for x in var.__dict__:
            if not x =='val':
                v=getattr(var,x)
                if not x=="enable":
                    v=str(v)
                getattr(self,x).SetValue(v)
        
          
        self.btn = wx.Button(panel, -1, label = "OK")
        self.btn.Bind(wx.EVT_BUTTON,self.OnOk) 
     
        sizer.Add(enable_sizer,0, wx.ALL|wx.CENTER,1)
        sizer.Add(bd_sizer)
        sizer.Add(self.name.sizer)
        sizer.Add(self.btn) 
        panel.SetSizer(sizer) 
        sizer.Fit(self)
        
       
    def OnOk(self,e):  
        for x in self.var.__dict__:
            if not x=="val":
                v=getattr(self,x).GetValue()
                setattr(self.var,x,v)
                
        self.project.save()
        self.Destroy()
                    
                    
                    
                    

class __project__:
    def __init__(self,main_frame,filename,dirname,data={}):
        self.filename=filename
        self.dirname=dirname
        self.main_frame=main_frame
        if not data:
            default_data=copy.deepcopy(main_frame.config.project_schema) # as obj
            default_data.id=uuid_gen()
            default_data.name=self.filename
            self.data=default_data
        else:
            self.data=obj__(data)
        
    def save(self):
        with open(os.path.join(self.dirname, self.filename), 'w') as fp:
             json.dump(self.data.toJSON(), fp) 
    @property
    def name(self):
        return self.data.name.replace('.json',"")
    @property
    def uuid(self):
        return self.data.id
    def get_cons(self,from_type,from_,to_type,to_):
        return next((x for x in self.data.cons if ','.join((x.from_type,x.from_,x.to_type,x.to_))==
                     ','.join((from_type,from_,to_type,to_))), None) 
    def cons_quick_balance(self,from_type,from_):
        # check available water/inventory phase
        m_max=0
        if from_type=='post':
            mc=[]
            cin_max=[]
            cout_max=[]
            m=[]
            for s in self.data.subs:
                mc.append(float(getattr(from_.subs,s.id)[0].val))
                cin_max.append(float(getattr(from_.subs,s.id)[1].val))
                cout_max.append(float(getattr(from_.subs,s.id)[2].val))
                m.append(1000*mc[-1]/(cout_max[-1]-cin_max[-1]+1e-16))
            m_max=max(m)
            # coolect all inputs:
            
        if from_type in ['source','sink']:
            m_max=from_.m.val
        return m_max
    def extract_data(self,subs):
        #print("pinch",subs.name,"===========================================")
        posts=[]
        sources=[]
        sinks=[]
        sensitivity_problem={}
        for i,p in enumerate(self.data.posts):
            mc,cin_max,cout_max=list(map(lambda x:x,getattr(p.subs,subs.id)))
            R = getattr(p.regen.R,subs.id)
            f = getattr(p.regen.f,subs.id)
            loc=p.loc
            if loc:
                loc = next(l for l in self.data.loc if l.id == loc).name
            loc_regen=getattr(p.regen.loc,subs.id)
            if loc_regen:
                loc_regen = next(l for l in self.data.loc if l.id == loc_regen).name
            posts.append({'name':p.name,'cin_max':cin_max.val,"cout_max":cout_max.val,"mc":mc.val,"loc":loc,
                          "regen":{"R":getattr(p.regen.R,subs.id).val,"f":getattr(p.regen.f,subs.id).val,"loc":loc_regen}})
            # sensitivity
            if cin_max.enable:
                sensitivity_problem["posts,"+str(i)+",cin_max"]={"bound":[float(cin_max.lb),float(cin_max.ub)],"name":cin_max.name}
            if cout_max.enable:
                sensitivity_problem["posts,"+str(i)+",cout_max"]={"bound":[float(cout_max.lb),float(cout_max.ub)],"name":cout_max.name}
            if R.enable:
                sensitivity_problem["regen,"+str(i)+",R"]={"bound":[float(R.lb),float(R.ub)],"name":R.name}
            if f.enable:
                sensitivity_problem["regen,"+str(i)+",f"]={"bound":[float(f.lb),float(f.ub)],"name":f.name}
        for s in self.data.sources:
            loc = s.loc
            if loc:
                loc = next(l for l in self.data.loc if l.id == loc).name
            sources.append({'name':s.name,'m':s.m.val,"c":getattr(s.subs,subs.id).val,"loc":loc})
        for s in self.data.sinks:
            loc = s.loc
            if loc:
                loc = next(l for l in self.data.loc if l.id == loc).name
            sinks.append({'name':s.name,'m':s.m.val,"cin_max":getattr(s.subs,subs.id).val,"loc":loc})
        
        return posts, sources,sinks,sensitivity_problem
    def sensitivity_analysis(self,subs,N):
        posts, sources,sinks,sensitivity_problem = self.extract_data(subs)
        pinch=pinch1(posts=posts,sources=sources,sinks=sinks,verbose=False)
        sensi = pinch.sensitivity_analysis(sensitivity_problem,N)
        htm = "<html>"
        htm+="<font color=#85929E>"+str(datetime.datetime.now())+"</font><br>"
        htm+="<b>Projet : </b> <font color=#2471A3>"+self.name+"</font>"
        htm+="<br><b>Analyse basée sur : </b> <font color=#58D68D>"+subs.name+"</font>"
        htm+="<table  border=1 width=100%><tr><th></th><th>Variable</th><th>Indice ordre 1</th><th>Indice Total</th></tr>"
        labels=[]
        for i,k in enumerate(sensi.problem['names']):
            inv,index,var = k.split(',')
            vars_={"cin_max":'Pollution entrée','cin_max':'Pollution sortie',"R":"Abattement","f":"Ratio traité"}
            if sensi.var_names[i]:
                var = sensi.var_names[i]
            else:
                var = vars_[var]
            if inv=='regen':
                inv=self.data.posts[int(index)]
            else:
                inv = getattr(self.data,inv)[int(index)]
            
            labels.append(inv.name+"\n"+var)
            htm+="<tr>"
            htm+="<td>"+inv.name+"</td>"
            htm+="<td>"+var+"</td>"
            # <font color=#D35400><b>["+var+"]</b></font>
            htm+="<td>"+str(sensi.Si_sobol["S1"][i]) +"</td>"
            htm+="<td>"+str(sensi.Si_sobol["ST"][i]) +"</td>"
            htm+="</tr>"
        htm+="</table>"
        htm+="<br><a href=sensi_bar,"+subs.id+">"+"graph"+"</a>"
        
        # plt.ioff()
        # fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
        # ax.bar(range(len(sensi.Si_sobol["S1"])),sensi.Si_sobol["S1"],)
        # ax.set_xticklabels(labels)
        # ax.set_xticks(range(len(sensi.Si_sobol["S1"])))
        # im_='tmp/sensi_bar_si.png'
        # fig.savefig(im_,dpi=1000)
        # htm+="<br>"
        # htm+='<img src='+im_+' width="400" height="400">'
        # plt.ion()
        
        setattr(self,"sensi",{"bar":{'labels':labels,"SI":sensi.Si_sobol["S1"],"ST":sensi.Si_sobol["ST"]}})
        
        return htm+"</html>"
        
        
    def sim_dyn(self):
        pinchs={}
        for s in self.data.subs:
            posts,sources,sinks = self.extract_data(s)
            pinch=pinch1(posts=posts,sources=sources,sinks=sinks,verbose=False)
            pinchs[s.id]=pinch
        htm="<html><center><b>"+self.name+"</b></center>"
        htm+="<table  border=1 width=80%><tr><th></th><th>min m<sup>3</sup>/h</th></tr>"
        for k,v in pinchs.items():
            s=next(p for p in self.data.subs if p.id == k)
            htm+="<tr>"
            htm+="<td><font color=#27AE60><b>"+s.name+"</b></font></td><td>"+formatting(v.cascade.fw,d=2)+"</td>"            
            htm+="</tr>"
        htm+="</table>"
        htm+="</html>"
        return htm
    def pinch(self):
        res={"html":"result","pinchs":{}}
        pinchs={}
        for s in self.data.subs:
            posts,sources,sinks,sensi_prob = self.extract_data(s)
            pinch=pinch1(posts=posts,sources=sources,sinks=sinks,verbose=False)
            pinchs[s.id]=pinch
        res["pinchs"]=pinchs
        
        head = "<html>"
        head+="<font color=#85929E>"+str(datetime.datetime.now())+"</font><br>"
        head+="<b>Projet:</b> <font color=#2471A3>"+self.name+"</font>"
        
        composites=["C=f(m<sub>C</sub>)","m<sub>C</sub>=f(m<sub>eau</sub>)"]
        htm=head
        htm+="<h3>Résultat de minimisation par polluant</h3>"
        htm+="<table  border=1 width=80%><tr><th></th><th>min m<sup>3</sup>/h</th><th>"+composites[0]+"</th><th>"+composites[1]+"</th><th>Réseau d'eau</th></tr>"
        
        for k,v in pinchs.items():
            s=next(p for p in self.data.subs if p.id == k)
            htm+="<tr>"
            htm+="<td><font color=#27AE60><b>"+s.name+"</b></font></td><td>"+formatting(v.cascade.fw,d=2)+"</td>"
            htm+="<td><a href=plot_composite1,"+k+">"+"graph"+"</a></td>"
            htm+="<td><a href=plot_composite2,"+k+">"+"graph"+"</a></td>"
            htm+="<td><a href=networkpng,"+k+">"+"png"+"</a> <a href=networkpdf,"+k+">"+"pdf"+"</a></td>"
            
            htm+="</tr>"
        htm+="</table>"
        
        # for k,v in pinchs.items():
        #     s=next(p for p in self.data.subs if p.id == k)
        #     htm+="<h3>Cascade eau, <font color=#27AE60><b>"+s.name+"</b></h3><br>"
        #     htm+=v.cascade.to_html().replace("<table>","<table border=1>").replace("{",'<font bgcolor=#0FC8F1>').replace("}","</font>")
        
        htm+="<br>"
        i=0
        pbalance={}
        ppollution={}
        for k,v in pinchs.items():
            i+=1
            pbalance[k]=[]
            ppollution[k]=[]
            s=next(p for p in self.data.subs if p.id == k)
            htm+="<br><b>"+str(i)+". <font bgcolor=#D6EAF8>"+"Analyse, <font color=#27AE60>"+s.name+"</font></b><br><br>"
            htm+="<b>"+str(i)+".1 Bilan</b><br>"
            htm+="<ul>"
            for i,post in enumerate(v.posts):
                htm+='<li>'+post.name +' : ' +'<a href=balancepost'+str(i)+','+k+'>eau</a>, '+'<a href=pollpost'+str(i)+','+k+'>pollution</a>, '+"</li>"
                pb = head
                ppoll=head
                pb+="<br><a href=main,>Retour</a></html><br><br>"
                ppoll+="<br><a href=main,>Retour</a></html><br><br>"
                pb+="<b>Analyse, <font color=#27AE60>"+s.name+"</font>, Bilan eau, "+post.name+"</b><br><br>"
                ppoll+="<b>Analyse, <font color=#27AE60>"+s.name+"</font>, Transfert de pollution, "+post.name+"</b><br><br>"
                pb1,pb2,poll = post.html_balances()
                pb+="<font bgcolor=#5DADE2>Inputs</font><br>"+pb1+"<br><br>"
                pb+="<font bgcolor=#5DADE2>Outputs</font><br>"+pb2
                pb+="<br><br><a href=main,>Retour</a></html>"
                ppoll+=poll
                ppoll+="<br><br><a href=main,>Retour</a></html>"
                pbalance[k].append(pb)
                ppollution[k].append(ppoll)
            htm+="</ul>"
            
            htm+="<b>"+str(i)+".2 "+"Cascade eau : </b>"+"<a href=cascade1,"+k+">faisable</a>"+", <a href=cascade0,"+k+">non faisable</a>"+"<br>"
        
        cascade1={}
        cascade0={}
        
        for k,v in pinchs.items():   
            s=next(p for p in self.data.subs if p.id == k)
            cascade1[k] = head
            cascade1[k]+="<br><a href=main,>Retour</a></html><br><br>"
            cascade1[k]+="<b>Analyse, <font color=#27AE60>"+s.name+"</font>, Cascade faisable</b><br><br>"
            cascade1[k]+=v.cascade.to_html().replace("<table>","<table border=1>").replace("{",'<font bgcolor=#0FC8F1>').replace("}","</font>")
            cascade1[k]+="<br><br><a href=main,>Retour</a></html>"
            
            cascade0[k] = head
            cascade0[k]+="<br><a href=main,>Retour</a></html><br><br>"
            cascade0[k]+="<b>Analyse, <font color=#27AE60>"+s.name+"</font>, Cascade non faisable</b><br><br>"
            cascade0[k]+=v.cascade.to_html(feasible=False).replace("<table>","<table border=1>").replace("{",'<font bgcolor=#0FC8F1>').replace("}","</font>")
            cascade0[k]+="<br><br><a href=main,>Retour</a></html>"   
            
            
 
        
        res["html"]={"main":htm,"cascade1":cascade1,"cascade0":cascade0,"pbalance":pbalance,'ppollution':ppollution}
        
        setattr(self,"mono",res)
            
        
        
"""
"""
"""
    PROJECT TREE
"""
class ProjetTree( wx.ScrolledWindow):
    def __init__(self,parent,main_frame):
        super().__init__(parent)
        self.tree = wx.TreeCtrl(self,  wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                style=wx.TR_DEFAULT_STYLE | wx.TR_EDIT_LABELS) 
        
        self.main_frame=main_frame
        image_list = wx.ImageList(24,24)
        self.tree.AssignImageList(image_list)
        fldridx = image_list.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (24,24)))
        fldropenidx = image_list.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, (24,24)))
        #     sys.exec_prefix
        im1 = os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim", self.main_frame.icons.project_tree)
        self.icon1 = image_list.Add(wx.Image(im1, wx.BITMAP_TYPE_PNG).Scale(24,24).ConvertToBitmap())

        self.tree.SetBackgroundColour(wx.Colour(214, 234, 248 ))
        
        
        self.root = self.tree.AddRoot(self.main_frame.dict.root) 
        self.tree.SetItemImage(self.root, fldridx,wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.root, fldropenidx,wx.TreeItemIcon_Expanded)
        tree_sizer = wx.BoxSizer()
        tree_sizer.Add(self.tree,-1, wx.EXPAND,-1) 
        self.SetSizer(tree_sizer)         
        self.tree.Expand(self.root)
        
        # bind
        self.tree.Bind(wx.EVT_TREE_ITEM_MENU,self.OnPopup)
    def OnPopup(self,e):
        item = e.GetItem()
        data = self.tree.GetItemData(item)
        if isinstance(data,__project__):
            class PopMenu(wx.Menu): 
                def __init__(self, parent): 
                    super(PopMenu, self).__init__() 
                    self.parent = parent 
                    # menu item 1 
                    pcopy = wx.MenuItem(self, -1, parent.main_frame.dict.copy) 
                    self.Append(pcopy) 
                    # menu item 2 
                    rmv = wx.MenuItem(self, -1, parent.main_frame.dict.rmv) 
                    self.Append(rmv) 
                    # bind
                    self.Bind(wx.EVT_MENU,self.OnCopy,pcopy)
                    self.Bind(wx.EVT_MENU,self.OnRMV,rmv)
                def OnCopy(self,e):
                    dlg = wx.FileDialog(self.parent.main_frame, self.parent.main_frame.dict.save_as, os.getcwd(), "", "*.json", \
                    wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
                    dlg.SetSize((100,100)) 
                    if dlg.ShowModal() == wx.ID_OK:
                        filename = dlg.GetFilename()
                        dirname = dlg.GetDirectory()
                        if not (filename,dirname) in list(map(lambda x:(x.filename,x.dirname),self.parent.main_frame.projects.values())):
                            project=__project__(self,filename,dirname,data.data.toJSON())
                            project.data.name=project.filename
                            project.id=uuid_gen()
                            self.parent.main_frame.projects[project.uuid]=project
                            self.parent.main_frame.project_tree.AppendItem(project.name,data=project,) 
                            project.save()
                    dlg.Destroy()
                def OnRMV(self,e):
                    self.parent.tree.Delete(item)
                    del self.parent.main_frame.projects[data.uuid]
                        
            self.PopupMenu(PopMenu(self,)) 
            
      
    def AppendItem(self,name,data):
        item = self.tree.AppendItem(self.root, name,data=data) 
        self.tree.SetItemImage(item, self.icon1, wx.TreeItemIcon_Normal)
        self.tree.SelectItem(item)
        self.tree.Expand(self.root) 
"""
    END PROJECT TREE
"""


"""
 TABS                  ***************** TABS *********************
"""
#    ======================= SUBS ============================================
class subs_grid(gridlib.Grid):
    def __init__(self, parent,main_frame):
        self.main_frame=main_frame
        self.sel=[]
        self.fonts=[wx.Font(14, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,  wx.FONTWEIGHT_BOLD, underline=False,faceName="", encoding=wx.FONTENCODING_DEFAULT),
                    wx.Font(14, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,  wx.FONTWEIGHT_NORMAL, underline=False,faceName="", encoding=wx.FONTENCODING_DEFAULT)]
        self.default_name_color=wx.Colour(40, 180, 99)
        self.err_name_color=wx.Colour(231, 76, 60)
        gridlib.Grid.__init__(self, parent,) 
        self.CreateGrid(0,len(main_frame.dict.subs_cols))
        for i,c in enumerate(main_frame.dict.subs_cols):
           self.SetColLabelValue(i, c)
        for i in [0,1,4]:
            self.HideCol(i)

        self.AutoSize()
            # Grid
        self.EnableEditing( True )
        self.EnableGridLines( True )
        self.SetGridLineColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
        self.EnableDragGridSize( True )
        self.SetMargins( 0, 0 )
                # Columns
        self.EnableDragColMove( False )
        self.EnableDragColSize( True )
        self.SetColLabelSize( 20 )
        self.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        self.SetColSize(2,200)
        self.SetColSize(3,200)

        # Rows
        self.EnableDragRowSize( True )
        self.SetRowLabelSize(20 )
        self.SetRowLabelAlignment( wx.ALIGN_LEFT, wx.ALIGN_LEFT )
        
        # self.GetGridWindow().Bind(wx.EVT_MOTION, self.onMouseOver)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.onCellChanged)
        self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.onSingleSelect)           
        
    def onSingleSelect(self, event):
        self.sel = [event.GetRow(),event.GetCol()]
        event.Skip()
    def onCellChanged(self,e):
            self.Parent.update_data()
    def add_row(self,i,row):
        for j,r in enumerate(row):
            self.SetCellValue ( i, j, r)
            self.SetRowSize(i, 25)
        self.SetCellTextColour(i,2, self.default_name_color)
        self.SetCellFont(i ,2, self.fonts[0])
        self.SetCellFont(i ,3, self.fonts[1])
        self.SetCellValue ( i, 4, self.GetCellValue ( i, 2)) # save tmp
class subs_tab(wx.ScrolledWindow):
        def __init__(self, parent,main_frame):
            self.main_frame=main_frame
            super().__init__(parent)
            self.SetScrollbars(20, 20, 50, 50)
            add_btn = wx.BitmapButton(self , 0,bitmap=wx.Bitmap(os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",self.main_frame.icons.add), wx.BITMAP_TYPE_ANY))
            rmv_btn = wx.BitmapButton(self , 1,bitmap=wx.Bitmap(os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",self.main_frame.icons.rmv), wx.BITMAP_TYPE_ANY))
            sizer = wx.BoxSizer(wx.VERTICAL)
            btn_sizer = wx.BoxSizer(wx.HORIZONTAL) 
            btn_sizer.Add(add_btn,) 
            btn_sizer.Add(rmv_btn,) 
            sizer.Add(btn_sizer ,) 
            
            self.grid=subs_grid(self,main_frame)
            sizer.Add(self.grid, 1, flag=wx.EXPAND) 
            
            add_btn.Bind(wx.EVT_BUTTON,self.OnAdd)
            rmv_btn.Bind(wx.EVT_BUTTON,self.OnSupp)    
            
            self.SetSizer(sizer) 
        
        def update(self,project=None):
            if project:
                self.update()
                for i,s in enumerate(project.data.subs):
                    self.grid.AppendRows(numRows=1)
                    row=[]
                    for k in self.main_frame.config.subs_schema.__dict__:
                        row.append(getattr(s,k))
                    self.grid.add_row(i,row)
                
            else:
                if self.grid.GetNumberRows()>0:
                    self.grid.DeleteRows(numRows=self.grid.GetNumberRows())
            
        def OnAdd(self,e):
            project = self.main_frame.get_selected_project()
            if project:
              n=self.grid.GetNumberRows()
              self.grid.AppendRows(1) 
              self.grid.add_row(n,[project.uuid,'_'+uuid_gen()])
              self.Layout()
              self.Parent.Layout()
              
        def OnSupp(self, event):
            if self.grid.GetNumberRows()>0 and self.grid.sel:
                project=self.main_frame.projects[self.grid.GetCellValue( self.grid.sel[0], 0)]
                dlg = wx.MessageDialog(None, self.main_frame.dict.supp_req+" '"+self.grid.GetCellValue( self.grid.sel[0], 2)+"'?",project.name ,wx.YES_NO | wx.ICON_QUESTION)
                result = dlg.ShowModal()
                if result == wx.ID_YES:
                   self.grid.DeleteRows( pos=self.grid.sel[0], numRows=1)
                   # self.Fit()
                   self.update_data()
               
               
               
        def update_data(self):
            subs=[]
            for i in range(self.grid.GetNumberRows()):
                if self.grid.GetCellValue(i,2):
                    s={}
                    for j,k in enumerate(self.main_frame.config.subs_schema.__dict__):
                        s[k]=self.grid.GetCellValue(i,j)
                    subs.append(obj__(s))
                    
                if not self.grid.GetCellValue(i,2) and self.grid.GetCellValue(i,4):
                    for j,k in enumerate(self.main_frame.config.subs_schema.__dict__):
                        if j==2:
                            s[k]=self.grid.GetCellValue(i,4)
                        else:
                            s[k]=self.grid.GetCellValue(i,j)
                    subs.append(obj__(s))
                   
            # update
            if subs:
                project=self.main_frame.projects[self.grid.GetCellValue(0,0)]
                old_ids=list(map(lambda x:x.id,project.data.subs))
                new_ids=list(map(lambda x:x.id,subs))
                for c in new_ids:
                    if not c in old_ids:
                        for p in project.data.posts:
                            setattr(p.subs,c,[var__(self.main_frame),var__(self.main_frame),var__(self.main_frame)])
                            setattr(p.regen.loc,c,'')
                            setattr(p.regen.R,c,var__(self.main_frame))
                            setattr(p.regen.f,c,var__(self.main_frame))
                        for s in project.data.sources:
                            setattr(s.subs,c,var__(self.main_frame))
                        for s in project.data.sinks:
                            setattr(s.subs,c,var__(self.main_frame))
                for c in old_ids:
                     if not c in new_ids:
                        for p in project.data.posts:
                            delattr(p.subs,c)
                            delattr(p.regen.loc,c)
                            delattr(p.regen.R,c)
                            delattr(p.regen.f,c)
                        for s in project.data.sources:
                            delattr(s.subs,c)
                        for s in project.data.sinks:
                            delattr(s.subs,c)
                if subs: 
                    project.data.subs=subs
                    project.save()
# ============================================================================
#      LOC TAB =============================================================
# ============================================================================
class loc_grid(gridlib.Grid):
    def __init__(self, parent,main_frame):
        self.main_frame=main_frame
        self.sel=[]
        self.fonts=[wx.Font(14, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,  wx.FONTWEIGHT_BOLD, underline=False,faceName="", encoding=wx.FONTENCODING_DEFAULT),
                    wx.Font(14, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,  wx.FONTWEIGHT_NORMAL, underline=False,faceName="", encoding=wx.FONTENCODING_DEFAULT)]
        self.default_name_color=wx.Colour(46, 134, 193) #" blue"
        self.err_name_color=wx.Colour(231, 76, 60)
        gridlib.Grid.__init__(self, parent,) 
        self.CreateGrid(0,len(main_frame.dict.loc_cols))
        for i,c in enumerate(main_frame.dict.loc_cols):
           self.SetColLabelValue(i, c)
        for i in [0,1,4]:
            self.HideCol(i)

        self.AutoSize()
            # Grid
        self.EnableEditing( True )
        self.EnableGridLines( True )
        self.SetGridLineColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
        self.EnableDragGridSize( True )
        self.SetMargins( 0, 0 )
                # Columns
        self.EnableDragColMove( False )
        self.EnableDragColSize( True )
        self.SetColLabelSize( 20 )
        self.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        self.SetColSize(2,200)
        self.SetColSize(3,200)

        # Rows
        self.EnableDragRowSize( True )
        self.SetRowLabelSize(20 )
        self.SetRowLabelAlignment( wx.ALIGN_LEFT, wx.ALIGN_LEFT )
        
        # self.GetGridWindow().Bind(wx.EVT_MOTION, self.onMouseOver)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.onCellChanged)
        self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.onSingleSelect)           
        
    def onSingleSelect(self, event):
        self.sel = [event.GetRow(),event.GetCol()]
        event.Skip()
    def onCellChanged(self,e):
            project=self.main_frame.projects[self.GetCellValue(0,0)]
            self.Parent.update_data(project)
    def add_row(self,i,row):
        for j,r in enumerate(row):
            self.SetCellValue ( i, j, r)
            self.SetRowSize(i, 25)
        self.SetCellTextColour(i,2, self.default_name_color)
        self.SetCellFont(i ,2, self.fonts[0])
        self.SetCellFont(i ,3, self.fonts[1])
        self.SetCellValue ( i, 4, self.GetCellValue ( i, 2)) # save tmp                    
class loc_tab(wx.ScrolledWindow):
        def __init__(self, parent,main_frame):
            self.main_frame=main_frame
            super().__init__(parent)
            self.SetScrollbars(20, 20, 50, 50)
            #add_btn = wx.Button(self , 0, "+")
            #rmv_btn = wx.Button(self , 0, "-")
            add_btn = wx.BitmapButton(self , 0,bitmap=wx.Bitmap(os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",self.main_frame.icons.add), wx.BITMAP_TYPE_ANY))
            rmv_btn = wx.BitmapButton(self , 1,bitmap=wx.Bitmap(os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",self.main_frame.icons.rmv), wx.BITMAP_TYPE_ANY))
            sizer = wx.BoxSizer(wx.VERTICAL)
            btn_sizer = wx.BoxSizer(wx.HORIZONTAL) 
            btn_sizer.Add(add_btn,) 
            btn_sizer.Add(rmv_btn,) 
            sizer.Add(btn_sizer ,) 
            
            self.grid=loc_grid(self,main_frame)
            sizer.Add(self.grid, 1, flag=wx.EXPAND) 
            
            add_btn.Bind(wx.EVT_BUTTON,self.OnAdd)
            rmv_btn.Bind(wx.EVT_BUTTON,self.OnSupp)    
            
            self.SetSizer(sizer) 
        
        def update(self,project=None):
            if project:
                self.update()
                for i,s in enumerate(project.data.loc):
                    self.grid.AppendRows(numRows=1)
                    row=[]
                    for k in self.main_frame.config.loc_schema.__dict__:
                        row.append(getattr(s,k))
                    self.grid.add_row(i,row)
                
            else:
                if self.grid.GetNumberRows()>0:
                    self.grid.DeleteRows(numRows=self.grid.GetNumberRows())
            
        def OnAdd(self,e):
            project = self.main_frame.get_selected_project()
            if project:
              n=self.grid.GetNumberRows()
              self.grid.AppendRows(1) 
              self.grid.add_row(n,[project.uuid,'_'+uuid_gen()])
              self.Layout()
              self.Parent.Layout()
              
        def OnSupp(self, event):
            if self.grid.GetNumberRows()>0 and self.grid.sel:
                project=self.main_frame.projects[self.grid.GetCellValue( self.grid.sel[0], 0)]
                dlg = wx.MessageDialog(None, self.main_frame.dict.supp_req+" '"+self.grid.GetCellValue( self.grid.sel[0], 2)+"'?",project.name ,wx.YES_NO | wx.ICON_QUESTION)
                result = dlg.ShowModal()
                if result == wx.ID_YES:
                   self.grid.DeleteRows( pos=self.grid.sel[0], numRows=1)
                   # self.Fit()
                   self.update_data(project)
               
               
               
        def update_data(self,project):
            loc=[]
            for i in range(self.grid.GetNumberRows()):
                if self.grid.GetCellValue(i,2):
                    l={}
                    for j,k in enumerate(self.main_frame.config.loc_schema.__dict__):
                        l[k]=self.grid.GetCellValue(i,j)
                    loc.append(obj__(l))
                    
                if not self.grid.GetCellValue(i,2) and self.grid.GetCellValue(i,4):
                    for j,k in enumerate(self.main_frame.config.loc_schema.__dict__):
                        if j==2:
                            l[k]=self.grid.GetCellValue(i,4)
                        else:
                            l[k]=self.grid.GetCellValue(i,j)
                    loc.append(obj__(l))
                   
            # update
            new_ids=list(map(lambda x:x.id,loc))
            # rmv if not exists
            for p in project.data.posts:
                if not p.loc in new_ids:
                    p.loc=''
                for s in p.regen.loc.__dict__:
                    if not getattr(p.regen.loc,s) in new_ids:
                        setattr(p.regen.loc,s,"")
            for s in project.data.sources:
                if not s.loc in new_ids:
                    s.loc=''
            for s in project.data.sinks:
                if not s.loc in new_ids:
                    s.loc=''  
            project.data.loc=loc
            project.save()                   
                
# ============================================================================
#      POST TAB =============================================================
# ============================================================================
class regen_grid(gridlib.Grid):
    def __init__(self, parent,main_frame,project,post):
        self.project=project
        self.post=post
        self.main_frame=main_frame
        self.sel=[]
        self.fonts=[wx.Font(14, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,  wx.FONTWEIGHT_BOLD, underline=False,faceName="", encoding=wx.FONTENCODING_DEFAULT),
                    wx.Font(14, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,  wx.FONTWEIGHT_NORMAL, underline=False,faceName="", encoding=wx.FONTENCODING_DEFAULT)]
        self.default_subs_color=wx.Colour(40, 180, 99)
        self.default_loc_color=wx.Colour(46, 134, 193) 
        gridlib.Grid.__init__(self, parent,) 
        self.CreateGrid(0,len(main_frame.dict.regen_cols))
        for i,c in enumerate(main_frame.dict.regen_cols):
           self.SetColLabelValue(i, c.encode(encoding='iso-8859-1'))
        self.HideCol(0)

        self.AutoSize()
            # Grid
        self.EnableEditing( True )
        self.EnableGridLines( True )
        self.SetGridLineColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
        self.EnableDragGridSize( True )
        self.SetMargins( 0, 0 )
                # Columns
        self.EnableDragColMove( False )
        self.EnableDragColSize( True )
        self.SetColLabelSize( 20 )
        self.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        self.SetColSize(1,160)
        self.SetColSize(2,100)
        self.SetColSize(3,100)
        self.SetColSize(4,160)

        # Rows
        self.EnableDragRowSize( True )
        self.SetRowLabelSize(20 )
        self.SetRowLabelAlignment( wx.ALIGN_LEFT, wx.ALIGN_LEFT )
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK,self.OnCellDClick)
    def OnCellDClick(self,e):
        #"subs","Polluants","Taux d'élimination","Fraction massique","Atelier"
        if e.GetCol() in [2,3] :
            var_name = {2:'R',3:'f'}[e.GetCol()]
            print(var_name)
            var = getattr(getattr(self.post.regen,var_name),self.GetCellValue(e.GetRow(),0))
            subs=next(p for p in self.project.data.subs if p.id == self.GetCellValue(e.GetRow(),0))
            VarCellDialog(self,self.project,self.post,var,'REGEN('+subs.name+')_'+{2:'R',3:'f'}[e.GetCol()]).ShowModal()
  
        
        
        
class post_grid(gridlib.Grid):
    def __init__(self, parent,main_frame):
        self.main_frame=main_frame
        self.sel=[]
        self.fonts=[wx.Font(14, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,  wx.FONTWEIGHT_BOLD, underline=False,faceName="", encoding=wx.FONTENCODING_DEFAULT),
                    wx.Font(14, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,  wx.FONTWEIGHT_NORMAL, underline=False,faceName="", encoding=wx.FONTENCODING_DEFAULT)]
        self.default_name_color=wx.Colour(93, 109, 126) #" blue"
        self.default_subs_color=wx.Colour(40, 180, 99)
        self.err_name_color=wx.Colour(231, 76, 60)
        gridlib.Grid.__init__(self, parent,) 
        self.CreateGrid(0,len(main_frame.dict.post_cols))
        for i,c in enumerate(main_frame.dict.post_cols):
           self.SetColLabelValue(i, c)
        for i in [0,1,2]:
            self.HideCol(i)

        self.AutoSize()
            # Grid
        self.EnableEditing( True )
        self.EnableGridLines( True )
        self.SetGridLineColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
        self.EnableDragGridSize( True )
        self.SetMargins( 0, 0 )
                # Columns
        self.EnableDragColMove( False )
        self.EnableDragColSize( True )
        self.SetColLabelSize( 20 )
        self.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        self.SetColSize(3,160)
        self.SetColSize(4,160)
        self.SetColSize(5,150)
        self.SetColSize(6,80)
        self.SetColSize(7,80)

        # Rows
        self.EnableDragRowSize( True )
        self.SetRowLabelSize(20 )
        self.SetRowLabelAlignment( wx.ALIGN_LEFT, wx.ALIGN_LEFT )
        
        # self.GetGridWindow().Bind(wx.EVT_MOTION, self.onMouseOver)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.onCellChanged)
        self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.onSingleSelect) 
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK,self.OnCellDClick)  
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK,self.OnPostShow)
    
    def OnPostShow(self,e):
        if e.GetCol()==3 :
            project=self.main_frame.projects[self.GetCellValue(0,0)]
            post=next(p for p in project.data.posts if p.id == self.GetCellValue(e.GetRow(),1))
            win = popup(self, )#
            win.htm.SetPage(post.toHTM(project,tp='post'))
            btn = e.GetEventObject()
            pos = btn.ClientToScreen( (0,0) )
            sz =  btn.GetSize()
            win.Position(pos, (0, sz[1]))
            win.Show(True)
    def OnCellDClick(self,e):
        if e.GetCol() in [5,6,7] :
            project=self.main_frame.projects[self.GetCellValue(0,0)]
            post=next(p for p in project.data.posts if p.id == self.GetCellValue(e.GetRow(),1))
            var = getattr(post.subs,self.GetCellValue(e.GetRow(),2))[e.GetCol()-5]
            VarCellDialog(self,project,post,var,{5:'mc',6:'cin_max',7:'cout_max'}[e.GetCol()]).ShowModal()
        if e.GetCol()==3 :
            project=self.main_frame.projects[self.GetCellValue(0,0)]
            post=next(p for p in project.data.posts if p.id == self.GetCellValue(e.GetRow(),1))
            class CellDialog(wx.Dialog):
                def __init__(self, parent): 
                    super(CellDialog, self).__init__(parent, title = post.name, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,size=(600,-1)) 
                    panel = wx.Panel(self) 
                    sizer = wx.BoxSizer(wx.VERTICAL) 
                    

                    loc_choices=list(map(lambda x:x.name, project.data.loc))
                    loc_choices.append("undefined")
                    self.loc=box_lst(panel,parent.main_frame.dict.loc,size=(100, 30), choices=loc_choices)
                    if post.loc:
                        self.loc.SetValue(next(l for l in project.data.loc if l.id == post.loc).name)
                    
                    self.regen=regen_grid(panel,parent.main_frame,project,post)
                    regen_label_sbox = wx.StaticBox(panel, -1, parent.main_frame.dict.regen.encode(encoding='iso-8859-1')) 
                    regen_sizer = wx.StaticBoxSizer(regen_label_sbox, wx.VERTICAL,) 
                    
                    
                    for i,k in enumerate(project.data.subs):
                        self.regen.AppendRows(1) 
                        self.regen.SetCellValue(i,0,k.id)
                        self.regen.SetCellValue(i,1,k.name)
                        self.regen.SetCellValue(i,2,str(getattr(post.regen.R,k.id).val))
                        self.regen.SetCellValue(i,3,str(getattr(post.regen.f,k.id).val))
                        regen_loc=getattr(post.regen.loc,k.id)
                        if regen_loc:
                            regen_loc = next(l for l in project.data.loc if l.id == regen_loc).name
                        else:
                            regen_loc=""
                        self.regen.SetCellEditor(i,4,wx.grid.GridCellChoiceEditor(loc_choices,) )
                        self.regen.SetCellValue(i,4,regen_loc)
                        self.regen.SetCellTextColour(i, 1, self.regen.default_subs_color)
                        self.regen.SetRowSize(i,24)
                        self.regen.SetCellFont(i,1,self.regen.fonts[0])
                    
                    regen_sizer.Add(self.regen,-1)    
                    
                    
                    self.btn = wx.Button(panel, -1, label = "OK")
                    self.btn.Bind(wx.EVT_BUTTON,self.OnOk) 
                    
                    
                    sizer.Add(self.loc.sizer)
                    sizer.Add(regen_sizer,-1,wx.EXPAND)
                    sizer.Add(self.btn) 
                    panel.SetSizer(sizer) 
                    

                    
                def OnOk(self,e):
                    if self.loc.GetValue()=="undefined":
                        post.loc=''
                    elif self.loc.GetValue():
                        post.loc=next(l for l in project.data.loc if l.name == self.loc.GetValue()).id
                    for i in range(self.regen.GetNumberRows()):
                        s_id = self.regen.GetCellValue(i,0)
                        getattr(post.regen.R,s_id).val = str2num(self.regen.GetCellValue(i,2))
                        getattr(post.regen.f,s_id).val = str2num(self.regen.GetCellValue(i,3))
                        if self.regen.GetCellValue(i,4)=="undefined":
                            setattr(post.regen.loc,s_id,"")
                        elif self.regen.GetCellValue(i,4):
                            setattr(post.regen.loc,s_id,next(l for l in project.data.loc if l.name == self.regen.GetCellValue(i,4)).id)
                    project.save()
                    self.Destroy()
            
            CellDialog(self,).ShowModal()
        
    def onSingleSelect(self, event):
        self.sel = [event.GetRow(),event.GetCol()]
        event.Skip()
    def onCellChanged(self,e):
            row=e.GetRow()
            project=self.main_frame.projects[self.GetCellValue(row,0)]
            post=next(p for p in project.data.posts if p.id == self.GetCellValue(row,1))
            if e.GetCol()==3:
                post.name=self.GetCellValue(row,3)
            else:
                getattr(post.subs,self.GetCellValue(row,2))[0].val=str2num(self.GetCellValue(row,5))
                getattr(post.subs,self.GetCellValue(row,2))[1].val=str2num(self.GetCellValue(row,6))
                getattr(post.subs,self.GetCellValue(row,2))[2].val=str2num(self.GetCellValue(row,7))

            project.save() 
            # if self.main_frame.sim_dyn[(project)]:
            #     print('sim dyn')
            #     self.main_frame.sim_dyn["main"].htm.SetPage(project.sim_dyn())
class post_tab(wx.ScrolledWindow):
        def __init__(self, parent,main_frame):
            self.main_frame=main_frame
            super().__init__(parent)
            self.SetScrollbars(20, 20, 50, 50)
            add_btn = wx.BitmapButton(self , 0,bitmap=wx.Bitmap(os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",self.main_frame.icons.add), wx.BITMAP_TYPE_ANY))
            rmv_btn = wx.BitmapButton(self , 1,bitmap=wx.Bitmap(os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",self.main_frame.icons.rmv), wx.BITMAP_TYPE_ANY))
            sizer = wx.BoxSizer(wx.VERTICAL)
            btn_sizer = wx.BoxSizer(wx.HORIZONTAL) 
            btn_sizer.Add(add_btn,) 
            btn_sizer.Add(rmv_btn,) 
            sizer.Add(btn_sizer ,) 
            
            self.grid=post_grid(self,main_frame)
            sizer.Add(self.grid, 1, flag=wx.EXPAND) 
            
            add_btn.Bind(wx.EVT_BUTTON,self.OnAdd)
            rmv_btn.Bind(wx.EVT_BUTTON,self.OnSupp)    
            
            self.SetSizer(sizer) 
            
            self.grid_color=False
        def get_grid_color(self):
                self.grid_color=not self.grid_color
                if self.grid_color:
                    return wx.Colour(255, 255, 255,0)
                else:
                    return wx.Colour(240, 240, 240,100)
        
        def update(self,project=None):
            if project:
                    self.update()
                    self.grid_color=False
                    color=0
                    count=0
                    for i,p in enumerate(project.data.posts):
                        for j,s in enumerate(project.data.subs):
                            self.grid.AppendRows(1) 
                            for k,id_ in enumerate([project.uuid,p.id,s.id]):
                                self.grid.SetCellValue(count, k,id_)
                            if j==0:
                                color=self.get_grid_color()
                                self.grid.SetCellValue(count, 3,p.name)
                                self.grid.SetCellFont(count,3,self.grid.fonts[0])
                                self.grid.SetCellTextColour(count, 3, self.grid.default_name_color)
                            else:
                                self.grid.SetReadOnly(count, 3, isReadOnly=True)
                            self.grid.SetReadOnly(count, 4, isReadOnly=True)
                            self.grid.SetCellTextColour(count, 4, self.grid.default_subs_color)
                            self.grid.SetCellValue(count, 4,s.name)
                            self.grid.SetCellFont(count,4,self.grid.fonts[0])
                            for k,var in enumerate(getattr(p.subs,s.id)):
                                self.grid.SetCellValue(count, 5+k,str(var.val))
                            for k in range(self.grid.GetNumberCols()):
                                self.grid.SetCellBackgroundColour(count, k, color)
                            self.grid.SetRowSize(count,24)
                            count+=1
                    self.Layout()
                    self.Parent.Layout()  
            else:
                if self.grid.GetNumberRows()>0:
                    self.grid.DeleteRows(numRows=self.grid.GetNumberRows()) 
            
        def OnAdd(self,e):
            project = self.main_frame.get_selected_project()
            if project:
                post=copy.deepcopy(self.main_frame.config.post_schema)
                post.name = self.main_frame.dict.post+str(len(project.data.posts)+1)
                post.id=uuid_gen()
                for s in project.data.subs:
                    setattr(post.subs,s.id,[var__(self.main_frame),var__(self.main_frame),var__(self.main_frame)])
                    setattr(post.regen.loc,s.id,"")
                    setattr(post.regen.R,s.id,var__(self.main_frame))
                    setattr(post.regen.f,s.id,var__(self.main_frame))
                project.data.posts.append(post)
                project.save()
                self.update(project)
              
        def OnSupp(self, event):
            if self.grid.GetNumberRows()>0 and self.grid.sel:
                project=self.main_frame.projects[self.grid.GetCellValue( self.grid.sel[0], 0)]
                post=next(p for p in project.data.posts if p.id == self.grid.GetCellValue( self.grid.sel[0], 1))
                dlg = wx.MessageDialog(None, self.main_frame.dict.supp_req+" '"+self.grid.GetCellValue( self.grid.sel[0], 3)+"'?",project.name,wx.YES_NO | wx.ICON_QUESTION)
                result = dlg.ShowModal()
                if result == wx.ID_YES:
                    project.data.posts = [x for x in project.data.posts if not (post.id == x.id)]
                    project.save()
                    self.update(project)
               
               
# ============================================================================
#     SINK TAB =============================================================
# ============================================================================  
class sink_grid(gridlib.Grid):
    def __init__(self, parent,main_frame):
        self.main_frame=main_frame
        self.sel=[]
        self.fonts=[wx.Font(14, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,  wx.FONTWEIGHT_BOLD, underline=False,faceName="", encoding=wx.FONTENCODING_DEFAULT),
                    wx.Font(14, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,  wx.FONTWEIGHT_NORMAL, underline=False,faceName="", encoding=wx.FONTENCODING_DEFAULT)]
        self.default_name_color=wx.Colour(93, 109, 126) #" blue"
        self.default_subs_color=wx.Colour(40, 180, 99)
        gridlib.Grid.__init__(self, parent,) 
        self.CreateGrid(0,len(main_frame.dict.sink_cols))
        for i,c in enumerate(main_frame.dict.sink_cols):
           self.SetColLabelValue(i, c.encode('cp1252'))
        for i in [0,1,2]:
            self.HideCol(i)

        self.AutoSize()
            # Grid
        self.EnableEditing( True )
        self.EnableGridLines( True )
        self.SetGridLineColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
        self.EnableDragGridSize( True )
        self.SetMargins( 0, 0 )
                # Columns
        self.EnableDragColMove( False )
        self.EnableDragColSize( True )
        self.SetColLabelSize( 20 )
        self.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        self.SetColSize(3,160)
        self.SetColSize(4,160)
        self.SetColSize(5,80)
        self.SetColSize(6,150)

        # Rows
        self.EnableDragRowSize( True )
        self.SetRowLabelSize(20 )
        self.SetRowLabelAlignment( wx.ALIGN_LEFT, wx.ALIGN_LEFT )
        
        self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.onCellChanged)
        self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.onSingleSelect) 
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK,self.OnCellDClick)  
    
    def OnCellDClick(self,e):
        if e.GetCol()==3 :
            project=self.main_frame.projects[self.GetCellValue(0,0)]
            sink=next(x for x in project.data.sinks if x.id == self.GetCellValue(e.GetRow(),1))
            class CellDialog(wx.Dialog):
                def __init__(self, parent): 
                    super(CellDialog, self).__init__(parent, title = sink.name, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,size=(600,-1)) 
                    panel = wx.Panel(self) 
                    sizer = wx.BoxSizer(wx.VERTICAL) 
                    
                    loc_choices=list(map(lambda x:x.name, project.data.loc))
                    loc_choices.append("undefined")
                    self.loc=box_lst(panel,parent.main_frame.dict.loc,size=(100, 30), choices=loc_choices)
                    if sink.loc:
                        self.loc.SetValue(next(l for l in project.data.loc if l.id == sink.loc).name)
                       
                    self.btn = wx.Button(panel, -1, label = "OK")
                    self.btn.Bind(wx.EVT_BUTTON,self.OnOk) 
                    
                    sizer.Add(self.loc.sizer)
                    sizer.Add(self.btn) 
                    panel.SetSizer(sizer) 
                    

                    
                def OnOk(self,e):
                    if self.loc.GetValue()=="undefined":
                        sink.loc=''
                    elif self.loc.GetValue():
                        sink.loc=next(l for l in project.data.loc if l.name == self.loc.GetValue()).id
                    project.save()
                    self.Destroy()
            
            CellDialog(self,).ShowModal()
        
    def onSingleSelect(self, event):
        self.sel = [event.GetRow(),event.GetCol()]
        event.Skip()
    def onCellChanged(self,e):
            row=e.GetRow()
            project=self.main_frame.projects[self.GetCellValue(row,0)]
            sink=next(x for x in project.data.sinks if x.id == self.GetCellValue(row,1))
            if e.GetCol()==3:
                sink.name=self.GetCellValue(row,3)
            elif e.GetCol()==5: # c
               getattr(sink.subs,self.GetCellValue(row,2)).val=str2num(self.GetCellValue(row,5))
            elif e.GetCol()==6: # m
                sink.m.val=str2num(self.GetCellValue(row,6))
            project.save() 
class sink_tab(wx.ScrolledWindow):
        def __init__(self, parent,main_frame):
            self.main_frame=main_frame
            super().__init__(parent)
            self.SetScrollbars(20, 20, 50, 50)
            add_btn = wx.BitmapButton(self , 0,bitmap=wx.Bitmap(os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",self.main_frame.icons.add), wx.BITMAP_TYPE_ANY))
            rmv_btn = wx.BitmapButton(self , 1,bitmap=wx.Bitmap(os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",self.main_frame.icons.rmv), wx.BITMAP_TYPE_ANY))
            sizer = wx.BoxSizer(wx.VERTICAL)
            btn_sizer = wx.BoxSizer(wx.HORIZONTAL) 
            btn_sizer.Add(add_btn,) 
            btn_sizer.Add(rmv_btn,) 
            sizer.Add(btn_sizer ,) 
            
            self.grid=sink_grid(self,main_frame)
            sizer.Add(self.grid, 1, flag=wx.EXPAND) 
            
            add_btn.Bind(wx.EVT_BUTTON,self.OnAdd)
            rmv_btn.Bind(wx.EVT_BUTTON,self.OnSupp)    
            
            self.SetSizer(sizer) 
            
            self.grid_color=False
        def get_grid_color(self):
                self.grid_color=not self.grid_color
                if self.grid_color:
                    return wx.Colour(255, 255, 255,0)
                else:
                    return wx.Colour(240, 240, 240,100)
        
        def update(self,project=None):
            if project:
                    self.update()
                    self.grid_color=False
                    color=0
                    count=0
                    for i,p in enumerate(project.data.sinks):
                        for j,s in enumerate(project.data.subs):
                            self.grid.AppendRows(1) 
                            for k,id_ in enumerate([project.uuid,p.id,s.id]):
                                self.grid.SetCellValue(count, k,id_)
                            if j==0:
                                color=self.get_grid_color()
                                self.grid.SetCellValue(count, 3,p.name)
                                self.grid.SetCellValue(count, 6,str(p.m.val))
                                self.grid.SetCellFont(count,3,self.grid.fonts[0])
                                self.grid.SetCellTextColour(count, 3, self.grid.default_name_color)
                            else:
                                self.grid.SetReadOnly(count, 3, isReadOnly=True)
                                self.grid.SetReadOnly(count, 6, isReadOnly=True)
                            self.grid.SetReadOnly(count, 4, isReadOnly=True)
                            self.grid.SetCellTextColour(count, 4, self.grid.default_subs_color)
                            self.grid.SetCellValue(count, 4,s.name)
                            self.grid.SetCellFont(count,4,self.grid.fonts[0])
                            self.grid.SetCellValue(count, 5,str(getattr(p.subs,s.id).val))
                            for k in range(self.grid.GetNumberCols()):
                                self.grid.SetCellBackgroundColour(count, k, color)
                            if j==0:
                                self.grid.SetCellBackgroundColour(count, 6, wx.Colour(214, 234, 248))
                            self.grid.SetRowSize(count,24)
                            count+=1
                    self.Layout()
                    self.Parent.Layout()  
            else:
                if self.grid.GetNumberRows()>0:
                    self.grid.DeleteRows(numRows=self.grid.GetNumberRows()) 
            
        def OnAdd(self,e):
            project = self.main_frame.get_selected_project()
            if project:
                sink=copy.deepcopy(self.main_frame.config.sink_schema)
                sink.name = self.main_frame.dict.sink+str(len(project.data.sinks)+1)
                sink.id=uuid_gen()
                sink.m=var__(self.main_frame)
                for s in project.data.subs:
                    setattr(sink.subs,s.id,var__(self.main_frame))
                project.data.sinks.append(sink)
                project.save()
                self.update(project)
              
        def OnSupp(self, event):
            if self.grid.GetNumberRows()>0 and self.grid.sel:
                project=self.main_frame.projects[self.grid.GetCellValue( self.grid.sel[0], 0)]
                sink=next(x for x in project.data.sinks if x.id == self.grid.GetCellValue( self.grid.sel[0], 1))
                dlg = wx.MessageDialog(None, self.main_frame.dict.supp_req+" '"+self.grid.GetCellValue( self.grid.sel[0], 3)+"'?",project.name,wx.YES_NO | wx.ICON_QUESTION)
                result = dlg.ShowModal()
                if result == wx.ID_YES:
                    project.data.sinks = [x for x in project.data.sinks if not (sink.id == x.id)]
                    project.save()
                    self.update(project)               
# ============================================================================
#     SOURCE TAB =============================================================
# ============================================================================  
class source_grid(gridlib.Grid):
    def __init__(self, parent,main_frame):
        self.main_frame=main_frame
        self.sel=[]
        self.fonts=[wx.Font(14, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,  wx.FONTWEIGHT_BOLD, underline=False,faceName="", encoding=wx.FONTENCODING_DEFAULT),
                    wx.Font(14, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,  wx.FONTWEIGHT_NORMAL, underline=False,faceName="", encoding=wx.FONTENCODING_DEFAULT)]
        self.default_name_color=wx.Colour(93, 109, 126) #" blue"
        self.default_subs_color=wx.Colour(40, 180, 99)
        gridlib.Grid.__init__(self, parent,) 
        self.CreateGrid(0,len(main_frame.dict.source_cols))
        for i,c in enumerate(main_frame.dict.source_cols):
           self.SetColLabelValue(i, c.encode('cp1252'))
        for i in [0,1,2]:
            self.HideCol(i)

        self.AutoSize()
            # Grid
        self.EnableEditing( True )
        self.EnableGridLines( True )
        self.SetGridLineColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
        self.EnableDragGridSize( True )
        self.SetMargins( 0, 0 )
                # Columns
        self.EnableDragColMove( False )
        self.EnableDragColSize( True )
        self.SetColLabelSize( 20 )
        self.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        self.SetColSize(3,160)
        self.SetColSize(4,160)
        self.SetColSize(5,80)
        self.SetColSize(6,150)

        # Rows
        self.EnableDragRowSize( True )
        self.SetRowLabelSize(20 )
        self.SetRowLabelAlignment( wx.ALIGN_LEFT, wx.ALIGN_LEFT )
        
        self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.onCellChanged)
        self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.onSingleSelect) 
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK,self.OnCellDClick)  
    
    def OnCellDClick(self,e):
        if e.GetCol()==3 :
            project=self.main_frame.projects[self.GetCellValue(0,0)]
            source=next(x for x in project.data.sources if x.id == self.GetCellValue(e.GetRow(),1))
            class CellDialog(wx.Dialog):
                def __init__(self, parent): 
                    super(CellDialog, self).__init__(parent, title = source.name, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,size=(600,-1)) 
                    panel = wx.Panel(self) 
                    sizer = wx.BoxSizer(wx.VERTICAL) 
                    
                    loc_choices=list(map(lambda x:x.name, project.data.loc))
                    loc_choices.append("undefined")
                    self.loc=box_lst(panel,parent.main_frame.dict.loc,size=(100, 30), choices=loc_choices)
                    if source.loc:
                        self.loc.SetValue(next(l for l in project.data.loc if l.id == source.loc).name)
                       
                    self.btn = wx.Button(panel, -1, label = "OK")
                    self.btn.Bind(wx.EVT_BUTTON,self.OnOk) 
                    
                    sizer.Add(self.loc.sizer)
                    sizer.Add(self.btn) 
                    panel.SetSizer(sizer) 
                    

                    
                def OnOk(self,e):
                    if self.loc.GetValue()=="undefined":
                        source.loc=''
                    elif self.loc.GetValue():
                        source.loc=next(l for l in project.data.loc if l.name == self.loc.GetValue()).id
                    project.save()
                    self.Destroy()
            
            CellDialog(self,).ShowModal()
        
    def onSingleSelect(self, event):
        self.sel = [event.GetRow(),event.GetCol()]
        event.Skip()
    def onCellChanged(self,e):
            row=e.GetRow()
            project=self.main_frame.projects[self.GetCellValue(row,0)]
            source=next(x for x in project.data.sources if x.id == self.GetCellValue(row,1))
            if e.GetCol()==3:
                source.name=self.GetCellValue(row,3)
            elif e.GetCol()==5:
                getattr(source.subs,self.GetCellValue(row,2)).val=str2num(self.GetCellValue(row,5))
            elif e.GetCol()==6:
                source.m.val=str2num(self.GetCellValue(row,6))
            project.save() 
class source_tab(wx.ScrolledWindow):
        def __init__(self, parent,main_frame):
            self.main_frame=main_frame
            super().__init__(parent)
            self.SetScrollbars(20, 20, 50, 50)
            add_btn = wx.BitmapButton(self , 0,bitmap=wx.Bitmap(os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",self.main_frame.icons.add), wx.BITMAP_TYPE_ANY))
            rmv_btn = wx.BitmapButton(self , 1,bitmap=wx.Bitmap(os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",self.main_frame.icons.rmv), wx.BITMAP_TYPE_ANY))
            sizer = wx.BoxSizer(wx.VERTICAL)
            btn_sizer = wx.BoxSizer(wx.HORIZONTAL) 
            btn_sizer.Add(add_btn,) 
            btn_sizer.Add(rmv_btn,) 
            sizer.Add(btn_sizer ,) 
            
            self.grid=source_grid(self,main_frame)
            sizer.Add(self.grid, 1, flag=wx.EXPAND) 
            
            add_btn.Bind(wx.EVT_BUTTON,self.OnAdd)
            rmv_btn.Bind(wx.EVT_BUTTON,self.OnSupp)    
            
            self.SetSizer(sizer) 
            
            self.grid_color=False
        def get_grid_color(self):
                self.grid_color=not self.grid_color
                if self.grid_color:
                    return wx.Colour(255, 255, 255,0)
                else:
                    return wx.Colour(240, 240, 240,100)
        
        def update(self,project=None):
            if project:
                    self.update()
                    self.grid_color=False
                    color=0
                    count=0
                    for i,p in enumerate(project.data.sources):
                        for j,s in enumerate(project.data.subs):
                            self.grid.AppendRows(1) 
                            for k,id_ in enumerate([project.uuid,p.id,s.id]):
                                self.grid.SetCellValue(count, k,id_)
                            if j==0:
                                color=self.get_grid_color()
                                self.grid.SetCellValue(count, 3,p.name)
                                self.grid.SetCellValue(count, 6,str(p.m.val))
                                self.grid.SetCellFont(count,3,self.grid.fonts[0])
                                self.grid.SetCellTextColour(count, 3, self.grid.default_name_color)
                            else:
                                self.grid.SetReadOnly(count, 3, isReadOnly=True)
                                self.grid.SetReadOnly(count, 6, isReadOnly=True)
                            self.grid.SetReadOnly(count, 4, isReadOnly=True)
                            self.grid.SetCellTextColour(count, 4, self.grid.default_subs_color)
                            self.grid.SetCellValue(count, 4,s.name)
                            self.grid.SetCellFont(count,4,self.grid.fonts[0])
                            self.grid.SetCellValue(count, 5,str(getattr(p.subs,s.id).val))
                            for k in range(self.grid.GetNumberCols()):
                                    self.grid.SetCellBackgroundColour(count, k, color)
                            if j==0:
                                self.grid.SetCellBackgroundColour(count, 6, wx.Colour(214, 234, 248))
                                    
                            self.grid.SetRowSize(count,24)
                            count+=1
                    self.Layout()
                    self.Parent.Layout()  
            else:
                if self.grid.GetNumberRows()>0:
                    self.grid.DeleteRows(numRows=self.grid.GetNumberRows()) 
            
        def OnAdd(self,e):
            project = self.main_frame.get_selected_project()
            if project:
                source=copy.deepcopy(self.main_frame.config.source_schema)
                source.name = self.main_frame.dict.source+str(len(project.data.sources)+1)
                source.id=uuid_gen()
                source.m=var__(self.main_frame)
                for s in project.data.subs:
                    setattr(source.subs,s.id,var__(self.main_frame))
                project.data.sources.append(source)
                project.save()
                self.update(project)
              
        def OnSupp(self, event):
            if self.grid.GetNumberRows()>0 and self.grid.sel:
                project=self.main_frame.projects[self.grid.GetCellValue( self.grid.sel[0], 0)]
                source=next(x for x in project.data.sources if x.id == self.grid.GetCellValue( self.grid.sel[0], 1))
                dlg = wx.MessageDialog(None, self.main_frame.dict.supp_req+" '"+self.grid.GetCellValue( self.grid.sel[0], 3)+"'?",project.name,wx.YES_NO | wx.ICON_QUESTION)
                result = dlg.ShowModal()
                if result == wx.ID_YES:
                    project.data.sources = [x for x in project.data.sources if not (source.id == x.id)]
                    project.save()
                    self.update(project)     
# ============================================================================
#     CONS TAB =============================================================
# ============================================================================  
class cons_grid(gridlib.Grid):
    def __init__(self, parent,main_frame):
        self.main_frame=main_frame
        gridlib.Grid.__init__(self, parent,) 
        self.CreateGrid(0,0)
        self.AutoSize()
            # Grid
        self.EnableEditing( False )
        self.EnableGridLines( True )
        self.SetGridLineColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
        self.EnableDragGridSize( True )
        self.SetMargins( 0, 0 )
                # Columns
        self.EnableDragColMove( False )
        self.EnableDragColSize( True )
        self.SetColLabelSize( 20 )
        self.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        # Rows
        self.EnableDragRowSize( True )
        self.SetRowLabelSize(20 )
        self.SetRowLabelAlignment( wx.ALIGN_LEFT, wx.ALIGN_LEFT )
        
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK,self.OnCellDClick) 
        self.SetLabelBackgroundColour(wx.Colour(255, 255, 255))
        self.SetLabelFont(wx.Font(8, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
        self.SetLabelTextColour(wx.Colour(128, 139, 150 ))
        
        self.sources_=[]
        self.sinks_=[]
    
    def OnCellDClick(self,e):
            class CellDialog(wx.Dialog):
                 def __init__(self, parent): 
                     self.project_=parent.main_frame.get_selected_project()
                     from_type,from_=parent.sources_[e.GetRow()]
                     to_type,to_=parent.sinks_[e.GetCol()]
                     self.cons_id=','.join((from_type,from_.id,to_type,to_.id))
                     self.cons=self.project_.get_cons(from_type,from_.id,to_type,to_.id)
                     super(CellDialog, self).__init__(parent, title = parent.main_frame.dict.cons+': '+from_.name+" -> "+to_.name, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,size=(-1,450)) 
                     

                     
                     panel = wx.Panel(self) 
                     sizer = wx.BoxSizer(wx.VERTICAL) 
                     bd_sizer = wx.BoxSizer(wx.HORIZONTAL) 
                     safety_sizer=wx.BoxSizer(wx.HORIZONTAL) 
                     self.lb=box_input(panel,parent.main_frame.dict.lb.encode('cp1252'),0)
                     self.ub=box_input(panel,parent.main_frame.dict.ub.encode('cp1252'),0)
                     bd_sizer.Add(self.lb.sizer)
                     bd_sizer.Add(self.ub.sizer)
                     
                     enable_sizer=wx.BoxSizer(wx.HORIZONTAL) 
                     self.enable = wx.CheckBox(panel,-1,label=parent.main_frame.dict.enable)
                     enable_sizer.Add(self.enable,0, wx.ALL|wx.CENTER)
                     
                     self.product_safety=box_input(panel,parent.main_frame.dict.product_safety.encode('cp1252'),0)
                     self.process_safety=box_input(panel,parent.main_frame.dict.process_safety.encode('cp1252'),0)
                     safety_sizer.Add(self.product_safety.sizer)
                     safety_sizer.Add(self.process_safety.sizer)
                     self.distance=box_input(panel,parent.main_frame.dict.distance.encode('cp1252'),0)
                     self.feasibility=box_input(panel,parent.main_frame.dict.feasibility.encode('cp1252'),0)
                     self.priority=box_input(panel,parent.main_frame.dict.priority.encode('cp1252'),0)
                       
                     self.btn = wx.Button(panel, -1, label = "OK")
                     self.btn.Bind(wx.EVT_BUTTON,self.OnOk) 
                     
                     htm = box_html(panel)
                     n_subs=len(self.project_.data.subs)
                     m_max=self.project_.cons_quick_balance(from_type,from_)
                    # im='<img src="icons\\w5.png" alt="" border=3 height=100 width=100>'
                     m_max='max. water supply: <font bgcolor=#F5B7B1>'+formatting(m_max,2,'m3/h</font>')
                     inf="<html><body bgcolor=#FDFEFE ><font size=2 face= 'courrier'>"
                     inf+="<table border=0 width=100%>"
                     inf+="<tr><td></td><td><b><font color='blue'>"+from_.name+"</font></b></td><td><b><font color='blue'>"+to_.name+"</font></b></td><td rowspan='"+str(n_subs+1)+"'>"+m_max+"</td></tr>"
                     for s in self.project_.data.subs:
                         if from_type=='post':
                             from_c=formatting(float(getattr(from_.subs,s.id)[-1].val))
                         else:
                             from_c=formatting(float(getattr(from_.subs,s.id).val))
                         if to_type=='post':
                            to_c=formatting(float(getattr(to_.subs,s.id)[1].val))
                         else:
                            to_c=formatting(float(getattr(to_.subs,s.id).val))
                         inf+="<tr><td><b><font color='green'>"+s.name+"</font></b></td><td>"+from_c+"</d><td>"+to_c+"</td><td></td></tr>"
                     inf+="</table>"
                     # inf+="<table>"
                     # inf+="<tr><td>"+c_tab+"</td>"
                     # m_max=self.project_.cons_quick_balance(from_type,from_)
                     # inf+='<td>'+'<img src="icons\\w5.png" alt="" border=3 height=60 width=20>'+'</td></tr></table>'
                     
                     
                     htm.SetPage(inf)
                     
                     self.is_new=False
                     if self.cons==None:
                         self.cons=copy.deepcopy(self.Parent.main_frame.config.cons_schema)
                         self.is_new=True
                     
                     for c in self.cons.__dict__ :
                        if c in self.__dict__:
                            if c=='enable':
                                getattr(self,c).SetValue(getattr(self.cons,c))
                            else:
                                getattr(self,c).SetValue(str(getattr(self.cons,c)))

                    
                     sizer.Add(htm,1,wx.EXPAND)
                     #sizer.Add(inf.sizer,1,wx.EXPAND)
                     sizer.Add(enable_sizer,0, wx.ALL|wx.CENTER,1)
                     sizer.Add(bd_sizer)
                     sizer.Add(safety_sizer)
                     sizer.Add(self.distance.sizer)
                     sizer.Add(self.feasibility.sizer)
                     sizer.Add(self.priority.sizer)
                     #sizer.Add(self.list,1,wx.EXPAND) 
                     sizer.Add(self.btn) 
                     panel.SetSizer(sizer) 
                     panel.Layout()
                    

                    
                 def OnOk(self,e):
                     if self.is_new:
                         self.project_.data.cons.append(self.cons)
                         self.cons.project=self.project_.uuid
                         self.cons.id = self.cons_id
                         from_type,from_,to_type,to_=self.cons_id.split(',')
                         self.cons.from_=from_
                         self.cons.from_type=from_type
                         self.cons.to_=to_
                         self.cons.to_type=to_type
                    
                     for c in self.cons.__dict__ :
                         if c in self.__dict__:
                             if c=='enable':
                                 setattr(self.cons,c,getattr(self,c).GetValue())
                             else:
                                 setattr(self.cons,c,str2num(getattr(self,c).GetValue()))

                     self.project_.save()
                     self.Parent.Parent.update(self.project_)
                     
                     
                     self.Destroy()
            
            CellDialog(self,).ShowModal() 
class cons_tab(wx.ScrolledWindow):
        def __init__(self, parent,main_frame):
            self.main_frame=main_frame
            super().__init__(parent)
            self.SetScrollbars(20, 20, 50, 50)
            self.grid=cons_grid(self,main_frame)
            sizer = wx.BoxSizer(wx.VERTICAL) 
            sizer.Add(self.grid, 1, flag=wx.EXPAND) 
        
            self.SetSizer(sizer) 
        
        def update(self,project=None):
            if project:
                    self.update()
                    sources_=[]
                    sinks_=[]
                    for p in project.data.posts:
                        sinks_.append(('post',p))
                        sources_.append(('post',p))
                    for s in project.data.sinks:
                        sinks_.append(('sink',s))
                    for s in project.data.sources:
                        sources_.append(('source',s))
                    self.grid.InsertRows(pos=0, numRows=len(sources_), updateLabels=False)
                    self.grid.InsertCols(pos=0, numCols=len(sinks_), updateLabels=False)
                    self.grid.SetRowLabelSize(100)
                    for i,sr in enumerate(sources_):
                        self.grid.SetRowLabelValue(i, sr[1].name)
                    for i,sk in enumerate(sinks_):
                        self.grid.SetColLabelValue(i, sk[1].name)
                    self.Layout()
                    self.Parent.Layout()  

                    self.grid.sources_=sources_
                    self.grid.sinks_=sinks_
                    
                    # update cells
                    for i,sr in enumerate(sources_):
                        for j,sk in enumerate(sinks_):
                            c = project.get_cons(sr[0],sr[1].id,sk[0],sk[1].id)
                            if c:
                                if c.enable:
                                    self.grid.SetCellBackgroundColour(i,j, wx.Colour(214, 234, 248))
                                    if c.ub:
                                        self.grid.SetCellValue(i,j,'['+str(c.lb)+','+str(c.ub)+']')
                            
            else:
                self.grid.sources_=[]
                self.grid.sinks_=[]
                if self.grid.GetNumberRows()>0:
                    self.grid.DeleteRows(numRows=self.grid.GetNumberRows()) 
                if self.grid.GetNumberCols()>0:
                    self.grid.DeleteCols(numCols=self.grid.GetNumberCols()) 
                    
             
class project_tab(wx.ScrolledWindow):
        def __init__(self, parent,main_frame):
            super().__init__(parent)
            self.main_frame=main_frame
            self.SetScrollbars(20, 20, 50, 50)
            sizer = wx.BoxSizer(wx.VERTICAL) 
            
            self.name=box_input(self,self.main_frame.dict.project_name,0,style = wx.ALIGN_LEFT|wx.TE_PROCESS_ENTER,size=(200, -1))
            self.desc=box_input(self,self.main_frame.dict.desc,-1,style = wx.ALIGN_LEFT|wx.TE_MULTILINE|wx.TE_READONLY,)
            
            self.name.Bind(wx.EVT_TEXT_ENTER,self.on_name)
            
            self.desc.Bind(wx.EVT_LEFT_DCLICK,self.on_desc)
            self.desc.SetToolTip(self.main_frame.dict.dc2edit)

            sizer.Add(self.name.sizer,0) 
            sizer.Add(self.desc.sizer,1,wx.EXPAND) 
            self.SetSizer(sizer) 
        def on_name(self,e):
                name = e.GetEventObject()
                project = self.main_frame.get_selected_project()
                if project:
                    project.data.name=name.GetValue()
                    project.save()
                    self.main_frame.project_tree.tree.SetItemText(self.main_frame.project_tree.tree.GetSelection(), project.data.name)

        def on_desc(self,e):
                   project_name=''
                   project = self.main_frame.get_selected_project()
                   if project:
                       project_name=project.name
                   desc = e.GetEventObject()
                   dlg = wx.TextEntryDialog(self,self.main_frame.dict.desc,project_name ,style = wx.TextEntryDialogStyle|wx.TE_MULTILINE)
                   dlg.SetValue(desc.GetValue())
                   dlg.SetSize((400,400))
                   if dlg.ShowModal() == wx.ID_OK:
                       desc.SetValue(dlg.GetValue())
                       if project:
                           project.data.desc=dlg.GetValue()
                           project.save()
                   dlg.Destroy()
        def update(self,project=None):
            if project:
                 self.name.SetValue(project.name)
                 self.desc.SetValue(project.data.desc)
            else:
                self.name.SetValue("")
                self.desc.SetValue("")




"""
    PROJECT PANEL CONFIG
"""
class project_panel_config(wx.ScrolledWindow):
     def __init__(self,parent,main_frame):
            super().__init__(parent,size=(-1,200)) 
            self.SetScrollbars(20, 20, 50, 50) 
            self.main_frame=main_frame
        
            # Create a panel and notebook (tabs holder)
            nb = wx.Notebook(self)
            nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED,self.OnTabChange)
            
            # Create the tab windows
            setattr(self.main_frame,'project_tab',project_tab(nb,main_frame))
            setattr(self.main_frame,'subs_tab',subs_tab(nb,main_frame))
            setattr(self.main_frame,'loc_tab',loc_tab(nb,main_frame))
            setattr(self.main_frame,'post_tab',post_tab(nb,main_frame))
            setattr(self.main_frame,'sink_tab',sink_tab(nb,main_frame))
            setattr(self.main_frame,'source_tab',source_tab(nb,main_frame))
            setattr(self.main_frame,'cons_tab',cons_tab(nb,main_frame))
            
            # Add the windows to tabs and name them.
            nb.AddPage(self.main_frame.project_tab, self.main_frame.dict.project_tab)
            nb.AddPage(self.main_frame.subs_tab, self.main_frame.dict.subs_tab)
            nb.AddPage(self.main_frame.loc_tab, self.main_frame.dict.loc_tab)
            nb.AddPage(self.main_frame.post_tab, self.main_frame.dict.post_tab)
            nb.AddPage(self.main_frame.sink_tab, self.main_frame.dict.sink_tab)
            nb.AddPage(self.main_frame.source_tab, self.main_frame.dict.source_tab)
            nb.AddPage(self.main_frame.cons_tab, self.main_frame.dict.cons_tab)
            
            # Set noteboook in a sizer to create the layout
            sizer = wx.BoxSizer()
            sizer.Add(nb, 1, wx.EXPAND,-1)
            self.SetSizer(sizer)
     def OnTabChange(self,e):
         project = self.main_frame.get_selected_project()
         if project:
             if e.GetSelection()==3: # posts tab selection
                 self.main_frame.post_tab.update(project)
             if e.GetSelection()==4: # sinks tab selection
                 self.main_frame.sink_tab.update(project)
             if e.GetSelection()==5: # source tab selection
                 self.main_frame.source_tab.update(project)
             if e.GetSelection()==6: # cons tab selection
                 self.main_frame.cons_tab.update(project)
             



"""
PROJECT PANEL DISP

"""
class html_result(html.HtmlWindow):

        
    # def OnCellClicked(self, cell, x, y, event):
    #     #print(dir(cell))
    #     print(cell.ConvertToText(cell.GetFirstChild()))
    #     #print(cell.GetRootCell().GetId())
    #     return True
    def OnLinkClicked(self, link):
        #print(dir(link))
        cmd,s=link.Href.split(",")
        if s:
            s = next(p for p in self.project.data.subs if p.id == s)
        if cmd=="plot_composite1":
            fig,ax = self.project.mono["pinchs"][s.id].composite()
            fig.canvas.set_window_title(self.project.name+" >> "+"Composite 1"+" >> "+s.name)
            fig.show()
        if cmd=="plot_composite2":
            fig,ax=self.project.mono["pinchs"][s.id].sk_sr_graph()
            fig.canvas.set_window_title(self.project.name+" >> "+"Composite 2"+" >> "+s.name)
            fig.show()
        if cmd[0:7]=="network":
            print("netwwww")
            g=self.project.mono["pinchs"][s.id].design.draw(grouping=True)
            g.format=cmd[7:]
            dir_ = os.path.join(self.project.dirname,"networks")
            g.view(filename=self.project.name+"_"+"RESEAU_EAU"+"_"+s.name,directory=dir_)
        if cmd=="main":
            self.SetPage(self.project.mono["html"]["main"])
        if cmd=="cascade1":
            self.SetPage(self.project.mono["html"]["cascade1"][s.id])
        if cmd=="cascade0":
            self.SetPage(self.project.mono["html"]["cascade0"][s.id])     
        if cmd[0:11] == "balancepost":
            self.SetPage(self.project.mono["html"]["pbalance"][s.id][int(cmd[11:])])  
        if cmd[0:8] == "pollpost":
            self.SetPage(self.project.mono["html"]["ppollution"][s.id][int(cmd[8:])])  
        if cmd=="sensi_bar":
            barWidth=.4
            fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
            SI = self.project.sensi["bar"]["SI"]
            ST = self.project.sensi["bar"]["ST"]
            labels = self.project.sensi["bar"]["labels"]
            x=range(len(SI))
            x2 = [x + barWidth for x in x]
            ax.bar(x,SI,width = barWidth,label='Sensibilité de 1er ordre',color = ['yellow']*len(x),edgecolor = ['blue']*len(x), linewidth = 2)
            ax.bar(x2,ST,width = barWidth,label='Indice de sensibilité total',color = ['pink']*len(x),edgecolor = ['green']*len(x), linewidth = 2)
            ax.legend()
            ax.set_xticklabels(labels)
            ax.set_xticks(range(len(SI)))
            ax.set_ylabel("Indices de sensibilité de premier ordre et totaux de Sobol")
            fig.canvas.set_window_title(self.project.name+" >> "+"Analyse de Sensibilité"+" >> "+s.name)
            fig.show()
            
            
        

class project_panel_disp(wx.ScrolledWindow):
      def __init__(self,parent,main_frame):
        self.main_frame=main_frame
        super().__init__(parent) 
        #splitter = wx.SplitterWindow(self, -1, wx.Point(0, 0),wx.Size(400, -1), wx.SP_3D)
        #self.html = html.HtmlWindow(splitter)
        #self.html2 = html.HtmlWindow(splitter)
        #splitter.SplitVertically(self.html, self.html2)
        self.html = html_result(self)
        sizer = wx.BoxSizer()
        #sizer.Add(splitter,-1, wx.EXPAND) 
        sizer.Add(self.html,-1, wx.EXPAND) 
        self.SetSizer(sizer)

"""
    PROJECT CONTENT
"""
class ProjectPanel(wx.Panel):
    def __init__(self,parent,main_frame):
        super().__init__(parent) 
        self.main_frame=main_frame
        splitter = wx.SplitterWindow(self, -1, wx.Point(0, 0),wx.Size(400, -1), wx.SP_3D)
        
        setattr(main_frame,'project_panel_config',project_panel_config(splitter,main_frame))
        setattr(main_frame,'project_panel_disp',project_panel_disp(splitter,main_frame))
        splitter.SplitHorizontally(main_frame.project_panel_config, main_frame.project_panel_disp)
        
        sizer = wx.BoxSizer()
        sizer.Add(splitter,-1, wx.EXPAND) 
        self.SetSizer(sizer) 
"""
    END PROJECT CONTENT
"""
"""
    MENU OPTIONS
    
"""
class menu_options(wx.Dialog):
    def __init__(self,main_frame):
        self.main_frame=main_frame
        super(menu_options, self).__init__(main_frame, title = main_frame.dict.menu_options.title,size=(-1, 200)) 
        panel = wx.Panel(self) 
        sizer = wx.BoxSizer(wx.VERTICAL) 
        
        btn = wx.Button(panel, -1, label = "OK")
        btn.Bind(wx.EVT_BUTTON,self.OnOk) 
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
        lang_label = wx.StaticText(panel, -1, main_frame.dict.menu_options.lang) 
        hbox1.Add(lang_label, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        choices_langs=[]
        for l in main_frame.dict.menu_options.langs:
            choices_langs.append(l.encode('cp1252'))
        
        self.langs = wx.ComboBox(panel,  choices = choices_langs)
        hbox1.Add(self.langs,1,wx.EXPAND) 
        self.langs.SetSelection(main_frame.config.lang)
        
        #bind
        self.langs.Bind(wx.EVT_COMBOBOX, self.OnLangs) 
        
        sizer.Add(hbox1,)
        sizer.Add(btn,0,1)
        panel.SetSizer(sizer) 
        #sizer.Fit(self)
    def OnLangs(self,e):
        pass
    def OnOk(self,e):
        if not self.main_frame.config.lang == self.langs.GetSelection():
            self.main_frame.config.lang=self.langs.GetSelection()
            self.main_frame.save_config()
            self.main_frame.Close()
            MainFrame().Show()
        self.Destroy()
        
"""
    MAIN FRAME
"""

class MainFrame(wx.Frame):
    def __init__(self):
        
        self.projects={}
        self.sim_dyn={'main':None}
        print(os.path.dirname(sys.argv[0]))
        # DICT ================================================================
        self.config_filename=os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",'config.json')
        self.dict_filename=os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",'dict.json')
        print(self.config_filename)
        file = open(self.config_filename,'r')
        self.config=obj__(json.loads(file.read()))
        file.close()
        file = open(self.dict_filename,'r')
        self.dict__=obj__(json.loads(file.read()))
        file.close()

        
        w = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        h = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)
        super().__init__(parent=None, title=self.dict.title,pos=(int(w/4), int(h/4)) ,size=(int(2*w/4),int(2*h/4)) )
        splitter = wx.SplitterWindow(self, -1,wx.Point(0, 0),wx.Size(300, -1), wx.SP_3D) 
        self.project_tree = ProjetTree(splitter,self)
        project_content = ProjectPanel(splitter,self)
        splitter.SplitVertically(self.project_tree, project_content)
        
        # set icon
        icon = wx.Icon()
        im_ = os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",self.icons.main_frame)
        icon.CopyFromBitmap(wx.Bitmap(im_, wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)
        # Setting up the menu.
        filemenu= wx.Menu()
        helpmenu= wx.Menu()
        toolsmenu= wx.Menu()
        
        self.menuNew = filemenu.Append(wx.ID_NEW,self.dict.new)
        filemenu.AppendSeparator()
        self.menuOpen = filemenu.Append(wx.ID_OPEN, self.dict.open)
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT,self.dict.exit)
        
        menuExit.SetBitmap(wx.Bitmap(os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",self.icons.logout)))
        self.menuNew.SetBitmap(wx.Bitmap(os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",self.icons.new)))
        self.menuOpen.SetBitmap(wx.Bitmap(os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",self.icons.open)))
        
        menuAbout= helpmenu.Append(wx.ID_ABOUT, self.dict.about.encode('cp1252'))
        menuAbout.SetBitmap(wx.Bitmap(os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",self.icons.chat)))
        menuLicence= helpmenu.Append(wx.ID_INFO, self.dict.lic)
        menuLicence.SetBitmap(wx.Bitmap(os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",self.icons.licence)))
        
        menuOptions=toolsmenu.Append(-1, self.dict.options)
        menuOptions.SetBitmap(wx.Bitmap(os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",self.icons.setting)))

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,self.dict.file) # Adding the "filemenu" to the MenuBar
        menuBar.Append(toolsmenu,self.dict.tools)
        menuBar.Append(helpmenu,self.dict.help)

        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        
        # binds
        self.Bind(wx.EVT_MENU, self.OnOptions, menuOptions)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnLicence, menuLicence)
        
        #self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnProjectEndEdit)
        
        self.ToolBar = wx.ToolBar( self, -1 ) 
        
        self.ToolBar.AddTool(1, "Analyse Pinch", wx.Bitmap(os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",self.icons.run1)), shortHelp="Analyse Pinch", ) 
        self.ToolBar.AddTool(2, "Sensitivity_Analysis", wx.Bitmap(os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",self.icons.sensi)), shortHelp="Analyse de sensibilité\nEffet des paramètres de l'inventaire sur l'analyse Pinch", ) 
        self.ToolBar.AddTool(3, "Export to Excel", wx.Bitmap(os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",self.icons.excel)), shortHelp="Convertir en Excel\nNon dispo dans la version actuelle", ) 
        self.ToolBar.AddTool(4, "Export to pdf", wx.Bitmap(os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",self.icons.pdf)), shortHelp="Rapport d'analyse\nNon dispo dans la version actuelle", ) 
        #tb.AddTool(2, "run pinch1", wx.Bitmap(os.path.join(self.icons.run1)), shortHelp="run mono" )
        #runbtn = wx.Button(tb , 0, "RUN")
        self.ToolBar.Realize() 
        self.ToolBar.Bind(wx.EVT_TOOL_ENTER, self.Ontbright)
        
        sizer = wx.BoxSizer()
        sizer.Add(splitter,-1, wx.EXPAND,-1) 
        self.SetSizer(sizer) 
        
        self.fernet=None
        self.inf={}
        self.lic_manager()
        

        
    def Ontbaction(self,e):
            project=self.get_selected_project()
            if project and e.GetId()==1:
                print("run...")
                project.pinch()
                setattr(self.project_panel_disp.html,"project",project)
                self.project_panel_disp.html.SetPage(project.mono['html']['main'])
            if project and e.GetId()==2:
                class CellDialog(wx.Dialog):
                    def __init__(self, parent): 
                        super(CellDialog, self).__init__(parent, title = project.name, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,size=(600,400)) 
                        icon = wx.Icon()
                        im_ = os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim",parent.icons.sensi)
                        icon.CopyFromBitmap(wx.Bitmap(im_, wx.BITMAP_TYPE_ANY))
                        self.SetIcon(icon)
                        splitter = wx.SplitterWindow(self, -1, wx.Point(0, 0),wx.Size(600, -1), wx.SP_3D)
                        panel = wx.Panel(splitter) 
                        sizer = wx.BoxSizer(wx.VERTICAL) 
                        subs=box_check_lstct(panel,"Type d'analyse ?", style=wx.LC_REPORT|wx.LC_SINGLE_SEL,size=wx.DefaultSize)
                        subs.InsertColumn(0, "No.")
                        subs.InsertColumn(1, "Pollutant")
                        subs.InsertColumn(2, "Description")
                        for i,s in enumerate(project.data.subs):
                            subs.Append([str(i), s.name, s.desc])  
                        #subs.Bind(wx.EVT_LISTBOX_DCLICK, self.OnSelect)
                        
                        btn = wx.Button(panel, -1, label = "Analyse")
                        btn.Bind(wx.EVT_BUTTON,self.OnAnalyse) 
                        
                        self.N=box_input(panel,"Taille d'échantillons à générer",0)
                        self.N.SetValue("1000")
                        
                        # _2ndorder_sizer=wx.BoxSizer(wx.HORIZONTAL) 
                        # self._2ndorder = wx.CheckBox(panel,-1,label="Calculer les sensibilités de second ordre")
                        # _2ndorder_sizer.Add(self._2ndorder,0, wx.ALL|wx.CENTER)
                        # self._2ndorder.SetValue(True)
                        
                        self.method=box_lst(panel,"Méthode d'analyse", choices=["Sobol, Monte Carlo","Fractional Factorial","Morris Analysis"])
                        self.method.SetSelection(0)
                        
                        # self.conf=box_input(panel,"Intervalle de confiance",0)
                        # self.conf.SetValue("0.95")
                        
                        self.htm = html_result(splitter)
                        setattr(self.htm ,'project',project)
                        
                        
                        sizer.Add(subs.sizer, 0, wx.ALL|wx.EXPAND, 5)
                        sizer.Add(self.N.sizer, 0, wx.ALL, 5)
                       # sizer.Add(_2ndorder_sizer, 0, wx.ALL, 5)
                        #sizer.Add(self.conf.sizer, 0, wx.ALL, 5)
                        sizer.Add(self.method.sizer, 0, wx.ALL, 5)
                        sizer.Add(wx.StaticLine(panel), 0, wx.ALL|wx.EXPAND, 5)
                        sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
                        #sizer.Add(self.htm,1,wx.EXPAND,1)
                        
                        panel.SetSizerAndFit(sizer) 
                   
                        self.subs=subs
                        # self.sizer=sizer
                        main_sizer = wx.BoxSizer()
                        splitter.SplitVertically(panel, self.htm)
                        main_sizer.Add(splitter,-1, wx.EXPAND) 
                        self.SetSizer(main_sizer)
                       # main_sizer.Fit(self)
                        

                    def OnAnalyse(self,e):
                        subs_index = self.subs.GetFirstSelected()
                        if subs_index >-1:
                            subs = project.data.subs[subs_index]
                            htm = project.sensitivity_analysis(subs,int(self.N.GetValue()))
                            self.htm.SetPage(htm)
                            
                            #number of samples to generate
                            
                        # win_main = sim_dyn_popup(self.Parent,(project,project.data.subs[e.GetSelection()]))
                        # btn = e.GetEventObject()
                        # pos = btn.ClientToScreen( (0,0) )
                        # sz =  btn.GetSize()
                        # win_main.Position(pos, (0, sz[1]))
                        # win_main.Show(True)
                        # win_main.SetSize( (400,200) )
                        # win_main.htm.SetPage("<html><center>"+project.name+", Analyse "+project.data.subs[e.GetSelection()].name+"</center></html>")
                        # self.Destroy()
                
                CellDialog(self,).Show()
                
        
    def Ontbright(self,e):
            project=self.get_selected_project()
            if project:
                e.GetEventObject().SetToolShortHelp(1,"Analuse Pinch >> "+project.name)
            
    def get_selected_project(self):
        if self.projects:
            item=self.project_tree.tree.GetSelection()
            data = self.project_tree.tree.GetItemData(item)
            if isinstance(data,__project__):
                return data
        return None
    def OnProjectSelection(self,e):
        project=self.project_tree.tree.GetItemData(e.GetItem())
        if isinstance(project,__project__):
            self.project_tab.update(project)
            self.subs_tab.update(project)
            self.loc_tab.update(project)
            self.post_tab.update(project)
            self.sink_tab.update(project)
            self.source_tab.update(project)
            self.cons_tab.update(project)
        else:
            self.project_tab.update()
            self.subs_tab.update()
            self.loc_tab.update()
            self.post_tab.update()
            self.sink_tab.update()
            self.cons_tab.update()
    def lic_manager(self,lic_notif=False):
       
        if path.exists(os.path.join(sys.exec_prefix,"wpinch.lic")):
            file = open(os.path.join(sys.exec_prefix,"wpinch.lic"), 'rb')  # Open the file as wb to read bytes
            self.fernet = Fernet(file.read())
            file.close()
            with open(os.path.join(sys.exec_prefix,"Lib\site-packages\WaterOptim","inf.enc"), 'rb') as f:
                data = f.read()  # Read the bytes of the encrypted file
                try:
                    self.inf = json.loads(self.fernet.decrypt(data))
                    self.Bind(wx.EVT_MENU, self.OnOpen, self.menuOpen)
                    self.Bind(wx.EVT_MENU, self.OnNew, self.menuNew)
                    self.ToolBar.Bind(wx.EVT_TOOL, self.Ontbaction)
                    self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnProjectSelection)
                                # Events.
                    # self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnProjectEndEdit)
                    if lic_notif:
                        wx.MessageBox('Hello from AgroParisTech', 'Info', wx.OK | wx.ICON_INFORMATION)
                except InvalidToken as e:
                    print("Invalid Key - Unsuccessfully decrypted")
        else:
            pass
            
    @property
    def dict(self):
        return getattr(self.dict__,self.dict__.langs[self.config.lang])
    @property
    def icons(self):
        return self.config.icons
    def OnOptions(self,e):
        menu_options(self).ShowModal() 
    def save_config(self):
        with open(self.config_filename, 'w') as outfile:
            json.dump(self.config.toJSON(), outfile)
    def OnExit(self,e):
        self.Close(True)
    def OnAbout(self,e):
        if self.inf:
            info = wx.adv.AboutDialogInfo()
            info.SetName(self.inf['name'])
            info.SetDescription(self.inf['desc'])
            info.SetLicence(self.inf['lic'])
            info.AddDeveloper(self.inf['author'])
            info.SetVersion(self.inf['version'])
            info.SetCopyright(self.inf['copyright'])
            info.SetWebSite(self.inf['web'])
            wx.adv.AboutBox(info)
    def OnLicence(self,e):
        """ Open a file"""
        dlg = wx.FileDialog(self, "Choose a file", "", "", "*.lic*",style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST )
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetDirectory()
            filename =dlg.GetFilename()
            file = open(os.path.join(dirname, filename), 'rb')  # Open the file as wb to read bytes
            key = file.read()  # The key will be type bytes
            file.close()
            file = open(os.path.join(sys.exec_prefix, filename), 'wb')  # Open the file as wb to write bytes
            file.write(key)  # The key is type bytes still
            file.close()
            if not self.inf:
                self.lic_manager(True)
                  

                    
        dlg.Destroy()
    def OnOpen(self,e):
        dlg = wx.FileDialog(self, self.dict.select_file, "", "", "*.json*",style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
        dlg.SetSize((100,100)) 
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetDirectory()
            for filename in dlg.GetFilenames():
                with open(os.path.join(dirname, filename),"r") as json_file:
                    if not (filename,dirname) in list(map(lambda x:(x.filename,x.dirname),self.projects.values())):
                        project=__project__(self,filename,dirname,data=json.load(json_file))
                        self.projects[project.uuid]=project
                        self.project_tree.AppendItem(project.name,data=project,) 
                        # #update attr of the project
                        # project.save()
                    
        dlg.Destroy()
    def OnNew(self,e):
        dlg = wx.FileDialog(self, self.dict.on_new_project.title, os.getcwd(), "", "*.json", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT,) 
        dlg.SetSize((100,100)) 
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            if not (filename,dirname) in list(map(lambda x:(x.filename,x.dirname),self.projects.values())):
                project=__project__(self,filename,dirname)
                self.projects[project.uuid]=project
                self.project_tree.AppendItem(project.name,data=project,) 
                project.save()
        dlg.Destroy()

def pinch():
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
    
"""
   END MAIN FRAME
"""        
if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()