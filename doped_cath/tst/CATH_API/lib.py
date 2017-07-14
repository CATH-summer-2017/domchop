import requests
CATH_BASE='www.cathdb.info'
protocol = 'http://'
url_BASE = protocol + CATH_BASE

def fetch_cath(cath_url):
	url = url_BASE + cath_url
	req = requests.request('GET',url);
	if req.status_code != 200:
		return [('HTTP Request_failed',url),[]]
	else:
		try:
			j = req.json();
		except:
			return [('no json returned',url),[]]
		if not j["success"]:
			return [('CATH API failed',url),[]]
		return [0,j["data"]]
	
# '/version/:version_id/api/rest/superfamily'
def CATH_superfamily(version):

	url = ('/version/%s/api/rest/superfamily' % version)
	# print(url)
	return fetch_cath(url)

# class CATH_obj():
# 	def fetch():
# 		pass
# 	self.url=[];

# class dCATH_superfamily(CATH_obj):
def dCATH_superfamily(version, domain_id):
	url = "/version/{:s}/domain/{:s}/".format(version, domain_id)
	return fetch_cath(url)