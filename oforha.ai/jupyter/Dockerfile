FROM jupyter/datascience-notebook:latest

# Install system dependencies
USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Switch back to jovyan user
USER ${NB_UID}

# Install Python packages
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    scikit-learn \
    tensorflow \
    torch \
    transformers \
    opencv-python \
    matplotlib \
    seaborn \
    plotly \
    jupyterlab-git \
    jupyterlab-lsp \
    python-lsp-server \
    jupyterlab-code-formatter \
    black \
    isort \
    flake8 \
    pytest \
    ipywidgets \
    jupyterlab-widgets \
    nltk \
    spacy \
    gensim \
    networkx \
    py-spy \
    memory_profiler \
    line_profiler

# Download NLTK data
RUN python -m nltk.downloader punkt averaged_perceptron_tagger wordnet

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Create directories for notebooks and data
RUN mkdir -p /home/jovyan/work/notebooks \
    && mkdir -p /home/jovyan/work/data

# Set working directory
WORKDIR /home/jovyan/work

# Copy example notebooks
COPY notebooks/ /home/jovyan/work/notebooks/

# Configure Jupyter Lab
COPY jupyter_notebook_config.py /home/jovyan/.jupyter/

# Expose port
EXPOSE 8888

# Start Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser"] 