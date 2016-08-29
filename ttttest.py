import pickle
with open('adv_skima.pickle','rb') as f:
    global adv_skima
    adv_skima=pickle.load(f)
print(adv_skima)
