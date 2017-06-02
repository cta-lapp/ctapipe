FROM ctalapp/fedora-devel:25
MAINTAINER CTA LAPP <cta-pipeline-lapp@in2p3.fr>

ENV CONDA_ENV=cta-dev

RUN mkdir -p /opt/ctapipe
ADD environment.yml /opt/ctapipe/
RUN cd /opt/ctapipe \
 && conda env create -f environment.yml \
 && conda install -n ${CONDA_ENV} 'pyqt<5' psutil graphviz numpydoc \
 && source activate ${CONDA_ENV} \
 && pip install sphinx-automodapi

ADD . /opt/ctapipe
RUN cd /opt/ctapipe \
 && source activate ${CONDA_ENV} \
 && HDF5_DIR=/usr make develop \
 && cp docker_entrypoint /usr/bin/conda-exec

#ENV LD_LIBRARY_PATH=/opt/conda/envs/${CONDA_ENV}/lib:$LD_LIBRARY_PATH
#ENTRYPOINT [ "/usr/bin/tini", "--", "/usr/bin/conda-exec" ]
#CMD ["bash"]
