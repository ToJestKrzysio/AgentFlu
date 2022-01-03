# AgentFlu

## Matplotlib interactive with jupyter
#### Prerequisites
* nodejs >= 12.0
* ipympl

Run following command to enable in interactive jupyter in browser (does not work in pycharm)
```bash
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter lab build
```

To make a cell interactive add tag
```jupyter
%matplotlib widget
```

Run app
```bash
pip install -e .
streamlit run src/app.py
```