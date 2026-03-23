
"""
Voici une liste de datasets pour vos différents tests. Ne les testez pas tous en même temps !
"""

# DATASET PRISE EN MAIN
avions = [
    {"id": "AF342", "fuel": 18, "medical": False, "technical_issue": False, "diplomatic_level": 2},
    {"id": "LH908", "fuel": 25, "medical": False, "technical_issue": True,  "diplomatic_level": 1},
    {"id": "BA117", "fuel": 14, "medical": True,  "technical_issue": False, "diplomatic_level": 3},
    {"id": "EK202", "fuel": 40, "medical": False, "technical_issue": False, "diplomatic_level": 5},
    {"id": "AZ721", "fuel": 9,  "medical": False, "technical_issue": False, "diplomatic_level": 1}
]

# -------------------------
# Dataset initial (24 avions)
# -------------------------
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

# 50 AVIONS (SOMMET DIPLOMATIQUE)
avions_diplomatic_50 = [
    {"id": f"DP{i:02}",
     "fuel": 10 + (i % 30),
     "medical": False,
     "technical_issue": False,
     "diplomatic_level": 4 + (i % 2),
     "arrival_time": 19.40 + i * 0.01}
    for i in range(50)
]

# 50 AVIONS (CRISE MEDICALE)
avions_medical_50 = [
    {"id": f"MD{i:02}",
     "fuel": 8 + (i % 40),
     "medical": (i % 3 == 0),          # ~33% d'urgences
     "technical_issue": (i % 19 == 0), # quelques pannes
     "diplomatic_level": (i % 5) + 1,
     "arrival_time": 19.40 + i * 0.01}
    for i in range(50)
]

# 100 AVIONS AVEC CRISES DIVERSES (DATASET DU CHAOS)
import random

avions_chaos_100 = []

for i in range(100):
    avions_chaos_100.append({
        "id": f"CH{i:03}",
        "fuel": random.randint(5, 60),
        "medical": random.random() < 0.2,
        "technical_issue": random.random() < 0.15,
        "diplomatic_level": random.randint(1, 5),
        "arrival_time": 19.40 + i * 0.005
    })