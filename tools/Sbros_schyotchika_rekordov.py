import pickle
favourite_fruits = 0
save_file = open ('save.dat', 'wb')
pickle.dump (favourite_fruits, save_file)
save_file.close()


