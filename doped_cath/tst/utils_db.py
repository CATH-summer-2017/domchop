from .models import *
from domutil.util import *
# from utils import *
from modeller import *
import numpy as np 
from django.db import transaction

def verify_version(ver):
    #### Check whether this version is recorded in 'version' table
#     try:
    vset = version.objects.filter(name=ver)
    if vset.count() > 1:
        raise Exception,'multiple version with name %s'%(ver)
    elif not vset.exists():
        v = version(name=ver)
        v.save()
    else:
        v = vset[0]
    return v


### Modeller initialisation
def	init_env(env=None):

	with stdoutIO() as s:	
		env = environ()
		#env.io.atom_files_directory = ['../atom_files']
		env.io.atom_files_directory = ['../pdbs','$(PDBlib)/',
		'$(repos)/cathdb/dompdb/',
        '$(repos)/cathdb/temppdbs/',
		]
		env.libs.topology.read(file='$(LIB)/top_heav.lib')
		env.libs.parameters.read(file='$(LIB)/par.lib')
	return env
	
### Fill structure-based stats
def domain_stat_null(d):
	dstat = domain_stat(domain = d);
	dstat.save()
	return dstat
	# if d.domain_stat == None:

def domain_stat_fill( d, **kwargs):
	 try:
	 	dstat = d.domain_stat
	 except:
	 	dstat = domain_stat_null(d);

	 outdict = get_something( str(d.domain_id) , **kwargs)

	 for k,v in outdict.iteritems():
	 	if hasattr(dstat,k):
	 		setattr(dstat, k, v)
	 dstat.save()
	 return d

##### !!!!! DEPRECATED !!!!!! 
def homsf_stat_fill(h):
# if 1:
    if h.level.letter == 'H':
        pass
    else:
        print "Node %s is not filled because it is not a homsf, but a '%s'" % (str(h),h.level.letter)
    
    
    try:
        nstat = h.node_stat
    except:
        nstat = node_stat(node = h)
        nstat.save()
        

    hset  = h.classification_set;
    ### Compute statistics only if the set is larger than 10
    if hset.count() > 10:
        hset = hset.annotate(Acount=Avg("domain__domain_stat__atom_count"))
        hset = hset.annotate(Rcount=Avg("domain__domain_stat__res_count"))
        hset = hset.annotate(NBcount=Avg("domain__domain_stat__nbpair_count"))

    #     hset.domain
        l = hset.values_list('Acount','Rcount','NBcount')
        a = np.array(l)
    #     C = np.cov(a[:,0],a[:,1],a[:,2])
        c = np.cov(a.T)
        C = cov2corr(c); ## utils.cov2corr
#         print(C.shape)
        nstat.Rsq_NBcount_Acount = C[0,2] ** 2
        nstat.Rsq_NBcount_Rcount = C[1,2] ** 2
    else:
        nstat.Rsq_NBcount_Acount = None
        nstat.Rsq_NBcount_Rcount = None
    try:
        nstat.save()
    except:
        print nstat.__dict__
    return h


#### Calculate Mahalanobis distance between the point(pt) and the distribution (mu, cinv), with "mu"=Euclidean_centre AND "cinv"=inversed_covariance_matrix
def maha_dist(pt, mu, cinv):
    dd = pt - mu
    md = dd.T.dot( cinv.dot( dd))
    return md


from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
pip_pc_std = Pipeline([
    ('pca', PCA(n_components=2)),
    ('scaling', StandardScaler()),
                    ])
        
def homsf_stat_fill(h):
#     if 1:
    if h.level.letter == 'H':
        pass
    else:
        print "Node %s is not filled because it is not a homsf, but a '%s'" % (str(h),h.level.letter)


    try:
        nstat = h.node_stat
    except:
        nstat = node_stat(node = h)
        nstat.save()

    hset  = h.classification_set;


    ### Compute statistics only if the set is larger than 10
    if hset.count() > 10:
        hset = hset.annotate(Acount=Avg("domain__domain_stat__atom_count"))
        hset = hset.annotate(Rcount=Avg("domain__domain_stat__res_count"))
        hset = hset.annotate(NBcount=Avg("domain__domain_stat__nbpair_count"))

    #     hset.domain
        l = hset.values_list('Acount','NBcount','Rcount')
        a = np.array(l)
        # sa = a
        c = np.cov(a.T)
        C = cov2corr(c); ## utils.cov2corr
        nstat.Rsq_NBcount_Acount = C[0,1] ** 2
        nstat.Rsq_NBcount_Rcount = C[2,1] ** 2

        sa = a[:,0:2]
        # sa = np.vstack([a[:,0],a[:,1]]).T ### Using only 'Acount' and 'NBcount', discard 'Rcount'
        c = c[:2,:2]

        cinv = np.linalg.inv(c)
        mu = np.mean(sa, axis = 0)

        dstat_set = hset.values_list('domain',flat = True)

        sset = hset ### rename to sset ,aka "s35_set"
    #     qset = domain_stat.objects.none()
        qlst = []
        # print sa.shape
        pcxs,pcys = pip_pc_std.fit_transform(sa).T 

        #### Inverted pc axis if opposing originial x/y axis
        if np.dot(pcys, sa[:,1]) < 0:
            pcys *= -1
        if np.dot(pcxs, sa[:,0]) < 0:
            pcxs *= -1

        for s,pt,pcx,pcy in zip( sset , sa, pcxs, pcys):
            dstat = s.domain.domain_stat
            md = maha_dist( pt, mu, cinv)
            dstat.maha_dist = md
            dstat.pcx = pcx
            dstat.pcy = pcy

    #         print(s.domain)
    #         print(dstat)
    #         print(md)
            qlst.append(dstat)
    #         dstat.save()
    #     qset = list(chain(qset , [dstat]))

    #         print type(qset)

    else:
        nstat.Rsq_NBcount_Acount = None
        nstat.Rsq_NBcount_Rcount = None
        qlst = []

    # help(qset.save)

    # qset.save()
    try:
        nstat.save()
        for q in qlst:
            q.save()
#         print 'success'
        return 1
    except Exception as e:
#         print nstat.__dict__
        print 'failed for ', str(e)
        return 0

