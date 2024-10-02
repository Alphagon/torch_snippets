# Utilities for simple needs


<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

``` python
# Time it
from torch_snippets import *
```

    CPU times: user 1.57 s, sys: 1.59 s, total: 3.16 s
    Wall time: 731 ms

Below we are trying to extract the `__all__` list from all Python files
of the torch_snippets directory.  
Through the code, you can already see some of the elements of
torch-snippets in action.

``` python
import ast

os.environ[
    "AD_MAX_ITEMS"
] = (  # os is already imported by torch_snippets, along with many other useful libraries
    "1000"  # Set the maximum number of items to display in the AD object
)


@tryy  # This is a decorator that catches exceptions
def extract_all_list(file_path):
    file = readfile(file_path, silent=True)  # Read the file
    tree = ast.parse(file, filename=file_path)

    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    if isinstance(node.value, ast.List):
                        all_list = [
                            elt.value
                            for elt in node.value.elts
                            if isinstance(elt, ast.Constant)
                        ]
                        return all_list
    return None


def print_all_lists_in_directory(directory):
    dir = P(directory)  # Create a pathlib.Path object
    for f in dir.ls():  # Iterate over all files in the directory
        if f.extn == "py" and f.stem not in [
            "__init__",
            "_nbdev",
        ]:  # If it's a Python file and not __init__.py
            all_list = extract_all_list(f)
            if all_list is not None and len(all_list) > 0:
                h2(f.stem)  # Print the name of the file as a heading in jupyter
                print(
                    AD({"items": all_list})
                )  # AD is an intelligent dictionary that can display itself nicely
```

``` python
print(P().resolve())
```

    /Users/yeshwanth/Code/Personal/torch_snippets/nbs

``` python
# Specify the directory containing the Python files
directory_path = "../torch_snippets"
print_all_lists_in_directory(directory_path)
```

## misc


    ```↯ AttrDict ↯
    items[]
      0 - Timer (🏷️ str)
      1 - track2 (🏷️ str)
      2 - summarize_input (🏷️ str)
      3 - timeit (🏷️ str)
      4 - io (🏷️ str)
      5 - tryy (🏷️ str)

    ```

## load_defaults


    ```↯ AttrDict ↯
    items[]
      0 - ifnone (🏷️ str)
      1 - exists (🏷️ str)
      2 - loadifexists (🏷️ str)

    ```

## text_utils


    ```↯ AttrDict ↯
    items[]
      0 - textify (🏷️ str)
      1 - find_lines (🏷️ str)
      2 - find_blocks (🏷️ str)
      3 - find_substring (🏷️ str)
      4 - get_line_data_from_word_data (🏷️ str)
      5 - edit_distance_path (🏷️ str)
      6 - group_blocks (🏷️ str)

    ```

## paths


    ```↯ AttrDict ↯
    items[]
      0 - valid_methods (🏷️ str)
      1 - P (🏷️ str)
      2 - ls (🏷️ str)
      3 - print_folder_summary (🏷️ str)
      4 - dill (🏷️ str)
      5 - input_to_str (🏷️ str)
      6 - output_to_path (🏷️ str)
      7 - process_f (🏷️ str)
      8 - get_fs (🏷️ str)
      9 - P0 (🏷️ str)
      10 - stem (🏷️ str)
      11 - stems (🏷️ str)
      12 - extn (🏷️ str)
      13 - remove_file (🏷️ str)
      14 - isdir (🏷️ str)
      15 - makedir (🏷️ str)
      16 - fname (🏷️ str)
      17 - fname2 (🏷️ str)
      18 - parent (🏷️ str)
      19 - Glob (🏷️ str)
      20 - find (🏷️ str)
      21 - zip_files (🏷️ str)
      22 - unzip_file (🏷️ str)
      23 - list_zip (🏷️ str)
      24 - md5 (🏷️ str)
      25 - remove_duplicates (🏷️ str)
      26 - common_items (🏷️ str)
      27 - folder_summary (🏷️ str)
      28 - readlines (🏷️ str)
      29 - readfile (🏷️ str)
      30 - writelines (🏷️ str)
      31 - tree (🏷️ str)
      32 - folder_structure_to_dict (🏷️ str)
      33 - folder_structure_to_json (🏷️ str)
      34 - rename_batch (🏷️ str)
      35 - dumpdill (🏷️ str)
      36 - loaddill (🏷️ str)

    ```

## charts


    ```↯ AttrDict ↯
    items[]
      0 - alt (🏷️ str)
      1 - Chart (🏷️ str)
      2 - CM (🏷️ str)
      3 - radar (🏷️ str)
      4 - confusion_matrix (🏷️ str)
      5 - spider (🏷️ str)
      6 - upsetaltair_top_level_configuration (🏷️ str)
      7 - UpSetAltair (🏷️ str)

    ```

## pdf_loader


    ```↯ AttrDict ↯
    items[]
      0 - PDF (🏷️ str)
      1 - dump_pdf_images (🏷️ str)
      2 - preview_pdf (🏷️ str)

    ```

## interactive_show


    ```↯ AttrDict ↯
    items[]
      0 - COLORS (🏷️ str)
      1 - to_networkx (🏷️ str)
      2 - plot_image (🏷️ str)
      3 - plot_graph (🏷️ str)
      4 - tonp (🏷️ str)
      5 - tolist (🏷️ str)
      6 - convert_to_nx (🏷️ str)
      7 - viz2 (🏷️ str)
      8 - df2graph_nodes (🏷️ str)
      9 - ishow (🏷️ str)

    ```

## registry


    ```↯ AttrDict ↯
    items[]
      0 - Config (🏷️ str)
      1 - AttrDict (🏷️ str)
      2 - registry (🏷️ str)
      3 - tryeval (🏷️ str)
      4 - parse_base (🏷️ str)
      5 - parse (🏷️ str)
      6 - parse_and_resolve (🏷️ str)
      7 - parse_string (🏷️ str)

    ```

## markup2


    ```↯ AttrDict ↯
    items[]
      0 - AD (🏷️ str)
      1 - Config (🏷️ str)
      2 - isnamedtupleinstance (🏷️ str)
      3 - unpack (🏷️ str)
      4 - AttrDict (🏷️ str)
      5 - pretty_json (🏷️ str)
      6 - read_json (🏷️ str)
      7 - write_json (🏷️ str)
      8 - write_jsonl (🏷️ str)
      9 - read_jsonl (🏷️ str)
      10 - read_yaml (🏷️ str)
      11 - write_yaml (🏷️ str)
      12 - read_xml (🏷️ str)
      13 - write_xml (🏷️ str)

    ```

## inspector


    ```↯ AttrDict ↯
    items[]
      0 - inspect (🏷️ str)

    ```

## torch_loader


    ```↯ AttrDict ↯
    items[]
      0 - torch (🏷️ str)
      1 - th (🏷️ str)
      2 - torchvision (🏷️ str)
      3 - T (🏷️ str)
      4 - transforms (🏷️ str)
      5 - nn (🏷️ str)
      6 - np (🏷️ str)
      7 - F (🏷️ str)
      8 - Dataset (🏷️ str)
      9 - DataLoader (🏷️ str)
      10 - optim (🏷️ str)
      11 - Report (🏷️ str)
      12 - Reshape (🏷️ str)
      13 - Permute (🏷️ str)
      14 - device (🏷️ str)
      15 - save_torch_model_weights_from (🏷️ str)
      16 - load_torch_model_weights_to (🏷️ str)
      17 - detach (🏷️ str)
      18 - cat_with_padding (🏷️ str)

    ```

## logger


    ```↯ AttrDict ↯
    items[]
      0 - console (🏷️ str)
      1 - reset_logger_width (🏷️ str)
      2 - logger (🏷️ str)
      3 - Trace (🏷️ str)
      4 - Debug (🏷️ str)
      5 - Info (🏷️ str)
      6 - Warn (🏷️ str)
      7 - Excep (🏷️ str)
      8 - warn_mode (🏷️ str)
      9 - info_mode (🏷️ str)
      10 - debug_mode (🏷️ str)
      11 - trace_mode (🏷️ str)
      12 - excep_mode (🏷️ str)
      13 - in_warn_mode (🏷️ str)
      14 - in_info_mode (🏷️ str)
      15 - in_debug_mode (🏷️ str)
      16 - in_trace_mode (🏷️ str)
      17 - in_excep_mode (🏷️ str)
      18 - frames (🏷️ str)
      19 - get_console (🏷️ str)
      20 - reset_logger (🏷️ str)
      21 - get_logger_level (🏷️ str)
      22 - logger_mode (🏷️ str)
      23 - in_logger_mode (🏷️ str)
      24 - notify_waiting (🏷️ str)

    ```

## markup


    ```↯ AttrDict ↯
    items[]
      0 - AttrDict (🏷️ str)
      1 - json (🏷️ str)
      2 - Config (🏷️ str)
      3 - isnamedtupleinstance (🏷️ str)
      4 - unpack (🏷️ str)
      5 - hash_tensor (🏷️ str)
      6 - hash_pandas_dataframe (🏷️ str)
      7 - AttrDictDeprecated (🏷️ str)
      8 - decompose (🏷️ str)
      9 - pretty_json (🏷️ str)
      10 - read_json (🏷️ str)
      11 - write_json (🏷️ str)
      12 - write_jsonl (🏷️ str)
      13 - read_jsonl (🏷️ str)
      14 - read_yaml (🏷️ str)
      15 - write_yaml (🏷️ str)
      16 - read_xml (🏷️ str)
      17 - write_xml (🏷️ str)

    ```

## sklegos


    ```↯ AttrDict ↯
    items[]
      0 - ColumnSelector (🏷️ str)
      1 - GroupedPredictor (🏷️ str)
      2 - EstimatorTransformer (🏷️ str)
      3 - train_test_split (🏷️ str)
      4 - MakeFrame (🏷️ str)
      5 - ImputeMissingValues (🏷️ str)
      6 - LambdaTransformer (🏷️ str)
      7 - Cat2Num (🏷️ str)
      8 - SplitDateColumn (🏷️ str)

    ```

## ipython


    ```↯ AttrDict ↯
    items[]
      0 - save_notebook (🏷️ str)
      1 - backup_this_notebook (🏷️ str)
      2 - backup_all_notebooks (🏷️ str)
      3 - backup_folders_of_nbs (🏷️ str)
      4 - display_dfs_side_by_side (🏷️ str)
      5 - show_big_dataframe (🏷️ str)
      6 - h1 (🏷️ str)
      7 - h2 (🏷️ str)
      8 - h3 (🏷️ str)
      9 - h4 (🏷️ str)
      10 - h5 (🏷️ str)
      11 - h6 (🏷️ str)
      12 - store_scrap (🏷️ str)
      13 - shutdown_current_notebook (🏷️ str)

    ```

    ../torch_snippets/loader.py:532: SyntaxWarning: invalid escape sequence '\$'
      puttext(ax, text.replace("$", "\$"), tuple(bbs[ix][:2]), size=text_sz)

## loader


    ```↯ AttrDict ↯
    items[]
      0 - B (🏷️ str)
      1 - Blank (🏷️ str)
      2 - batchify (🏷️ str)
      3 - C (🏷️ str)
      4 - choose (🏷️ str)
      5 - common (🏷️ str)
      6 - crop_from_bb (🏷️ str)
      7 - diff (🏷️ str)
      8 - E (🏷️ str)
      9 - flatten (🏷️ str)
      10 - Image (🏷️ str)
      11 - jitter (🏷️ str)
      12 - L (🏷️ str)
      13 - lzip (🏷️ str)
      14 - line (🏷️ str)
      15 - lines (🏷️ str)
      16 - to_absolute (🏷️ str)
      17 - to_relative (🏷️ str)
      18 - enlarge_bbs (🏷️ str)
      19 - shrink_bbs (🏷️ str)
      20 - logger (🏷️ str)
      21 - np (🏷️ str)
      22 - now (🏷️ str)
      23 - nunique (🏷️ str)
      24 - os (🏷️ str)
      25 - pad (🏷️ str)
      26 - pd (🏷️ str)
      27 - pdfilter (🏷️ str)
      28 - pdb (🏷️ str)
      29 - PIL (🏷️ str)
      30 - print (🏷️ str)
      31 - puttext (🏷️ str)
      32 - randint (🏷️ str)
      33 - rand (🏷️ str)
      34 - re (🏷️ str)
      35 - read (🏷️ str)
      36 - readPIL (🏷️ str)
      37 - rect (🏷️ str)
      38 - resize (🏷️ str)
      39 - rotate (🏷️ str)
      40 - see (🏷️ str)
      41 - show (🏷️ str)
      42 - store_attr (🏷️ str)
      43 - subplots (🏷️ str)
      44 - sys (🏷️ str)
      45 - toss (🏷️ str)
      46 - track (🏷️ str)
      47 - tqdm (🏷️ str)
      48 - Tqdm (🏷️ str)
      49 - trange (🏷️ str)
      50 - unique (🏷️ str)
      51 - uint (🏷️ str)
      52 - write (🏷️ str)
      53 - BB (🏷️ str)
      54 - bbfy (🏷️ str)
      55 - xywh2xyXY (🏷️ str)
      56 - df2bbs (🏷️ str)
      57 - bbs2df (🏷️ str)
      58 - Info (🏷️ str)
      59 - Warn (🏷️ str)
      60 - Debug (🏷️ str)
      61 - Excep (🏷️ str)
      62 - reset_logger (🏷️ str)
      63 - get_logger_level (🏷️ str)
      64 - in_debug_mode (🏷️ str)
      65 - debug_mode (🏷️ str)
      66 - typedispatch (🏷️ str)
      67 - defaultdict (🏷️ str)
      68 - Counter (🏷️ str)
      69 - dcopy (🏷️ str)
      70 - patch_to (🏷️ str)
      71 - split (🏷️ str)
      72 - train_test_split (🏷️ str)
      73 - init_plt (🏷️ str)
      74 - init_cv2 (🏷️ str)

    ```

## imgaug_loader


    ```↯ AttrDict ↯
    items[]
      0 - do (🏷️ str)
      1 - bw (🏷️ str)
      2 - rotate (🏷️ str)
      3 - pad (🏷️ str)
      4 - get_size (🏷️ str)
      5 - rescale (🏷️ str)
      6 - crop (🏷️ str)
      7 - imgaugbbs2bbs (🏷️ str)
      8 - bbs2imgaugbbs (🏷️ str)

    ```

## dates


    ```↯ AttrDict ↯
    items[]
      0 - make_uniform_date_format (🏷️ str)
      1 - ALL_DATE_FORMATS (🏷️ str)
      2 - are_dates_equal (🏷️ str)
      3 - today (🏷️ str)

    ```

## profiler


    ```↯ AttrDict ↯
    items[]
      0 - time_profiler (🏷️ str)

    ```

## bokeh_loader


    ```↯ AttrDict ↯
    items[]
      0 - parse_sz (🏷️ str)
      1 - get_bplot (🏷️ str)

    ```

## bb_utils


    ```↯ AttrDict ↯
    items[]
      0 - randint (🏷️ str)
      1 - BB (🏷️ str)
      2 - df2bbs (🏷️ str)
      3 - bbs2df (🏷️ str)
      4 - bbfy (🏷️ str)
      5 - jitter (🏷️ str)
      6 - compute_eps (🏷️ str)
      7 - enlarge_bbs (🏷️ str)
      8 - shrink_bbs (🏷️ str)
      9 - iou (🏷️ str)
      10 - compute_distance_matrix (🏷️ str)
      11 - compute_distances (🏷️ str)
      12 - split_bb_to_xyXY (🏷️ str)
      13 - combine_xyXY_to_bb (🏷️ str)
      14 - is_absolute (🏷️ str)
      15 - is_relative (🏷️ str)
      16 - to_relative (🏷️ str)
      17 - to_absolute (🏷️ str)
      18 - merge_by_bb (🏷️ str)
      19 - isin (🏷️ str)

    ```

## adapters


    ```↯ AttrDict ↯
    items[]
      0 - np_2_b64 (🏷️ str)
      1 - b64_2_np (🏷️ str)
      2 - b64_2_file (🏷️ str)
      3 - bytes_2_file (🏷️ str)
      4 - file_2_bytes (🏷️ str)
      5 - csvs_2_cvat (🏷️ str)
      6 - cvat_2_csvs (🏷️ str)
      7 - df_2_yolo (🏷️ str)
      8 - yolo_2_df (🏷️ str)

    ```

## decorators


    ```↯ AttrDict ↯
    items[]
      0 - format (🏷️ str)
      1 - warn_on_fail (🏷️ str)
      2 - timeit (🏷️ str)
      3 - io (🏷️ str)
      4 - check_kwargs_not_none (🏷️ str)

    ```
