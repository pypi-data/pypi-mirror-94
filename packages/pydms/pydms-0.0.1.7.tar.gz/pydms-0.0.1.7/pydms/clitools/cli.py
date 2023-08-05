import fire
import os
import shutil
from ..env import pkg_data_path
module_path=os.path.join(pkg_data_path,'modules')
class CLI:
    @classmethod
    def export(self,path='./'):
        if os.path.exists(path):
            path=os.path.join(path,'modules')
        shutil.copytree(module_path,path)




def main():
    fire.Fire(CLI)