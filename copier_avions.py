def copier_avions():
    copie=list[dict]= [{"id": "AF342", "fuel": 18, "medical": False, "technical_issue": False, "diplomatic_level": 2, "arrival_time": 19.42,"scoring":0},
    {"id": "LH908", "fuel": 25, "medical": False, "technical_issue": True,  "diplomatic_level": 1, "arrival_time": 19.44,"scoring":0},
    {"id": "BA117", "fuel": 14, "medical": True,  "technical_issue": False, "diplomatic_level": 3, "arrival_time": 19.46,"scoring":0},
    {"id": "EK202", "fuel": 40, "medical": False, "technical_issue": False, "diplomatic_level": 5, "arrival_time": 19.47,"scoring":0},
    {"id": "IB455", "fuel": 12, "medical": False, "technical_issue": False, "diplomatic_level": 2, "arrival_time": 19.49,"scoring":0},
    {"id": "AZ721", "fuel": 9,  "medical": False, "technical_issue": False, "diplomatic_level": 1, "arrival_time": 19.50,"scoring":0},
    {"id": "UA331", "fuel": 22, "medical": False, "technical_issue": False, "diplomatic_level": 4, "arrival_time": 19.51,"scoring":0},
    {"id": "QR998", "fuel": 16, "medical": False, "technical_issue": False, "diplomatic_level": 5, "arrival_time": 19.52,"scoring":0},
    {"id": "TK876", "fuel": 8,  "medical": False, "technical_issue": False, "diplomatic_level": 2, "arrival_time": 19.53,"scoring":0},
    {"id": "AC410", "fuel": 35, "medical": False, "technical_issue": False, "diplomatic_level": 3, "arrival_time": 19.54,"scoring":0},
    {"id": "DL550", "fuel": 11, "medical": True,  "technical_issue": False, "diplomatic_level": 2, "arrival_time": 19.55,"scoring":0},
    {"id": "SU119", "fuel": 27, "medical": False, "technical_issue": False, "diplomatic_level": 1, "arrival_time": 19.56,"scoring":0},
    {"id": "SN204", "fuel": 6,  "medical": False, "technical_issue": False, "diplomatic_level": 2, "arrival_time": 19.57,"scoring":0},
    {"id": "KL330", "fuel": 19, "medical": False, "technical_issue": False, "diplomatic_level": 3, "arrival_time": 19.58,"scoring":0},
    {"id": "EY601", "fuel": 28, "medical": False, "technical_issue": False, "diplomatic_level": 4, "arrival_time": 19.59,"scoring":0},
    {"id": "AF118", "fuel": 15, "medical": False, "technical_issue": True,  "diplomatic_level": 2, "arrival_time": 20.00,"scoring":0},
    {"id": "LH332", "fuel": 21, "medical": False, "technical_issue": False, "diplomatic_level": 1, "arrival_time": 20.01,"scoring":0},
    {"id": "BA450", "fuel": 10, "medical": False, "technical_issue": False, "diplomatic_level": 3, "arrival_time": 20.02,"scoring":0},
    {"id": "IB900", "fuel": 17, "medical": False, "technical_issue": False, "diplomatic_level": 2, "arrival_time": 20.03,"scoring":0},
    {"id": "AZ333", "fuel": 13, "medical": False, "technical_issue": False, "diplomatic_level": 1, "arrival_time": 20.04,"scoring":0},
    {"id": "UA870", "fuel": 24, "medical": False, "technical_issue": False, "diplomatic_level": 4, "arrival_time": 20.05,"scoring":0},
    {"id": "QR555", "fuel": 7,  "medical": False, "technical_issue": False, "diplomatic_level": 5, "arrival_time": 20.06,"scoring":0},
    {"id": "TK221", "fuel": 20, "medical": False, "technical_issue": False, "diplomatic_level": 2, "arrival_time": 20.07,"scoring":0},
    {"id": "AC990", "fuel": 5,  "medical": False, "technical_issue": False, "diplomatic_level": 3, "arrival_time": 20.08,"scoring":0},]

    if "medical" in copie == True:
        copie["scoring"] += 5
    else:        copie["scoring"] += 1

    if "technical_issue" in copie == True:
        copie["scoring"] += 5
    else:        copie["scoring"] += 1

    return copie 



