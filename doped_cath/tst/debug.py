from CATH_API.lib import *
print(CATH_superfamily('v4_1_0')[1][0])


req = requests.request('GET', 'http://www.cathdb.info/version/v4_1_0/api/rest/superfamily/1.10.8.10')
print(j_parsed["data"]["child_count_s35_code"])
j='''
{
"success": true,
"data": {
"cath_id_depth": "4",
"s100_code": null,
"child_count_s100_code": "95",
"cath_id": "1.10.8.10",
"superfamily_id": "1.10.8.10",
"classification_description": null,
"child_count_s95_code": "73",
"child_count_s60_code": "65",
"child_count_s35_code": "53",
"s95_code": null,
"child_count_s100_count": "255",
"s60_code": null,
"s35_code": null,
"example_domain_id": "1oaiA00",
"classification_name": "DNA helicase RuvA subunit, C-terminal domain",
"child_count_c": "0",
"child_count_t": "0",
"child_count_h": "0",
"child_count_a": "0"
}
}
'''
