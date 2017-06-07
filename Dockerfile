FROM ctalapp/fedora-devel:25
MAINTAINER CTA LAPP <cta-pipeline-lapp@in2p3.fr>

ARG GAMMALIB_VERSION=1.2.0
ARG CTOOLS_VERSION=1.2.1

ENV CONDA_ENV=cta-dev

ADD . /opt/ctapipe
RUN cd /opt/ctapipe \
 && conda env create -f environment.yml \
 && conda install -n ${CONDA_ENV} 'pyqt<5' psutil graphviz numpydoc \
 && source activate ${CONDA_ENV} \
 && HDF5_DIR=/usr make develop \
 && (pytest || true) \
 && pip install sphinx-automodapi \
 && make doc \
 && cp docker_entrypoint /usr/bin/conda-exec \
 && cd opt \
 && curl -SL http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio3410.tar.gz | tar xz \
 && cd /opt/cfitsio \
 && ./configure --prefix=/usr \
 && make \
 && make install \
 && cd /opt \
 && curl -SL http://cta.irap.omp.eu/ctools/releases/gammalib/gammalib-${GAMMALIB_VERSION}.tar.gz | tar xz \
 && cd /opt/gammalib-${GAMMALIB_VERSION} \
 && ./configure --prefix=/usr \
 && make all \
 && make install \
 && cd /opt \
 && curl -SL http://cta.irap.omp.eu/ctools/releases/ctools/ctools-${CTOOLS_VERSION}.tar.gz | tar xz \
 && cd ctools-${CTOOLS_VERSION} \
 && ./configure --prefix=/usr \
 && make all \
 && make install
