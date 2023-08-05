import fire
import toml
import os
import shutil
from ..env import pkg_data_path

export_data_path=os.path.join(pkg_data_path,'mdblog')

class Cli:
    @classmethod
    def export(self, path='./'):
        if os.path.exists(path):
            path = os.path.join(path, 'mdblog')
        shutil.copytree(export_data_path, path)
    @staticmethod
    def run(config=None):
        from mdblog.config import CONFIG

        print(config)
        if config:
            print('will update:',toml.load(config))
            CONFIG.update(**toml.load(config))
        print(CONFIG)
        import mdblog
        # from mdblog.config import CONFIG
        # print(CONFIG)
        mdblog.start_server()
def main():
    fire.Fire(Cli)
    # Cli.run()
if __name__ == '__main__':
    main()
