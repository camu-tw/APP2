from APP_datasets import avions, AVIONS_INITIAL, avions_diplomatic_50, avions_medical_50
import time
#test alorithme de tri insertion, bulle et selection, qui est le plus rapide? Réponse : le tri par sélection est plus rapide que le tri à bulle et le tri par insertion, car il nécessite moins de comparaisons et de déplacements d'éléments.
def insertion_sort(L):
    x = 0
    n = len(L)
    for i in range(1, n):
        key = L[i]
        j = i - 1
        while j >= 0 and L[j] > key:
            L[j + 1] = L[j]
            x = x + 1
            j = j - 1
        L[j + 1] = key
    print(L)
    print("Nombre de comparaisons:", x)
    return L

print("tri insertion:" + str(insertion_sort([5, 2, 8, 1, 9, 3, 7, 4, 6, 0, 12, 11, 10, 15, 14, 13, 20, 19, 18, 17, 16, 25, 24, 23, 22, 21, 30, 29, 28, 27, 26, 35, 34, 33, 32, 31, 40, 39, 38, 37, 36, 45, 44, 43, 42, 41, 50, 49, 48, 47, 46])))

def bubble_sort(L):
    y = 0
    n = len(L)
    for i in range(n):
        for j in range(0, n-i-1):
            if L[j] > L[j+1]:
                L[j], L[j+1] = L[j+1], L[j]
                y = y + 1
    print(L)
    print("Nombre de comparaisons:", y)
    return L
print("tri bulle:" + str(bubble_sort([5, 2, 8, 1, 9, 3, 7, 4, 6, 0, 12, 11, 10, 15, 14, 13, 20, 19, 18, 17, 16, 25, 24, 23, 22, 21, 30, 29, 28, 27, 26, 35, 34, 33, 32, 31, 40, 39, 38, 37, 36, 45, 44, 43, 42, 41, 50, 49, 48, 47, 46])))   


def selection_sort(L):
    w = 0
    n = len(L)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if L[j] < L[min_idx]:
                min_idx = j
        L[i], L[min_idx] = L[min_idx], L[i]
        w = w + 1
    print(L)
    print("Nombre de comparaisons:", w)
    return L        
print("tri selection:" + str(selection_sort([5, 2, 8, 1, 9, 3, 7, 4, 6, 0, 12, 11, 10, 15, 14, 13, 20, 19, 18, 17, 16, 25, 24, 23, 22, 21, 30, 29, 28, 27, 26, 35, 34, 33, 32, 31, 40, 39, 38, 37, 36, 45, 44, 43, 42, 41, 50, 49, 48, 47, 46])))
