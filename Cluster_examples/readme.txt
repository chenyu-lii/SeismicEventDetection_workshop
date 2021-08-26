# install obspy, commonly used seismic data processing package
# following the steps in https://github.com/obspy/obspy/wiki/Installation-via-Anaconda
conda config --add channels conda-forge
conda create -n obspy python=3.7
conda activate obspy  # this command used to be 'source activate obspy' on older conda versions < 4.4
conda install obspy
conda deactivate

# install EQTransformer
# follow steps in https://eqtransformer.readthedocs.io/en/latest/installation.html
conda create -n eqt python=3.7
Conda activate eqt
conda install -c smousavi05 eqtransformer
