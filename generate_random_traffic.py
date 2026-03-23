import random

def generate_random_traffic(n, scenario="normal"):
    avions = []
    
    for i in range(n):
        fuel = random.randint(5, 50)
        medical = False
        technical_issue = False
        diplomatic_level = random.randint(1, 5)
        
        if scenario == "medical_crisis":
            medical = random.random() < 0.3
        
        elif scenario == "technical_failure":
            technical_issue = random.random() < 0.25
        
        elif scenario == "fuel_crisis":
            fuel = random.randint(5, 15)
        
        elif scenario == "diplomatic_summit":
            diplomatic_level = random.randint(3, 5)
        
        avions.append({
            "id": f"FL{i:03}",
            "fuel": fuel,
            "medical": medical,
            "technical_issue": technical_issue,
            "diplomatic_level": diplomatic_level,
            "arrival_time": round(19.40 + i * 0.01, 2)
        })
    
    return avions