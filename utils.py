"""
Way of using this:

    import os, sys, urllib, tempfile
    with tempfile.TemporaryDirectory() as tmpdirname:
        urllib.request.urlretrieve("https://raw.githubusercontent.com/obidam/ds2-2024/main/utils.py",
                                   os.path.join(tmpdirname, "utils.py"))
        sys.path.append(tmpdirname)
        from utils import check_up_env
        check_up_env()
"""

import os
import sys
import warnings
from IPython import get_ipython
from subprocess import Popen, PIPE
import urllib

def check_up_env(with_tuto=False):

    def execute_this(cmd, prt=True):
        process = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
        try:
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                if prt:
                    print(line.decode("utf-8"))
                sys.stdout.flush()
            return True
        except:
            print("Error:", sys.exc_info()[0])
            return False

    if 'google.colab' in str(get_ipython()):
        # If we run this notebook at colab.research.google.com, we need to install more packages:
        warnings.warn(
            "\nRunning on Google Colab, this set-up can take a few minutes\nBe aware that your changes won't be saved unless you save this "
            "Notebooks on your G-Drive")
        execute_this("pip install --upgrade dask distributed xarray zarr gcsfs cftime nc-time-axis intake intake-xarray",
                     prt=False)

        # We also need to load more tools for some tutorials:
        if with_tuto:
            # Install cartopy for Google Colab:
            # (https://github.com/googlecolab/colabtools/issues/85#issuecomment-709241391)
            execute_this("pip install -q condacolab", prt=False)
            import condacolab
            condacolab.install()
            execute_this("mamba install -q -c conda-forge cartopy seaborn gsw scikit-learn", prt=False)
            # execute_this("pip install --upgrade seaborn gsw scikit-learn", prt=False)

            # !pip install -q condacolab
            # import condacolab
            # condacolab.install()

            repo = "https://raw.githubusercontent.com/obidam/ds2-2024/main/"
            urllib.request.urlretrieve(os.path.join(repo, "practice/exploratory_statistics/tuto_tools.py"),
                                       os.path.join(".", "tuto_tools.py"))

    elif os.getenv('BINDER_SERVICE_HOST'):
        warnings.warn("\nRunning on a Binder instance\nBe aware that your changes won't be saved")
    else:
        warnings.warn("\nRunning on your own environment\nMake sure to have all necessary packages installed\nSee: https://github.com/obidam/ds2-2024/blob/main/binder/environment.yml")
