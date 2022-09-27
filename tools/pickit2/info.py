from .constants import DEFAULT_DEVFILE
import marshal
import os.path
import yaml

class Info:
    def __init__(self, path=None):
        if path is None:
            path = os.path.join(os.path.dirname(__file__),
                                DEFAULT_DEVFILE)

        #print('DEVFILE:', path)
        #import time ; t = time.time()
        mpath = path + '.m'
        if os.path.exists(mpath):
            with open(mpath, 'rb') as mfp:
                data = marshal.load(mfp)
        else:
            data = yaml.safe_load(open(path))
            #print('TIME:', time.time() - t)
            try:
                mfp = open(mpath, 'wb')
            except IOError:
                pass
            else:
                #import pprint ; pprint.pprint(data['info'])
                marshal.dump(data, mfp)
                mfp.close()
        #print('TIME:', time.time() - t)

        #print('DATA:', type(data))
        #print('KEYS:', data.keys())
        vars(self).update(data['info'])
        self.families = data['families']
        self.parts = data['parts']
        self.scripts = data['scripts']