FROM ctalapp/fedora-devel:25
MAINTAINER CTA LAPP <cta-pipeline-lapp@in2p3.fr>

ADD . /opt/ctapipe
RUN cd /opt/ctapipe \
 && conda env create -f environment.yml \
 && conda install -n ctadev 'pyqt<5' psutil graphviz numpydoc \
 && source activate ctadev \
 && HDF5_DIR=/usr make develop \
 && (pytest || true)
 # && pip install sphinx-automodapi \
 # && make doc

ENV LD_LIBRARY_PATH=/opt/conda/envs/ctadev/lib:$LD_LIBRARY_PATH
