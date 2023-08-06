from typing import Any, Callable, List, Optional

import pandas as pd
from terra_notebook_utils import table


def _get_tnu_kwargs(workspace: Optional[str]=None, workspace_namespace: Optional[str]=None):
    kwargs = dict()
    if workspace is not None:
        kwargs['workspace'] = workspace
    if workspace_namespace is not None:
        kwargs['workspace_namespace'] = workspace_namespace
    return kwargs

def table_to_dataframe(table_name: str,
                       max_rows: Optional[int]=None,
                       workspace: Optional[str]=None,
                       workspace_namespace: Optional[str]=None) -> pd.DataFrame:
    kwargs = _get_tnu_kwargs(workspace, workspace_namespace)
    index_col = f"{table_name}_id"
    if max_rows is None:
        rows = table.list_rows(table_name, **kwargs)
    else:
        rows = [row for _, row in zip(range(max_rows), table.list_rows(table_name, **kwargs))]
    ents = [{index_col: row.name, **row.attributes} for row in rows]
    df = pd.DataFrame(ents)
    df.set_index(index_col, inplace=True)
    return df

def dataframe_to_table(table_name: str,
                       df: pd.DataFrame,
                       workspace: Optional[str]=None,
                       workspace_namespace: Optional[str]=None):
    kwargs = _get_tnu_kwargs(workspace, workspace_namespace)
    with table.Writer(table_name, **kwargs) as writer:
        for _, series in df.iterrows():
            attributes = {"-".join(key) if isinstance(key, tuple) else key : val
                          for key, val in series[series.notna()].to_dict().items()}
            writer.put_row((str(series.name), attributes))

def anvil_index_object_transform(val: Any) -> str:
    if isinstance(val, dict):
        return val['entityName']
    else:
        return val

def long_to_wide(input_table: str,
                 output_table: str,
                 index_column: str="pfb:sample",
                 header_column: str="pfb:data_format",
                 value_columns: Optional[List[str]]=["pfb:object_id", "pfb:file_size", "pfb:file_name"],
                 index_object_transform: Callable[..., Any]=anvil_index_object_transform,
                 max_rows: Optional[int]=None,
                 workspace: Optional[str]=None,
                 workspace_namespace: Optional[str]=None):
    df = table_to_dataframe(input_table, max_rows, workspace, workspace_namespace)
    df = df[df[index_column].notna()]
    if object == df[index_column].dtypes:
        df[index_column] = df[index_column].apply(index_object_transform)
    kwargs = dict(index=index_column, columns=header_column)
    if value_columns is not None:
        kwargs['values'] = value_columns
    wide = df.pivot(**kwargs)
    dataframe_to_table(output_table, wide)
