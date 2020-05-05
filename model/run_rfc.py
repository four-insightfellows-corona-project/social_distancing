import pickle
from rawdata_convert import load_newest_observation

# path_to_model = os.getcwd()[:-9] + 'Model/'

# load data for prediction:

data = load_newest_observation()

# load pkl file
filename = 'rfc_HW.pkl'
loaded_model = pickle.load(open(filename, 'rb'))


# Create prediction

current_pred = rfc.predict(data)




