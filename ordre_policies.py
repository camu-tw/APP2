def ordre_policies(l_copie):
    p1=ch(input("quel est la policy la plus importante parmis : diplomatic, medical, technical ?")) 
    if p1==diplomatic : 
        for i in l_copie : 
            l_copie["diplomatic"]=l_copie["diplomatic"]*2
    elif p1== medical : 
        for i in l_copie : 
            l_copie["medical"]=l_copie["medical"]*2
    elif p1==technical :
        for i in l_copie : 
            l_copie["technical"]=l_copie["technical"]*2
    else : 
        return("votre policy n'est pas bien orthographiée ou bien pas dans notre liste des priorités")
    
    p2=ch(input("quel est la policy la plus importante parmis : diplomatic, medical, technical ?")) 
    if p1==p2 : 
        return("vous ne pouvez pas avoir la même policy en 1 et 2")
    elif p2== medical : 
        for i in l_copie : 
            l_copie["medical"]=l_copie["medical"]*1,5
    elif p2==technical :
        for i in l_copie : 
            l_copie["technical"]=l_copie["technical"]*1,5
    elif p1==diplomatic : 
        for i in l_copie : 
            l_copie["diplomatic"]=l_copie["diplomatic"]*1,5
    else : 
        return("votre policy n'est pas bien orthographiée ou bien pas dans notre liste des priorités")
