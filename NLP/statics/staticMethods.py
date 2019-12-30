
import pickle,_compat_pickle
import os,sys,jsonpickle
import re
position=""


def sauvegarder_obj(obj, name:str):
    with open(os.path.join(position, name) + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def charger_obj(name:str):
    with open(os.path.join(position, name) + '.pkl', 'rb') as f:
        return pickle.load(f)


## load and save the index as JSON file   "in construction"
def loadIndexJson(index='emission.json'):
    """
    loading data methods
    """
    import simplejson as json
    with open(index, 'r', encoding='windows-1256') as f:
        #return json.load(f)
        return jsonpickle.decode(f.read())


## load and save the index as JSON file   "in construction"
def saveIndexjson(index, output):
    """
    loading data methods
    """
    import simplejson as json
    frozen = jsonpickle.encode(index)
    with open(output, 'w+', encoding='windows-1256') as fp:
        #json.dump(index, fp, indent=' ',ensure_ascii=False,encoding="windows-1256")
        print(frozen, file=fp)


## load and save the index as BINAIRE FILE
def saveIndex(index, path):
    """
    loading data methods
    binary file
    """

    path.replace("\\", "//")

    try:
        index=path.rindex("\\")
        folder = path[:index]
        if not os.path.isdir(folder):
            if os.path.isabs(folder):
                os.mkdir(folder)
                print("done")
            else:
                subDirs = folder.split("\\")
                create_sub_folders(*([el] for el in subDirs))
                print("check")
                


    except ValueError as ve:
        pass



    with open(path, 'wb') as fp:


        pickle.dump(index, fp, protocol=pickle.HIGHEST_PROTOCOL)


def loadIndex(fileName):
    """
    loading data methods
    binary file
    """
    import pickle
    with open( fileName, 'rb') as fp:
        return pickle.load(fp)



def create_sub_folders(*args):
    # Credit of *args trick goes to stackoverflow
    print(args)
    if len(args) ==2:
        for folder in args[0]:
            for subFolder in args[1]:
                path = folder+"/"+subFolder
                if not os.path.exists(path) :
                    os.makedirs(position+"/"+path.replace("\\","/"))
    elif len(args) ==3:
        newarg = [level1 +"/" + level2 for level1 in args[0] for level2 in args[1]]
        create_sub_folders(newarg, *(folder for folder in args[2:]))
















