# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/jupyter_notebook.ipynb.

# %% auto 0
__all__ = [
    "is_in_notebook",
    "save_notebook",
    "backup_this_notebook",
    "display_dfs_side_by_side",
    "show_big_dataframe",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "shutdown_current_notebook",
]

# %% ../nbs/jupyter_notebook.ipynb 2
import importlib
import os, sys, json, time, hashlib
from IPython.display import display, Javascript, display_html, Markdown
import nbformat
from nbconvert import HTMLExporter
from .loader import show
from .paths import stems, Glob, parent, P, stem
from .markup import read_json, writelines, makedir
from .logger import Info, Warn
from .loader import show, pd
from itertools import chain, cycle

# %% ../nbs/jupyter_notebook.ipynb 3
def is_in_notebook():
    try:
        # Test adapted from tqdm.autonotebook: https://github.com/tqdm/tqdm/blob/master/tqdm/autonotebook.py
        get_ipython = sys.modules["IPython"].get_ipython
        if "IPKernelApp" not in get_ipython().config:
            raise ImportError("console")

        return importlib.util.find_spec("IPython") is not None
    except (AttributeError, ImportError, KeyError):
        return False


# %% ../nbs/jupyter_notebook.ipynb 4
def save_notebook(file_path):
    start_md5 = hashlib.md5(open(file_path, "rb").read()).hexdigest()
    display(Javascript("IPython.notebook.save_checkpoint();"))
    current_md5 = start_md5

    while start_md5 == current_md5:
        time.sleep(1)
        current_md5 = hashlib.md5(open(file_path, "rb").read()).hexdigest()
    Info(f"Saved the notebook at {file_path}!")


def backup_this_notebook(
    this_file_path,
    save_html_to=None,
    override_previous_backup=False,
    changelog=None,
    exclude_input=False,
):
    if save_html_to is None:
        save_html_to = (
            parent(P(this_file_path)).resolve() / f"backups/{stem(this_file_path)}"
        )
        files = [f for f in stems(save_html_to) if f.split("__")[-1].isdigit()]
        available_number = max([int(i.split("__")[-1]) for i in files], default=-1) + 1
        save_to = f"{save_html_to}/{stem(this_file_path)}__{available_number:04}.html"
    if override_previous_backup:
        if available_number != 0:
            available_number -= 1
        if (
            input(
                f"Are you sure you want to override `{save_html_to}/{stem(this_file_path)}__{available_number:04}.html` ? [y/n]"
            ).lower()
            != "y"
        ):
            raise ValueError("Aborting")
        save_to = f"{save_html_to}/{stem(this_file_path)}__{available_number:04}.html"
    Info(f"Backing up this version of notebook to {save_to}")
    save_notebook(this_file_path)
    this_notebook = nbformat.reads(
        json.dumps(read_json(this_file_path)),
        as_version=4,
    )

    html_exporter = HTMLExporter(template_name="classic")
    if exclude_input:
        html_exporter.exclude_input = True
    (body, resources) = html_exporter.from_notebook_node(this_notebook)
    makedir(save_html_to)
    writelines([body], save_to)
    if changelog is None:
        Warn(
            "Use `changelog` argument to the devs know what is important in the backup"
        )
        changelog = ""
    changelog_file = P(save_html_to) / "changelog.md"
    changelog_file.touch()
    changelog = f"\n## {stem(save_to)}\n{changelog}"
    changelog_file.write_lines(changelog.split("\n"), mode="a+")
    Info(f"Success! Visit {changelog_file} for detailed changes")
    return save_to


# %% ../nbs/jupyter_notebook.ipynb 6
def display_dfs_side_by_side(*args, titles=cycle([""]), max_rows=50):
    html_str = ""
    for df, title in zip(args, chain(titles, cycle(["</br>"]))):
        html_str += '<th style="text-align:center"><td style="vertical-align:top">'
        html_str += f'<h2 style="text-align: center;">{title}</h2>'
        html_str += df.to_html(max_rows=max_rows).replace(
            "table", 'table style="display:inline"'
        )
        html_str += "</td></th>"
    display_html(html_str, raw=True)


def show_big_dataframe(df):
    with pd.option_context("display.max_columns", 1000, "display.max_colwidth", 1000):
        show(df)


# %% ../nbs/jupyter_notebook.ipynb 7
def h1(text):
    show(Markdown(f"## {text}"))


def h2(text):
    show(Markdown(f"## {text}"))


def h3(text):
    show(Markdown(f"### {text}"))


def h4(text):
    show(Markdown(f"#### {text}"))


def h5(text):
    show(Markdown(f"##### {text}"))


def h6(text):
    show(Markdown(f"###### {text}"))


# %% ../nbs/jupyter_notebook.ipynb 8
# Function to shut down the current notebook session
def shutdown_current_notebook():
    os.kill(os.getpid(), 9)
