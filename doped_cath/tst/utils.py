import numpy as np
from .models import *
import json


### Lets get 2.40.50.140
def select_homsf(sc):
#     sc = "2.40.50.140".split('.');
    sclst = sc.split('.');
    hier = ["Class","arch","topo","homsf","s35","s60","s95","s100"]
    dct = {x:int(y) for x,y in zip(hier,sclst+['0'])}
    # x for x in 
    homsf = classification.objects.get(**dct)
    return homsf


# s0 = StringIO.StringIO();
def preprocess(sfname="2.40.50.140"):
    homsf = select_homsf(sfname);

    xs = [];
    ys = [];
    y2s= [];
    lbls =[];


    for d in homsf.classification_set.all():      
        d = d.domain
        vals = get_something( str(d.domain_id),env,s0=s0)
        x = vals['nbpair_count']
        y = vals['DOPE']
        xs += [x];
        ys += [y];
        y2s+= [d.domain_length]
        lbls+=[d.domain_id];

    return (np.array(xs),np.array(ys),np.array(y2s),lbls)
    
#### The ACTUAL functoinal scripts!!!
# import matplotlib as mpl
# mpl.use('Agg')

import matplotlib
matplotlib.use('Agg') ### This is crucial to prevent server crash

import matplotlib.pyplot as plt
import mpld3

import StringIO
import sys,re
from domutil.util import *

#### Need to change the name of plugin sometime
class HelloWorld(mpld3.plugins.PluginBase):  # inherit from PluginBase
    """The Plugin that controls the behaviour of tooltip"""

    JAVASCRIPT = """
    mpld3.register_plugin("helloworld", HelloWorld);
    HelloWorld.prototype = Object.create(mpld3.Plugin.prototype);
    HelloWorld.prototype.constructor = HelloWorld;
    HelloWorld.prototype.requiredProps = ["id","labels",];
    
    function HelloWorld(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };
    
    HelloWorld.prototype.draw = function(){
       
    for(var i=0; i<this.props.ids.length; i++){    
        var obj = mpld3.get_element(this.props.id, this.fig);
        var labels = (this.props.labels);
        
//        obj.elements().on("mousedown",
//                          function(d, i){
//                          alert("clicked on points[" + labels[i] + "]");
//                          //highlight("#row_264173");
//                          highlight("#dbid_"+labels[i]);
//                          });

      
//         var obj = mpld3.get_element(this.props.ids[i], this.fig),
//             alpha_fg = this.props.alpha_fg;
//             alpha_bg = this.props.alpha_bg;
           var  alpha_fg = 1.0;
           var   alpha_bg = 0.3;
         obj.elements().on("mousedown",
                          function(d, i){
                          alert("clicked on points[" + labels[i] + "]");
                          //highlight("#row_264173");
                          highlight("#dbid_"+labels[i]);
                          })
             .on("mouseover", function(d, i){
                            d3.select(this).transition().duration(50)
                              .style("stroke-opacity", alpha_fg); })
             .on("mouseout", function(d, i){
                            d3.select(this).transition().duration(200)
                              .style("stroke-opacity", alpha_bg); 
                              });
    };

    }
    """
    def __init__(self, points,labels,idxs):
        self.dict_ = {"type": "helloworld",
                     "id": mpld3.utils.get_id(points),
                     "labels":labels,
                     "idxs":idxs}

class RectPlugin(mpld3.plugins.PluginBase):
    JAVASCRIPT = r"""
    mpld3.register_plugin("rect", RectPlugin);
    RectPlugin.prototype = Object.create(mpld3.Plugin.prototype);
    RectPlugin.prototype.constructor = RectPlugin;
    RectPlugin.prototype.requiredProps = [];
    RectPlugin.prototype.defaultProps = {
      button: true,
      enabled: null
    };
    function RectPlugin(fig, props){
      mpld3.Plugin.call(this, fig, props);
      var enabled = this.props.enabled;
      if (this.props.button) {
        var rectButton = mpld3.ButtonFactory({
          buttonID: "rect",
          sticky: true,
          actions: [ "drag" ],
          onActivate: this.activate.bind(this),
          onDeactivate: this.deactivate.bind(this),
          onDraw: function() {
            this.setState(enabled);
          },
          icon: function() {
            return mpld3.icons["brush"];
          }
        });
        this.fig.buttons.push(rectButton);
      }
      this.extentClass = "rectbrush";
    }
    RectPlugin.prototype.activate = function() {
      if (this.enable) this.enable();
    };
    RectPlugin.prototype.deactivate = function() {
      if (this.disable) this.disable();
    };
    RectPlugin.prototype.draw = function() {
      mpld3.insert_css("#" + this.fig.figid + " rect.extent." + this.extentClass, {
        fill: "#fff",
        "fill-opacity": 0,
        stroke: "#999"
      });
      var brush = this.fig.getBrush();
      this.enable = function() {
        this.fig.showBrush(this.extentClass);
        brush.on("brushend", brushend.bind(this));
        this.enabled = true;
      };
      this.disable = function() {
        this.fig.hideBrush(this.extentClass);
        this.enabled = false;
      };
      this.toggle = function() {
        this.enabled ? this.disable() : this.enable();
      };
      function brushend(d) {
        if (this.enabled) {
          var extent = brush.extent();
          if (!brush.empty()) {
          }
        } else {
          d.axes.call(brush.clear());
        }
      }
      this.disable();
    };
    """
    def __init__(self, button=True, enabled=True, xlim=None,ylim=None):
        if enabled is None:
            enabled = not button
        self.dict_ = {"type": "rect",
                      "button": button,
                      "enabled": enabled,
                      "xlim":xlim,
                      "ylim":ylim,
                      }


def scatterplot_dict(xs,y2s,ids, colors = None,lbls=None, forced_lbls=None, regress = True, show = False,**kwargs):   
    if not lbls:
        lbls = ids
    # if forced_lbls:
    #     lbls = forced_lbls
    #     print( "lbls settled")
    # print( "lbls not settled")

    # font = {'family' : 'normal',
    #     'weight' : 'bold',
    #     'size'   : 16}
    # # matplotlib.rc('font', **font)
    SMALL_SIZE = 12
    MEDIUM_SIZE = 16
    BIGGER_SIZE = 18
    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    # plt.rc('axes', titleweight='bold')    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = 'Ubuntu'
    plt.rcParams['font.monospace'] = 'Ubuntu Mono'
    plt.rcParams['font.weight'] = 10
    # plt.rcParams['font.size'] = 10
    # plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['text.usetex']=False
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['axes.titleweight'] = 'bold'


    idx = [not (x is None or y is None) for x,y in zip(xs,y2s)]
    xs = [x for x,y in zip(xs,idx) if y]
    y2s = [x for x,y in zip(y2s,idx) if y]
    ids = [x for x,y in zip(ids,idx) if y]
    
    xs = np.array(xs);
    y2s = np.array(y2s)
    # 
    # xs = xs.flat[idx]
    # print(len(idx))
    # y2s = y2s.flat[idx]
    # ids = [x for x,y in zip(ids,idx) if y]
    # lbls = lbls[idx]
    
    msg = '';
    plt.close()
    siz = [450,400]
    DPI=100.
    fig = plt.figure(figsize = [x/float(DPI) for x in siz], dpi=DPI)
    ax1 = fig.add_subplot(111,**kwargs)
    points = ax1.scatter(xs,y2s, 
        # colors,
        edgecolor = 'b',facecolor = 'b',
        # edgecolor = 'r',facecolor = 'r',
        marker ='o',
        # c = colors,
         s =100,
         alpha = 0.15,
         # **kwargs
         )
    # if 1:
    title = ''
    if regress:
        ((m,b),C) = np.polyfit(xs, y2s, 1, cov =True) ### This covariance seems different from the one generated by np.cov()
        # (m,b) = np.polyfit(xs, y2s, 1, cov = False)
        C = np.cov(xs,y2s)
        r_sq = cov2corr(C).flat[1] ** 2
  
        res2  = y2s - ( m*xs + b)
        outs = MAD_outlier(res2,3.0)
        outs = (outs * (res2<0));
        xso = xs[outs]
        y2so = y2s[outs]
        sc1 = ax1.scatter(xso,y2so,s=33,
            color='r',
            marker = 'x',
            label='outlier num = %d'%sum(outs))

        title += '''
        y  = %5.3f * x + %5.3f , 
        R_squared=%3.3f '''% (m,b,r_sq)
        xmm = np.array([min(xs),max(xs)])
        ax1.plot(xmm, m*xmm + b, 'g--',label = 'linear regression fit')

    oxlim = ax1.get_xlim()
    oylim = ax1.get_ylim()
    ax1.axis('auto')
    axlim = ax1.get_xlim()
    aylim = ax1.get_ylim()
    ax1.set_xlim(oxlim)
    ax1.set_ylim(oylim)

    ax1.legend()

    # ax1.legend(bbox_to_anchor=(1.1, 1.05))
    ax1.set_title(
        title)

    ax1.grid(True, which='both')
    plt.tight_layout()
 
    tooltip = mpld3.plugins.PointLabelTooltip(points, labels=lbls)
    mpld3.plugins.connect(fig, tooltip)
    mpld3.plugins.connect(fig, HelloWorld(points,lbls,ids))
    mpld3.plugins.connect(fig, RectPlugin(xlim=axlim,ylim=aylim))
    jdict = mpld3.fig_to_dict(fig);
    jstr = json.dumps(jdict);

    if show:
        mpld3.show()
    else:
        plt.close(fig)
        # fig.show()
        # plt.close("all")
    return(jdict)

##### !!!!!!!!!!!! Deprecated
def scatterplot_homsf_dict(homsf, fields=None, **kwargs):
    
    # sf = select_homsf(sfname)
    fields = (fields or 
        ['domain__domain_stat__res_count',
        'domain__domain_stat__nbpair_count',
        'domain__id',
        ])


    vlst = homsf.classification_set.values_list(
        *fields);

    # print()

    vlst = zip(*vlst );
    xs,y2s,lbls = vlst;


    jdict = scatterplot_dict(xs,y2s,lbls,**kwargs)
    return(jdict)

def scatterplot_qset_dict(qset, fields=None, labels = None, subplot_kwargs = None,  **kwargs):
    
    # sf = select_homsf(sfname)
    fields = (fields or 
        ['domain__domain_stat__res_count',
        'domain__domain_stat__nbpair_count',
        'domain__id',
        # 'domain__domain_id',
        ])


    vlst = qset.values_list(
        *fields);


    vlst = zip(*vlst );

    if len(vlst) == 4:
        xs,y2s,ids,lbls = vlst;
    elif len(vlst) == 3:
        xs,y2s,ids = vlst;
        # lbls = None

    # print(list(labels).__len__())
    lbls = list(labels) 

    # if forced_lbls:
    #     lbls = forced_lbls
    #     print( "lbls settled")
    # print( "lbls not settled")
    # print("debug",len(forced_lbls))


    jdict = scatterplot_dict(xs,y2s,ids, lbls = lbls, **subplot_kwargs)
    return(jdict)

# mpld3.save_json(fig,'tmp')