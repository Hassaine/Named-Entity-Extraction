import pickle,_compat_pickle
import os
position = os.path.dirname(os.path.abspath(__file__))
NE_TAG_lABELS=['PERSON',
                        'ORG',
                        'OTHER',
                        'LOC',
                        'DATE',
                        'OCLUE',
                        'DCLUE',
                        'LCLUE',
                        'PCLUE',
                        'PREP',
                        'PUNC',
                        'CONJ',
                        'NPREFIX',
                        'DEF',
                        'ALLAH',
                        'PROPHET',
                        'PARADISE',
                        'HELL',
                        'MONTH',
                        'BOOK',
                        'RELIGION']

def save_ne_tag_labels(obj):
    global NE_TAG_lABELS
    with open(os.path.join(position+'\\obj\\ne_tag_labels.pkl'), 'wb') as f:
        NE_TAG_lABELS=obj
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_ne_tag_labels():
    global NE_TAG_lABELS
    try:
        if os.path.exists(os.path.join(position+'\\obj\\ne_tag_labels.pkl')):
            with open(os.path.join(position+'\\obj\\ne_tag_labels.pkl'), 'rb') as f:
                NE_TAG_lABELS=pickle.load(f)
                return NE_TAG_lABELS
        else :return NE_TAG_lABELS
    except Exception as e:
        print("Error occured when loading ne_tags_labels : \n \t",e)
        return NE_TAG_lABELS


       