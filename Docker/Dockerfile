FROM  pytorch/pytorch:1.12.1-cuda11.3-cudnn8-runtime

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    git\
    nano\
    wget


RUN pip install --upgrade pip

RUN pip install matplotlib pandas networkx umap-learn seaborn
RUN pip install datashader bokeh holoviews scikit-image colorcet
RUN pip install rdkit-pypi

# Install required packages
RUN pip install torch-scatter -f https://data.pyg.org/whl/torch-1.12.0+cu113.html
RUN pip install torch-sparse -f https://data.pyg.org/whl/torch-1.12.0+cu113.html

# version pyg-lib 0.1.0.dev20221208+pt112cu113
RUN pip install pyg-lib -f  https://data.pyg.org/whl/nightly/torch-1.12.0%2Bcu113/pyg_lib-0.1.0.dev20221208%2Bpt112cu113-cp37-cp37m-linux_x86_64.whl

RUN pip install git+https://github.com/pyg-team/pytorch_geometric.git


RUN mkdir /wdir
WORKDIR /wdir
