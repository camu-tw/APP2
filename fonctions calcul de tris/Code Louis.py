AVIONS_INITIAL = [
    {"id": "AF342", "fuel": 18, "medical": False, "technical_issue": False, "diplomatic_level": 2, "arrival_time": 19.42},
    {"id": "LH908", "fuel": 25, "medical": False, "technical_issue": True,  "diplomatic_level": 1, "arrival_time": 19.44},
    {"id": "BA117", "fuel": 14, "medical": True,  "technical_issue": False, "diplomatic_level": 3, "arrival_time": 19.46},
    {"id": "EK202", "fuel": 40, "medical": False, "technical_issue": False, "diplomatic_level": 5, "arrival_time": 19.47},
    {"id": "IB455", "fuel": 12, "medical": False, "technical_issue": False, "diplomatic_level": 2, "arrival_time": 19.49},
    {"id": "AZ721", "fuel": 9,  "medical": False, "technical_issue": False, "diplomatic_level": 1, "arrival_time": 19.50},
    {"id": "UA331", "fuel": 22, "medical": False, "technical_issue": False, "diplomatic_level": 4, "arrival_time": 19.51},
    {"id": "QR998", "fuel": 16, "medical": False, "technical_issue": False, "diplomatic_level": 5, "arrival_time": 19.52},
    {"id": "TK876", "fuel": 8,  "medical": False, "technical_issue": False, "diplomatic_level": 2, "arrival_time": 19.53},
    {"id": "AC410", "fuel": 35, "medical": False, "technical_issue": False, "diplomatic_level": 3, "arrival_time": 19.54},
    {"id": "DL550", "fuel": 11, "medical": True,  "technical_issue": False, "diplomatic_level": 2, "arrival_time": 19.55},
    {"id": "SU119", "fuel": 27, "medical": False, "technical_issue": False, "diplomatic_level": 1, "arrival_time": 19.56},
    {"id": "SN204", "fuel": 6,  "medical": False, "technical_issue": False, "diplomatic_level": 2, "arrival_time": 19.57},
    {"id": "KL330", "fuel": 19, "medical": False, "technical_issue": False, "diplomatic_level": 3, "arrival_time": 19.58},
    {"id": "EY601", "fuel": 28, "medical": False, "technical_issue": False, "diplomatic_level": 4, "arrival_time": 19.59},
    {"id": "AF118", "fuel": 15, "medical": False, "technical_issue": True,  "diplomatic_level": 2, "arrival_time": 20.00},
    {"id": "LH332", "fuel": 21, "medical": False, "technical_issue": False, "diplomatic_level": 1, "arrival_time": 20.01},
    {"id": "BA450", "fuel": 10, "medical": False, "technical_issue": False, "diplomatic_level": 3, "arrival_time": 20.02},
    {"id": "IB900", "fuel": 17, "medical": False, "technical_issue": False, "diplomatic_level": 2, "arrival_time": 20.03},
    {"id": "AZ333", "fuel": 13, "medical": False, "technical_issue": False, "diplomatic_level": 1, "arrival_time": 20.04},
    {"id": "UA870", "fuel": 24, "medical": False, "technical_issue": False, "diplomatic_level": 4, "arrival_time": 20.05},
    {"id": "QR555", "fuel": 7,  "medical": False, "technical_issue": False, "diplomatic_level": 5, "arrival_time": 20.06},
    {"id": "TK221", "fuel": 20, "medical": False, "technical_issue": False, "diplomatic_level": 2, "arrival_time": 20.07},
    {"id": "AC990", "fuel": 5,  "medical": False, "technical_issue": False, "diplomatic_level": 3, "arrival_time": 20.08},
]

 #je vais creer une fonction algorithme de tri qui prend en parametre le score de chaque avion.

def insertion_tri_score(L): #L = liste de dictionnaires d'avions
    n=len(L)
    a=0
    for i in range(1, n):
        key= L[i]
        j= i-1
        while j>=0 and L[j]> key:
            L[j+1]= L[j]
            j=j-1
            a+=1
        L[j+1]= key
    return L,a

print(insertion_tri_score([7,4,9,3,23,1,42,8,5]))


