# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 06:54:41 2021

@author: HEDI
"""
import json
import copy
from numpy import array,diff,cumsum,multiply,argmin,unique,polyfit,polyval,linspace,concatenate,around,zeros,dot
from prettytable import PrettyTable
from bs4 import BeautifulSoup
from pandas import DataFrame
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import minimize


BLACK,RED,GREEN,RED2,BLUE,PURPLE,SKYBLUE,GREY,GREY2,RED3,GREEN2,YELLOW,BLUE2,PURPLE2,BLUE3,WHITE=map(lambda x: ''.join(('\x1b[$;5;',str(x),'m')),range(16))
CEND='\x1b[0m'
def fgc(c):
    return c.replace("$",'38')
def bgc(c):
    return c.replace("$",'48')
def line(label='',n=20,marker='-',c=GREY,bg=BLACK):
    if label:
        label=label.join([' ']*2)
    for i in range(n):
        print(marker, end='', flush=True)
    print(bgc(bg)+fgc(c)+label+CEND, end='', flush=True)
    for i in range(n):
        print(marker, end='', flush=True)
    print()
def label(txt,c=GREY,bg=BLACK):
    return bgc(bg)+fgc(c)+txt+CEND

def formatting(val,d=0):
    return ('{:.'+str(d)+'f}').format(val)

def nlabel(val,d=0,c=WHITE,bg=BLACK,paint=None):
    if paint:
        val= formatting(val,d=d).join(tuple(map(lambda x: x,paint)))
    else:
        val= formatting(val,d=d)
    return bgc(bg)+fgc(c)+val+CEND

def hlabel(txt,c="#D7DBDD",bg="#17202A"):
    return "<font color="+c+" bgcolor="+bg+">"+txt+"</font>"

def hnlabel(val,d=0,c="#FDFEFE",bg="#17202A",paint=None):
    if paint:
        val= formatting(val,d=d).join(tuple(map(lambda x: x,paint)))
    else:
        val= formatting(val,d=d)
    return "<font color="+c+" bgcolor="+bg+">"+val+"</font>"

    

json_schema={"post":{'name':'','cin_max':0,"cout_max":0,'mc':0,'loc':'',"regen":{},"priority":100,},
             "regen":{'R':0,'loc':'','f':0,'a':0,"priority":100},
             "pinch":{"posts":[],'sources':[],'sinks':[]},
             'sink':{'name':'','loc':'','cin_max':0,'m':0},
             'source':{'name':'','loc':'','c':0,'m':0,"priority":100},
             'design_source':{'type':'','parent':None,'m':0,'c':0,},
            }


class ptable(PrettyTable):
    def to_excel(self,filename):
        list_header = [] 
        data=[]
        soup = BeautifulSoup(self.get_html_string(),features="lxml")
        header = soup.find_all("table")[0].find("tr") 
        for items in header: 
            try: 
                list_header.append(items.get_text()) 
            except: 
                continue
        HTML_data = soup.find_all("table")[0].find_all("tr")[1:]
        for element in HTML_data: 
            sub_data = [] 
            for sub_element in element: 
                try: 
                    sub_data.append(sub_element.get_text()) 
                except: 
                    continue
            data.append(sub_data)   
        dataFrame = DataFrame(data = data, columns = list_header)  
        dataFrame.to_excel (filename+'.xlsx',index=False,sheet_name=filename)             
            
class __obj__:
    def __init__(self,schema={}):
        if schema:
            schema = copy.deepcopy(schema)
            for k,v in schema.items():
                # if isinstance(v,dict):
                #     setattr(self,k,__obj__(json_schema[k]))
                # else:
                setattr(self,k,v)
    def toJSON(self):
        obj = {}
        for x in json_schema[self.__class__.__name__[2:-2]]:
            v = getattr(self,x)
            if isinstance(v,__obj__):
                v = v.toJSON()
            elif isinstance(v,list):
                v=list(map(lambda l:l.toJSON(),v))    
            obj[x]=v

        return json.loads(json.dumps(obj,))

    def __repr__(self):
        return json.dumps(self.toJSON(), indent=2)
    @property
    def key(self):
        return str(id(self))
class __regen__(__obj__):
    def __init__(self,post,data):
        self.post=post
        super().__init__(json_schema['regen'])
        self.tmp={'w_out':{},'w_supp':0}
        for k,v in data.items():
            setattr(self,k,v)
        

    @property
    def co(self):
        return self.post.cout_max*(1-self.R/100)# 0 rien n'est traité, 1 traitement jusqu'à 0 ppm
        
    def m(self,a=None):
        """
        Parameters
        ----------
        a : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        TYPE
            a = 0 return lb
            a = 1 return ub
            default lb
        """
        if a ==None:
            a = self.a
        return self.f/100*(self.post.m_lb+(self.post.m_ub-self.post.m_lb)*a)
class __post__(__obj__):
    def __init__(self,pinch,data):
        self.pinch=pinch
        super().__init__(json_schema['post'])
        self.tmp = {'w_supp':0,'int_c':0,'mc':{},'w_in':{},'w_out':{}}
        for k,v in data.items():
            if k=='regen':
                self.regen=__regen__(self,v)
            else:
                setattr(self,k,v)
    @property
    def isregen(self):
            return self.regen and self.regen.R>0 and self.regen.f>0
    def includes(self,c1,c2):
        return c1 >= self.cin_max and c2 <= self.cout_max
    @property
    def m_ub(self):
        return self.mc/(self.cout_max-self.cin_max)*1000 
    @property
    def m_lb(self):
        return self.mc/self.cout_max*1000
    @property
    def m_b(self):
        return[self.m_lb,self.m_ub]   
    def pollution_transfer(self):
        patterns = ('.', '..', 'o', '\\\\', 'x','//' )
        intervals=[]
        sources=set()
        for k,v in self.tmp['mc'].items():
            for v1 in v:
                sources.add(v1[2])
        sources=list(sources)
        data={}
        for k,v in self.tmp['mc'].items():
            for s1 in sources:
                data[(k,s1)]=[0,0]
            for v1 in v:
                mc_,mw_,s = v1
                data[(k,s)][0]+=mc_
                data[(k,s)][1]+=mw_
            intervals.append('['+formatting(k[0])+','+formatting(k[1])+']')
        
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        xdata = range(len(self.tmp['mc'].items()))
        ydata=[]
        for i,s in enumerate(sources):
            if i==0:
                bottom=zeros(len(xdata))
            else:
                bottom=bottom+array(ydata)
            ydata=[]
            mw=0
            for k,v in data.items():
                if k[1]==s:
                    ydata.append(v[0])
                    mw+=v[1]
                
            ax.bar(xdata,ydata,bottom=bottom,
                   label=s.name+' ('+formatting(mw,d=2)+' m3/h)',
                   hatch=patterns[i],edgecolor='black',)
        ax.set_xticks(xdata,)
        ax.set_xticklabels(intervals)
        ax.legend(loc=0)
        ax.set_xlabel('Intervals ppm')
        ax.set_ylabel('Pollution transfer kg/h')
        
    def get_ww(self):
        return self.tmp["w_supp"]-sum(list(map(lambda x: x,self.tmp["w_out"].values())))
        
    def html_balances(self):
        def addcell(v,bg="",c=""):
            v=str(v)
            if bg:
                bg="bgcolor="+bg
            if c:
                v="<font color="+c+">"+v+"</font>"
            return "<td "+bg+">"+v+"</td>"
        tot_cell_label = addcell("Total",bg="#85929E",c="#D5F5E3")
        tot_cell_val = lambda v:addcell(formatting(v,d=2),bg="#3498DB",c="#FDFEFE")
        c_cell = lambda c1,c2:addcell(formatting(c1) +"<font bgcolor='#FCF3CF'>["+formatting(c2)+"]</font>")
        mc_cell = lambda c1,c2:addcell(formatting(c1,d=2) +"<font bgcolor='#FCF3CF'>["+formatting(c2,d=2)+"]</font>")
        
            
        html_input_balance ="<table border=1>"
        html_output_balance ="<table border=1>"
        html_pollution_transfer ="<table border=1>"
        
        # head
        for x in ["Stream","ppm","m3/h"]:
            html_input_balance+= "<th>"+x+"</th>"
            html_output_balance+= "<th>"+x+"</th>"
        html_input_balance+="</tr>"
        html_output_balance+="</tr>"
        for x in ['Interval ppm','Transfer kg/h','Water m3/h','']:
            html_pollution_transfer+= "<th>"+x+"</th>"
        html_pollution_transfer+="</tr>"
        
        
        # inputs
        if self.isregen:
            w_supp_regen = self.regen.tmp['w_supp']
        else:
            w_supp_regen=0
        c_in_moy = 0
        for s,mw_ in self.tmp["w_in"].items():
            c_in_moy+=s.c*mw_
            html_input_balance+="<tr>"
            for x in [s.name,around(s.c),formatting(mw_,d=2)]:
                html_input_balance+=addcell(x)
            html_input_balance+="</tr>"
        html_input_balance+="<tr>"
        html_input_balance+= tot_cell_label
        html_input_balance+= c_cell(c_in_moy/self.tmp["w_supp"],self.cin_max)
        html_input_balance+= tot_cell_val(self.tmp["w_supp"])
        html_input_balance+="</tr>"
        #outputs
        m_out=0
        for s,mw_ in self.tmp["w_out"].items():
            m_out+=mw_
            html_output_balance+="<tr>"
            html_output_balance+=addcell(s.name)
            html_output_balance+=c_cell(self.cout_max,self.cin_max)
            html_output_balance+=addcell(formatting(mw_,d=2))
            html_output_balance+="</tr>"
        m_ww = self.tmp['w_supp']-w_supp_regen-m_out
        if self.isregen:
            html_output_balance+="<tr>"
            html_output_balance+=addcell("REGEN")
            html_output_balance+=addcell(formatting(self.cout_max))
            html_output_balance+=addcell(formatting(w_supp_regen,d=2))
            html_output_balance+="</tr>"
        html_output_balance+="<tr>"
        html_output_balance+=addcell("Wastewater")
        html_output_balance+=addcell(formatting(self.cout_max))
        html_output_balance+=addcell(formatting(m_ww,d=2))        
        html_output_balance+="</tr>"
        html_output_balance+="<tr>"
        html_output_balance+=tot_cell_label
        html_output_balance+=addcell(formatting(self.cout_max))
        html_output_balance+=tot_cell_val(m_out+m_ww+w_supp_regen)
        html_output_balance+="</tr>"
        # pollution transfer
        mw_t=0
        mc_t=0
        for k,v in self.tmp['mc'].items():
            for v1 in v:
                mc_,mw_,s=v1
                mc_t+=mc_
                if not s==self:
                    mw_t+=mw_
                    name=addcell(s.name)
                    mw_=addcell(formatting(mw_,d=2))
                else:
                    name=addcell('Inner transfer',c="#C39BD3")
                    mw_=addcell(formatting(mw_,d=2),c="#C39BD3")
                html_pollution_transfer+="<tr>"
                html_pollution_transfer+=addcell('['+formatting(k[0])+','+formatting(k[1])+']')
                html_pollution_transfer+=addcell(formatting(mc_,d=2))
                html_pollution_transfer+=mw_
                html_pollution_transfer+=name
                html_pollution_transfer+="</tr>"
        html_pollution_transfer+="<tr>"
        html_pollution_transfer+=tot_cell_label
        html_pollution_transfer+=mc_cell(mc_t,self.mc)
        html_pollution_transfer+=tot_cell_val(mw_t)
        html_pollution_transfer+=addcell("")
        html_pollution_transfer+="</tr>"       
        
        
        return html_input_balance,html_output_balance,html_pollution_transfer
        
        
    def balance(self):
        html_balance=''
        if self.isregen:
            w_supp_regen = self.regen.tmp['w_supp']
        else:
            w_supp_regen=0
        line(label='Mass Balance ('+self.name+')',n=30,marker='=')
        print(label('INPUTS:',c=YELLOW))
        t=PrettyTable(field_names=["Stream","ppm","m3/h"])
        t.align='l'
        c_in_moy = 0
        for s,mw_ in self.tmp["w_in"].items():
            c_in_moy+=s.c*mw_
            t.add_row([s.name,around(s.c),formatting(mw_,d=2)])
        t.add_row([label('Total'),
                   formatting(c_in_moy/self.tmp["w_supp"])+nlabel(self.cin_max,paint='[]',c=BLUE2),
                   nlabel(self.tmp["w_supp"],d=2,c=WHITE,bg=BLUE)
                   ])
        print(t)
        html_balance=t.get_html_string()
        t.clear_rows()
        m_out=0
        
        for s,mw_ in self.tmp["w_out"].items():
            m_out+=mw_
            t.add_row([s.name,
                       formatting(self.cout_max)+nlabel(self.cin_max,paint='[]',c=BLUE2),
                       formatting(mw_,d=2)])
        m_ww = self.tmp['w_supp']-w_supp_regen-m_out
        if self.isregen:
            t.add_row(['REGEN',
                   formatting(self.cout_max),
                   nlabel(w_supp_regen,d=2,c=BLACK,bg=BLUE2)
                       ])
        t.add_row(['WasteWater',
                   formatting(self.cout_max),
                   nlabel(m_ww,d=2,c=GREEN2)
                   ])

        t.add_row([label('Total'),
                   formatting(self.cout_max),
                   nlabel(m_out+m_ww+w_supp_regen,d=2,c=WHITE,bg=BLUE)
                   ])
        print(label('OUTPUTS:',c=YELLOW))
        print(t)
        if self.isregen:
            t.clear_rows()
            t.add_row(['Total REGEN',formatting(self.cout_max),
                       nlabel(w_supp_regen,d=2,c=BLACK,bg=BLUE2)
                       ])
            m_out=0
            for s,mw_ in self.regen.tmp['w_out'].items():
                m_out+=mw_
                t.add_row([s.name,nlabel(s.cin_max,paint='[]',c=BLUE2),
                           formatting(mw_,d=2)])
            m_ww=w_supp_regen-m_out
            if m_ww:
                t.add_row(['WasteWater',formatting(self.regen.co),
                           nlabel(m_ww,d=2,c=GREEN2)
                           ])
            print(label('REGEN:',c=YELLOW))
            print(t)
        t=PrettyTable()
        t.field_names=['Interval ppm','Transfer kg/h','Water m3/h','']
        t.align='l'
        mw_t=0
        mc_t=0
        for k,v in self.tmp['mc'].items():
            for v1 in v:
                mc_,mw_,s=v1
                mc_t+=mc_
                if not s==self:
                    mw_t+=mw_
                    name=s.name
                    mw_=formatting(mw_,d=2)
                else:
                    name=label('Inner transfer',c=PURPLE)
                    mw_=nlabel(mw_,d=2,c=PURPLE)
                t.add_row(['['+formatting(k[0])+','+formatting(k[1])+']',formatting(mc_,d=2),mw_,name
                ])
        t.add_row([label('Total'),formatting(mc_t,d=2)+nlabel(self.mc,paint='[]',c=GREY),nlabel(mw_t,d=2,c=WHITE,bg=BLUE),""
                ])
        print(label('Pollution Transfer:',c=YELLOW))    
        print(t)
        line(label='Mass Balance ('+self.name+')',n=30,marker='=')
        return html_balance
            
class __sink__(__obj__):
    def __init__(self,pinch,data):
        self.pinch=pinch
        super().__init__(json_schema['sink'])
        self.tmp = {'w_supp':0,'w_in':{}}
        for k,v in data.items():
            setattr(self,k,v)
    def balance(self):
        line(label='Mass Balance ('+self.name+')',n=30,marker='=')
        print(label('INPUTS:',c=YELLOW))
        t=PrettyTable(field_names=["Stream","ppm","m3/h"])
        t.align='l'
        m_tot=0
        c_moy=0
        for s,mw_ in self.tmp["w_in"].items():
            m_tot+=mw_
            c_moy+=s.c*mw_
            t.add_row([s.name,formatting(s.c)+nlabel(self.cin_max,paint='[]',c=BLUE2),formatting(mw_,d=2)])
        t.add_row([label('Total'),
                    formatting(c_moy/m_tot)+nlabel(self.cin_max,paint='[]',c=BLUE2),
                    formatting(m_tot,d=2)+nlabel(self.m,d=2,c=WHITE,bg=BLUE,paint='[]')
                    ])
        print(t)
class __source__(__obj__):
    def __init__(self,pinch,data):
        self.pinch=pinch
        super().__init__(json_schema['source'])
        self.tmp = {'w_out':{}}
        for k,v in data.items():
            setattr(self,k,v)    
    def balance(self):
        line(label='Mass Balance ('+self.name+')',n=30,marker='=')
        print(label('OUTPUTS:',c=YELLOW))
        t=PrettyTable(field_names=["Stream","ppm","m3/h"])
        t.align='l'
        m_tot=0
        for s,mw_ in self.tmp["w_out"].items():
            m_tot+=mw_
            t.add_row([s.name,formatting(self.c)+nlabel(s.cin_max,paint='[]',c=BLUE2),formatting(mw_,d=2)])
        mww=self.m-m_tot
        t.add_row([label('Wastewater'),
                   formatting(self.c),
                   formatting(mww,d=2)
                   ])
        t.add_row([label('Total'),
                   formatting(self.c),
                   formatting(m_tot+mww,d=2)+nlabel(self.m,d=2,c=WHITE,bg=BLUE,paint='[]')
                   ])
        print(t)
        
# ===========================CASCADE========================================                
class __cascade__:
    def __init__(self,pinch):
        S=[]
        D=[]
        c=set([0,1e6])
        for p in pinch.posts:
            c.add(p.cin_max)
            c.add(p.cout_max)
            D.append({'c':p.cin_max,'m':p.m_ub})
            if p.isregen:
                S.append({'c':p.regen.co,'m':p.regen.m()})
                S.append({'c':p.cout_max,'m':p.m_ub-p.regen.m()})
                c.add(p.regen.co)
            else:
                S.append({'c':p.cout_max,'m':p.m_ub})
        for s in pinch.sources:
            S.append({'c':s.c,'m':s.m})
            c.add(s.c)
        for s in pinch.sinks:
            D.append({'c':s.cin_max,'m':s.m})
            c.add(s.cin_max)  
        c=sorted(c)
        # net water source/demand
        nwsd =  [0]*len(c)
        for i in range(len(c)):
            for x in list(filter(lambda x:x['c']==c[i],D)):
                nwsd[i]-=x['m']
            for x in list(filter(lambda x:x['c']==c[i],S)):
                nwsd[i]+=x['m']
        #purity
        p = 1-array(c)/1e6
        dp=-diff(p)
        cwsd=cumsum(nwsd)# cumulative water source/demand
        pwf = multiply(dp,cwsd[:-1])# pure water surplus/deficit pwf
        cpwf  =cumsum(pwf)# cumulative pure water surplus/deficit cpwf
        ffw=cpwf/(1-p[1:])# interval fresh water demand
        self.p=p
        self.c=c
        self.dp=dp
        self.nwsd=nwsd
        self.cwsd=cwsd
        self.pwf=pwf
        self.cpwf=cpwf
        self.ffw=ffw
        self.D=D
        self.S=S
        fw=abs(min(ffw))
        ww=abs(cwsd[-1]+fw)
        pp=argmin(ffw)+1
        self.fw=fw
        self.ww=ww
        self.pp=pp
    
    def __repr__(self):
        return self.__table__(feasible=True).get_string()
    def feasible(self,):
        print(self.__table__(feasible=True))
    def non_feasible(self,):
        print(self.__table__(feasible=False))
    def to_excel(self,filename,feasible=True,m_fact=1,m_d=2):
        self.__table__(feasible=feasible,m_fact=m_fact,m_d=m_d).to_excel (filename) 
    def to_html(self,feasible=True,m_fact=1,m_d=2):
        return self.__table__(feasible=feasible,m_fact=m_fact,m_d=m_d).get_html_string()
    
    def __table__(self,feasible=True,m_fact=1,m_d=2):
         if feasible:
            fw=self.fw
         else:
            fw=0
         cwsd=self.cwsd+fw
         pwf = multiply(self.dp,cwsd[:-1])
         cpwf  =cumsum(pwf)
         ffw=cpwf/(1-self.p[1:])
         t =  ptable()
         t.field_names=['C ppm','Purity','Purity Difference','NWSD','CWSD','PWF','CPWF','FFW']
         n=len(self.c)
         t.add_row(['-','-','-','-','fw='+formatting(fw*m_fact,m_d),'','',''])
         for i in range(n):
             cpwf_,ffw_=['','']
             if i:
                 cpwf_=formatting(cpwf[i-1]*m_fact,m_d)
                 ffw_=formatting(ffw[i-1]*m_fact,m_d)
             
             row=[formatting(self.c[i]),
                       formatting(self.p[i],6),
                       '',
                        formatting(self.nwsd[i]*m_fact,m_d),
                        '','',
                        cpwf_,
                        ffw_]
             if i==self.pp:
                 row=list(map(lambda x:'{'+x+'}',row))
             t.add_row(row)
             if i<n-1:
                 t.add_row(['','',
                       formatting(self.dp[i],6),
                       '',
                       formatting(cwsd[i]*m_fact,m_d),
                       formatting(pwf[i]*m_fact,6),
                       '',''])
         t.add_row(['-','-','-','-',
             'ww='+formatting(cwsd[-1]*m_fact,m_d),
             '','',''])
         return t
"""
    DESIGN
"""
class __design_source__(__obj__):
        def __init__(self,data):
            super().__init__()
            for k,v in data.items():
                setattr(self,k,v)
        def capacity(self,c):
            return self.m*(c-self.c)/1000
        @property
        def key(self):
            #return (self.type,self.parent,self.c)
            if self.type=="fw":
                return self.type
            if self.type=="r":
                return self.parent.regen.key
            return self.parent.key
        @property
        def priority(self):
            if self.type=='fw':
                return 1000
            if self.parent:
                if self.type=="r":
                    return self.parent.regen.priority
                else:
                    return self.parent.priority
            return 100
        @property
        def name(self):
            if self.parent:
                if self.type=="r":
                    return self.parent.name+' (regen)'
                else:
                    return self.parent.name
            return self.type
        def update(self,obj,mw):
            self.m-=mw
            if self.type in ["s","p"]:
                if not obj in self.parent.tmp['w_out'].keys():
                     self.parent.tmp['w_out'][obj]=0
                self.parent.tmp['w_out'][obj]+=mw
            elif self.type=='r':
                if not obj in self.parent.regen.tmp["w_out"].keys():
                     self.parent.regen.tmp["w_out"][obj]=0
                self.parent.regen.tmp["w_out"][obj]+=mw
                                
                                   
                                
                                
                                
        
class __design_sources__(dict):
    def __init__(self):
        super().__init__()
    def add(self,data):
        s = __design_source__(data)
        self[s.key]=s
    def __repr__(self):
        sources=list(self.values())
        return str(sources)
    def filter(self):
        return list(filter(lambda x:x.m,self.values()))
    def select_for_post(self,c_lim,verbose):
        sources = []
        for s in self.values():
            if s.c<c_lim and s.m > 1e-4:
                sources.append(s)
        if verbose:
                label(str(len(sources))+' SOURCES found',c=YELLOW)
        if sources:
            sources=sorted(sources, key=lambda s: s.capacity(c_lim) and s.priority) 
            if verbose:
                print(fgc(SKYBLUE),"SOURCE SELECTION",sources[-1].name,around(sources[-1].c),'ppm, ',formatting(sources[-1].m,d=2),'m3/h',CEND)
            return sources[-1]
        else:
            return False
    def select_for_sink(self,c_lim,m):
        sources = []
        for s in self.values():
            if s.c<=c_lim and s.m > 1e-4:
                sources.append(s)
        if sources:
            sources=sorted(sources, key=lambda s: s.m>=m and s.priority) 
            return sources[-1]
        else:
            return False
    def select_for_sink2(self,c_lim,m):
        sources = []
        for s in self.values():
            if  s.m>0:
                sources.append(s)
        if sources:
            c_ = list(map(lambda x:x.c, sources))
            bnds=list(map(lambda x:(0,x.m), sources))
            ub=list(map(lambda x:x.m, sources))
            def obj(x):
                return abs(sum(x)-m)
            cons = ({'type': 'eq', 'fun': lambda x:c_lim+.1-dot(x,c_)/(sum(x)+1e-16)},)
            res = minimize(obj, ub,  bounds=bnds,constraints=cons,method="SLSQP",options={ 'disp': False})
            out={}
            for i in range(len(sources)):
                if res.x[i]>1e-3:
                    out[sources[i]]=res.x[i]
            return out,res
            
        else:
            return False
        
class __design__():
    def __init__(self,pinch,verbose=False):
        MAX_IT=10
        self.pinch=pinch
        c=pinch.cascade.c[:-1]
        fw=pinch.cascade.fw   
        ww=pinch.cascade.ww            
        self.sources=__design_sources__()
        self.sources.add({'type':'fw','parent':None,'c':0,'m':fw,})
        for s in pinch.sources:
            self.sources.add({"type":'s','parent':s,'m':s.m,'c':s.c})
        for p in pinch.posts:
            self.sources.add({"type":'p','parent':p,'m':0,'c':p.cout_max})
            if p.isregen:
                # réserver le min d'eau pour la regen
                m_r = p.regen.m(a=0)
                self.sources.add({"type":'r','parent':p,'m':m_r,'c':p.regen.co})
                p.regen.tmp['w_supp']=m_r
        """
        GROUPING posts
        """
        groups={}
        for i in range(len(c)-1):
            groups[(c[i],c[i+1])]=[]
            for j,p in enumerate(pinch.posts):
                if p.includes(c[i], c[i+1]):
                    groups[(c[i],c[i+1])].append(p)
        self.groups=groups
        self.links={}
        if verbose:
            line(label='Start of Design',marker="=")
            print('Fresh Water',formatting(fw,d=2),'m3/h')
            print('Waste Water',formatting(ww,d=2),'m3/h')
            line(label='INIT SOURCES',)
            t = PrettyTable(field_names=['SOURCE','m3/h'])
            t.align='l'
            for i,s in enumerate(self.sources.values()):
                color=fgc(GREEN)
                if s.m:
                    color=fgc(WHITE)
                t.add_row([color+'SOURCE '+s.name,formatting(s.m,d=2)+CEND])
            print(t)
            line(label='GROUPING')
            t = PrettyTable(field_names=['INTERVAL ppm','POSTS'])
            t.align='l'
            for k,v in groups.items():
                t.add_row([around(k),list(map(lambda x:x.name,v))])
            print(t)
        for k,v in groups.items():
            c1,c2=k
            if verbose:
                line(label='Interval '+str(around(k)))
            for p in v:
                target=p.mc*(c2-c1)/(p.cout_max-p.cin_max)
                if verbose:print(p.name,fgc(WHITE)+'target', formatting(target,d=2),CEND)
                count=0
                while count<MAX_IT and target>1e-6:
                    count+=1
                    if verbose:
                        line(label='Iteration '+str(count),marker='.',n=4)
                    if p.tmp['w_supp']>0:
                        # vérifier la reserve interne précédente !
                        if p.tmp['int_c']<c2:
                            transfer = p.tmp['w_supp']*(c2-p.tmp['int_c'])/1000
                            if not k in p.tmp['mc'].keys():
                                p.tmp['mc'][k]=[]
                            p.tmp['mc'][k].append((transfer,p.tmp['w_supp'],p))
                            target-=transfer
                            p.tmp['int_c']=c2
                            if verbose:
                                print(fgc(GREY),'internal transfer',formatting(transfer,d=2), 'new target',formatting(target,d=2),CEND)
                    if target>1e-6:
                        s= self.sources.select_for_post(c2,verbose)
                        if s:
                            transfer=min(target, s.capacity(c2))
                            target-=transfer # update target
                            mw_=transfer*1000/(c2-s.c) # water supply
                            if not k in p.tmp['mc'].keys():
                                p.tmp['mc'][k]=[]
                            p.tmp['mc'][k].append((transfer,mw_,s))
                            p.tmp['w_supp']+=mw_
                            if not s in p.tmp["w_in"].keys():
                                p.tmp["w_in"][s]=0
                            p.tmp["w_in"][s]+=mw_
                            p.tmp['int_c']=c2

                            # update source
                            #s.m-=mw_
                            s.update(p,mw_)
                            # if s.type=='p':
                            #     if not p in s.parent.tmp['w_out'].keys():
                            #         s.parent.tmp['w_out'][p]=0
                            #     s.parent.tmp['w_out'][p]+=mw_
                            # if s.type=='r':
                            #     if not p in s.parent.regen.tmp["w_out"].keys():
                            #         s.parent.regen.tmp["w_out"][p]=0
                            #     s.parent.regen.tmp["w_out"][p]+=mw_
                            if verbose:
                                print('transfer',formatting(transfer,d=4), 'new target',formatting(target,d=2),'kg/h, ',bgc(BLUE)+formatting(mw_,d=2),'m3/h'+CEND)
                            if p.isregen:
                                if p.tmp['w_supp']*p.regen.f/100>p.regen.tmp['w_supp']:
                                    # balance...
                                    r_diff = p.tmp['w_supp']*p.regen.f/100-p.regen.tmp['w_supp']
                                    #self.sources['r',p,p.regen.co].m+=r_diff
                                    self.sources[p.regen.key].m+=r_diff
                                    p.regen.tmp['w_supp']+=r_diff
                                #self.sources['p',p,p.cout_max].m+=mw_*(1-p.regen.f/100)
                                self.sources[p.key].m+=mw_*(1-p.regen.f/100)
                            else:
                                #self.sources[('p',p,p.cout_max)].m+=mw_
                                self.sources[p.key].m+=mw_
                            
                            if not (s,p) in self.links.keys():
                                self.links[(s,p)]=0
                            self.links[(s,p)]+=mw_
                        else:
                            if verbose:
                                print(fgc(RED)+'No available SOURCES !',CEND)
            # feed sinks
            for sk in pinch.sinks:
                if verbose:
                    if sk.tmp["w_supp"]==0:
                        print(fgc(YELLOW)+sk.name,'target', formatting(sk.m,d=2),'m3/h','Cin_max',formatting(sk.cin_max),'ppm',CEND)
                if sk.cin_max==0 and c1==0:                    
                    while sk.tmp['w_supp']<sk.m:
                        s=self.sources.select_for_sink(c1,sk.m-sk.tmp['w_supp'])
                        if s:
                            water_sink=min(s.m,sk.m-sk.tmp['w_supp'])
                            sk.tmp['w_supp']+=water_sink
                            if not s in sk.tmp["w_in"].keys():
                                sk.tmp["w_in"][s]=0
                            sk.tmp["w_in"][s]+=water_sink
                            #s.m-=water_sink
                            s.update(sk,water_sink)
                            if verbose:
                                print('Water supply', fgc(GREY)+"{"+s.name,">>",sk.name+"}",fgc(WHITE)+formatting(water_sink,d=2),'m3/h',formatting(sk.tmp['w_supp']/sk.m*100),"%")
                            if (s,sk) in self.links.keys():
                                self.links[(s,sk)]+=water_sink
                            else:
                                self.links[(s,sk)]=water_sink  
                elif sk.cin_max<=c1 and sk.tmp['w_supp']<sk.m:
                    connections,res=self.sources.select_for_sink2(c1,sk.m-sk.tmp['w_supp'])
                    if connections:
                        if verbose:
                            print("Connection solver",res.nit,'iterations','success',res.success)
                        for s,m_ in connections.items():
                            #s.m-=m_
                            s.update(sk,m_)
                            sk.tmp['w_supp']+=m_
                            if not s in sk.tmp["w_in"].keys():
                                sk.tmp["w_in"][s]=0
                            sk.tmp["w_in"][s]+=m_
                            if verbose:
                                print(' \u2192 Water supply', fgc(GREY)+"{"+s.name,">>",sk.name+"}",fgc(WHITE)+formatting(m_,d=2),'m3/h',formatting(sk.tmp['w_supp']/sk.m*100),"%")
                            if (s,sk) in self.links.keys():
                                self.links[(s,sk)]+=m_
                            else:
                                self.links[(s,sk)]=m_       

        if verbose:
            line(label='End of Design',marker="=")
               
             
    def __repr__(self):
        return str({"sources":self.sources})
    
    def draw(self,grouping=False):
        fontname='verdana'
        fsize="point-size='"+str(10)+"'"
        from graphviz import Digraph
        def get_label(rows):
            label='<<font '+fsize+'>'
            for i in range(len(rows)):
                row=rows[i]
                txt=row['txt']
                if 'options' in row.keys():
                    for k,v in row['options'].items():
                        if k=='b' and v:
                            txt="<b>"+txt+"</b>"
                        if k=='c':
                            txt="<font color='"+v+"'>"+txt+'</font>'
                label+=txt
                if not i==len(rows)-1:
                    label+='<br/>'               
            return label+'</font>>'
        def add_source(g,s,i):
            label=get_label([{'txt':s.name,'options':{'b':1}},
                              {'txt':formatting(s.m,2)+' m3/h','options':{'c':'green'}},
                              {'txt':formatting(s.c)+' ppm','options':{}}
                             ])
            g.node(s.key,label=label,shape='tab',style='filled',fillcolor='grey91',fontname=fontname)
        def add_post(g,p,i):
            label=get_label([{'txt':p.name,'options':{'b':1}},
                              {'txt':formatting(p.mc,2)+' kg/h','options':{'c':'green'}},
                             ])
            g.node(p.key,label=label,shape='box',fontname=fontname)
        def add_sink(g,s,i):
            label=get_label([{'txt':s.name,'options':{'b':1}},
                              {'txt':formatting(s.m,2)+' m3/h','options':{'c':'green'}},
                              {'txt':formatting(s.cin_max)+' ppm','options':{}}
                             ])
            g.node(s.key,label=label,shape='box',style='filled',fillcolor='yellow',fontname=fontname)
        def add_regen(g,p,i):
            label=get_label([ {'txt':formatting(p.cout_max)+'&#8600;'+formatting(p.regen.co)},
                             ])
            g.node(p.regen.key,shape='invhouse',label=label, fillcolor="white:#82E0AA ", style='filled', gradientangle='90')        
        g = Digraph(engine='dot',)
        if grouping:
            locations=set()
            for i,p in enumerate(self.pinch.posts):
                if p.loc:
                    locations.add(p.loc)
                else:
                    add_post(g,p,i)
                if p.isregen:
                    if p.regen.loc:
                        locations.add(p.regen.loc)
                    else:
                        add_regen(g,p,i)
            for i,s in enumerate(self.pinch.sources):
                if s.loc:
                    locations.add(s.loc)
                else:
                    add_source(g,s,i)
            for i,s in enumerate(self.pinch.sinks):
                if s.loc:
                    locations.add(s.loc)
                else:
                    add_sink(g,s,i) 
            
            for loc in locations:
                with g.subgraph(name='cluster_'+loc) as c:
                    c.attr(color='blue',style='dashed,rounded')
                    label=get_label([ {'txt':loc},])
                    c.attr(label=label,labelfontcolor=    "#ff0000")
                    c.attr(fontname=fontname)
                    for i,p in enumerate(self.pinch.posts):
                        if p.loc==loc:
                            add_post(c,p,i)
                        if p.isregen:
                            if p.regen.loc==loc:
                                add_regen(c,p,i)
                    for i,s in enumerate(self.pinch.sources):
                        if s.loc==loc:
                            add_source(c,s,i)
                    for i,s in enumerate(self.pinch.sinks):
                        if s.loc==loc:
                            add_sink(c,s,i)
        else:
            for i,s in enumerate(self.pinch.sources):
                add_source(g,s,i)
            for i,p in enumerate(self.pinch.posts):
                add_post(g,p,i)
                if p.isregen:
                    add_regen(g,p,i)
            for i,s in enumerate(self.pinch.sinks):
                add_sink(g,s,i)
        # fw
        fw_label=get_label([{'txt':'Freshwater','options':{'b':1}},
                            {'txt':formatting(self.pinch.cascade.fw,2)+' m3/h','options':{'c':'blue'}},
                             ])
        g.node('fw',label=fw_label,style='filled',fillcolor='lightblue1',fontname=fontname)
        
        
        def edge_label(m,c=None):
            txt=[{'txt':formatting(m,2)}]
            if c:
                txt.append({'txt':formatting(c)})
            return get_label(txt)
        #links
        for k,m in self.links.items():
            if m>1e-3:
                from_=k[0]
                to_=k[1]
                if from_.type=='fw':
                    g.edge(from_.key,to_.key,color='dodgerblue',arrowhead='empty',label=edge_label(m))
                if from_.type=='s':
                    if from_.c==0:
                        g.edge(from_.key,to_.key,color='dodgerblue',arrowhead='empty',label=edge_label(m,from_.c))
                    else:
                        g.edge(from_.key,to_.key,color='gray',arrowhead='empty',label=edge_label(m,from_.c))
                if from_.type=='p':
                    g.edge(from_.key,to_.key,color='black',arrowhead='empty',label=edge_label(m,from_.c))
                if from_.type=='r':
                      g.edge(from_.key,to_.key,color='green',arrowhead='empty',label=edge_label(m,))
        # posts -> regen
        for i,p in enumerate(self.pinch.posts):
            if p.isregen:
                g.edge(p.key,p.regen.key,weight='1', 
                           penwidth='1',color='green',arrowhead='empty',
                           label=edge_label(p.regen.tmp['w_supp'])
                           )
        # ww
        ww_links={}
        m_ww=0
        # connect posts
        for p in self.pinch.posts:
            m_ww_=p.get_ww()
            m_ww+=m_ww_
            ww_links[p.key]=m_ww_
            
        # connect sources
        for s in self.sources.values():
            if s.type in ['s','r']:
                m_ww+=s.m
                ww_links[s.key]=s.m
        
        ww_label=get_label([{'txt':'Wastewater','options':{'b':1}},
                            {'txt':formatting(m_ww,2)+' m3/h','options':{'c':'blue'}},
                             ]) 
        g.node('ww',label=ww_label,style='filled',fillcolor='ivory',fontname=fontname,) 
        for k,m in  ww_links.items():
            if m>1e-2:
                g.edge(k,'ww',label=edge_label(m),style="",color="goldenrod3",arrowhead='empty')
        return g
            
            

class __pinch__(__obj__):
    def __init__(self,**args):
        super().__init__(json_schema['pinch'])
        design=True
        verbose=False
        for k,v in args.items():
            if k=='posts' or k=='usages':
                for x in sorted(v,key=lambda x: x['cin_max']):
                    self.posts.append(__post__(self,x))
            if k=='sources' :
                for x in sorted(v,key=lambda x: x['c']):
                    self.sources.append(__source__(self,x))
            if k=='sinks' or k=='puits':
                for x in sorted(v,key=lambda x: x['cin_max']):
                    self.sinks.append(__sink__(self,x))
            if k=="design":
                design=v
            if k=="verbose":
                verbose=v
                
                
        self.cascade=__cascade__(self)
        if design:
            self.design=__design__(self,verbose=verbose)
    def fast_cascade(self):
        return __cascade__(self)
    def sk_sr_graph(self,wwy=.2):
        #wwy=.1 to .5
        # SK & SR graph 
        # c=self.cascade.c[:-1]
        fw=self.cascade.fw   
        ww=self.cascade.ww
        sk=sorted(self.cascade.D,key=lambda x : x['c'])
        sr=sorted(self.cascade.S,key=lambda x:x['c'])
        m_sink=cumsum(array(list(map(lambda x:x['m'],sk))))
        mc_sink=cumsum(array(list(map(lambda x:x['m']*x['c']/1000,sk))))
        m_source=cumsum(list(map(lambda x:x['m'],sr)))
        mc_source=cumsum(array(list(map(lambda x:x['m']*x['c']/1000,sr))))
            
        # =========================================================================
        def affine(m,mc,m1):
            p=polyfit(m,mc,1)
            return polyval(p,m1)
        
        lb=max(m_sink[0],m_source[0]+fw)
        ub=min(m_sink[-1],m_source[-1]+fw)
        
        if lb>ub:
            tmp=lb
            lb=ub
            ub=tmp
        mc_sr=[]
        mc_sk=[]
        m__=[]
        for m in m_sink:
            if m<=ub and m >= lb:
                m__.append(m)
        for m in m_source+fw:
            if m<=ub and m >= lb:
                m__.append(m)
        m_=[]
        for i in range(len(m__)-1):
            m_=concatenate((m_,linspace(m__[i],m__[i+1],1000)))
            
        m_=unique(m_)
        for m in m_:
            for i in range(len(m_source)-1):
                if m>=m_source[i]+fw and m<=m_source[i+1]+fw:
                    mc_sr.append(affine([m_source[i]+fw,m_source[i+1]+fw],
                                     [mc_source[i],mc_source[i+1]],
                                      m))
                    break
            for i in range(len(m_sink)-1):
                if m>=m_sink[i] and m<=m_sink[i+1]:
                    mc_sk.append(affine([m_sink[i],m_sink[i+1]],[mc_sink[i],mc_sink[i+1]],m))
                    break
        mc_sr=array(mc_sr)
        mc_sk=array(mc_sk)
        i=argmin(abs(mc_sr-mc_sk))
        #==========================================================================
        

        
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        sink_color='tomato'
        source_color='blue'
        ax.plot(m_sink,mc_sink,'--',label='sink',color=sink_color,linewidth=1)
        ax.plot(m_source,mc_source,'-.',label='source',color="cornflowerblue",linewidth=1)
        ax.plot(m_source+fw,mc_source,'--',label='shifted source',color=source_color,linewidth=1)
        
        ax.fill_between(m_, mc_sk, mc_sr,
                        where=(mc_sk> mc_sr), facecolor='none', alpha=0.5,hatch='...')
        
        i=argmin(abs(mc_sr-mc_sk))
        plt.plot(m_[i],mc_sr[i],'*',label='pinch',markeredgecolor="darkgreen", markersize=8,markerfacecolor='white')
        
        #limites
        if fw:
            ax.plot([m_sink[0],m_sink[0]],[0,mc_source[-1]/3],'--',color='grey',linewidth=1)
            ax.plot([m_source[0]+fw,m_source[0]+fw],[0,mc_source[-1]/3],'--',color='grey',linewidth=1)

            ax.annotate('', xy=(m_sink[0], mc_source[-1]/3*.8), xytext=(m_source[0]+fw,mc_source[-1]/3*.8),size=8,
              arrowprops=dict(arrowstyle="<->, head_width=.2", connectionstyle="arc3",facecolor ='white',edgecolor='grey',ls='-',lw=1),
              bbox=dict(boxstyle="round", fc="grey", ec="black", pad=0.2, alpha=.2))
            ax.text((m_source[0]+fw)/2,mc_source[-1]/3*.95,"$\mathrm{"+formatting(fw,2)+"}$",size=10)
        if ww:
            ax.plot([m_source[-1]+fw,fw+m_source[-1]],[mc_sr[i]*(1-wwy*2),mc_source[-1]],'--',color='grey',linewidth=1)
            ax.plot([m_sink[-1],m_sink[-1]],[0,mc_sink[-1]*(1+wwy)],'--',color='grey',linewidth=1)

            ax.annotate('', xy=(m_sink[-1], mc_sr[i]*(1-wwy)), xytext=(m_source[-1]+fw,mc_sr[i]*(1-wwy)),size=8,
              arrowprops=dict(arrowstyle="<->, head_width=.2", connectionstyle="arc3",facecolor ='white',edgecolor='grey',ls='-',lw=1),
              bbox=dict(boxstyle="round", fc="grey", ec="black", pad=0.2, alpha=.2))
            ax.text((m_source[-1]+fw)-ww/2,mc_sr[i]*(1-wwy/2),"$\mathrm{"+formatting(ww,2)+"}$",size=10)
        
        ax.grid()
        ax.set_xlabel('water flowrate (m3/h)')
        ax.set_ylabel('mass flowrate of load (kg/h)')
        ax.legend() 
        return fig,ax

    def composite(self):
        c=self.cascade.c[:-1]
        fw=self.cascade.fw
        ww=self.cascade.ww
        sources=copy.deepcopy(self.cascade.S)
        sources.append({'c':0,'m':fw})

        mc_d=[0]
        mc_s=[0]
        
        # d_grouping=[]
        # s_grouping=[]


        for i in range(len(c)-1):
            mc_d_=0
            mc_s_=0
            dc=c[i+1]-c[i]
            for p in self.cascade.D:
                if p['c']<=c[i] :
                    mc_d_+=p['m']/1000*dc
            for s in sources:
                if s['c']<=c[i]:
                    mc_s_+=s['m']/1000*dc
            mc_s.append(mc_s_)
            mc_d.append(mc_d_)
        mc_d=cumsum(mc_d)
        mc_s=cumsum(mc_s)
        
        # fit source composite
        c_source=copy.deepcopy(c)
        if mc_s[-1]>mc_d[-1] and len(c)>=2:
            f = interp1d(mc_s[-2:],c[-2:],fill_value="extrapolate")
            mc_s[-1]=mc_d[-1]
            c_source[-1]=f(mc_d[-1])
        
        # pinch point
        mc_pinch=mc_d[self.cascade.pp]
        c_pinch=c[self.cascade.pp]
        max_load=mc_d[-1]
        max_c=c[-1]
            
        
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        
        ax.plot(mc_d,c,label='Demand composite',color='tomato',marker='s',markerfacecolor='white',markersize=4)
        ax.plot(mc_s,c_source,label='Source composite',color='dodgerblue',marker='s',markerfacecolor='white',markersize=4)
        ax.plot(mc_pinch,c_pinch,'*',markersize=10,markerfacecolor="lightgrey",color='forestgreen',label='Pinch ('+formatting(mc_pinch,2)+', '+formatting(c_pinch)+')')
        # max load lim
        ax.plot([max_load,max_load],[0,max_c],'--',color='grey',linewidth=1)
        ax.annotate(formatting(max_load,2)+'\nkg/h', xy=(max_load, max_c/4), xytext=(max_load-max_load/8,max_c/4),size=8,
              arrowprops=dict(arrowstyle="->, head_width=.2", connectionstyle="arc3",facecolor ='white',edgecolor='grey',ls='-'),
              bbox=dict(boxstyle="round", fc="grey", ec="black", pad=0.2, alpha=.2))
        # fw
        f = interp1d([0,mc_pinch],[0,c_pinch])
        mc_fw=mc_pinch/2
        c_fw=f(mc_fw)
        
        ax.annotate(formatting(fw,2)+'\n$\\mathrm{m^3/h}$', xy=(mc_fw,c_fw),
             xytext=(mc_pinch/3,c_pinch*(1.5)), 
             size=8, ha='right', va="center",
             bbox=dict(boxstyle="round", alpha=0.4,fc='skyblue'),
             arrowprops=dict(arrowstyle="wedge,tail_width=0.5", alpha=0.1));
        # ww
        ax.annotate(formatting(ww,2)+'\n$\\mathrm{m^3/h}$', xy=(mc_s[-1], c[-1]),
             xytext=(mc_s[-1]*.8, c[-1]), 
             size=8, ha='right', va="center",
             bbox=dict(boxstyle="round", alpha=0.4,fc='skyblue'),
             arrowprops=dict(arrowstyle="wedge,tail_width=0.5", alpha=0.1));
        
        
        
        ax.legend()
        ax.set_xlabel('Load kg/h')
        ax.set_ylabel('Concentration ppm')
        ax.grid()
        return fig,ax
    
    def sensitivity_analysis(self,problem,N=100):
        return __sensitivity_analysis__(self,problem,N)

class __sensitivity_analysis__:
        def __init__(self,pinch,problem,N):
            from SALib.sample import saltelli
            from SALib.analyze import morris
            from SALib.analyze import sobol
            from SALib.plotting.morris import horizontal_bar_plot, covariance_plot, \
                sample_histograms
            self.pinch=copy.deepcopy(pinch)
            self.problem={'num_vars':len(problem),
                          'names': list(problem.keys()),
                           'bounds':list(map(lambda x: x["bound"],problem.values()))}
            self.var_names=[]
            print(problem)
            for k,v in problem.items():
                if 'name' in v.keys():
                    self.var_names.append(v['name'])
                else:
                    self.var_names.append("")
            self.samples =  saltelli.sample(self.problem, N)
            Y = []
            for x in self.samples:
                for i,k in enumerate(self.problem['names']):
                    inv,index,var = k.split(',')
                    if inv=="regen":
                        setattr(self.pinch.posts[int(index)].regen,var,x[i])
                    else:
                        setattr(getattr(self.pinch,inv)[int(index)],var,x[i])   
                Y.append(self.pinch.fast_cascade().fw)
           # print(Y)
            self.Y=array(Y,)
            # self.Si_morris = morris.analyze(self.problem, self.samples, self.Y, conf_level=0.95,
            #             print_to_console=False, num_levels=10)
            self.Si_sobol = sobol.analyze(self.problem, self.Y, print_to_console=False)
            # fig, (ax1, ax2) = plt.subplots(1, 2)
            # horizontal_bar_plot(ax1, self.Si_morris, {}, sortby='mu_star', unit=r"m3/h")
            # covariance_plot(ax2, self.Si_morris, {}, unit=r"m3/h")

            # fig2 = plt.figure()
            # sample_histograms(fig2, self.samples, self.problem, {'color': 'y'})
            # plt.show()
            
                        
            
        
        
        

if __name__ == "__main__":
    usages=[{'name':'process 1','cin_max':0,'cout_max':100,'mc':2,'regen':{'R':10,'loc':'regen','f':50},'loc':'A'},
       {'name':'process 2','cin_max':50,'cout_max':100,'mc':5,'loc':"A",'regen':{'R':90,'loc':'regen','f':0}},
       {'name':'process 3','cin_max':50,'cout_max':800,'mc':30,'loc':'B','regen':{'R':90,'loc':'regen','f':0}},
       {'name':'process 4','cin_max':400,'cout_max':800,'mc':4,'loc':"B"}]
    
    # Dominic Foo
    sources=[{'name':'Distillation bottoms','c':0,'m':.8*3600/1000},
             {'name':'Off-gas condensate','c':14,'m':5*3600/1000},
             {'name':'Aqueous layer','c':25,'m':5.9*3600/1000},
             {'name':'Ejector condensate','c':34,'m':1.4*3600/1000}]
    demands = [{'name':'BFW0','cin_max':0,'m':1.2*3600/1000},
               {'name':'BFW','cin_max':10,'m':5.8*3600/1000},
               {'name':'BFW1','cin_max':1,'m':19.8*3600/1000}]
    
    pinch1=__pinch__(usages=usages,verbose=0)
    #pinch2=__pinch__(sinks=demands,sources=sources,verbose=True)
        
    
     