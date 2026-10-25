from __future__ import annotations

from typing import TYPE_CHECKING
import pickle
import polars

if TYPE_CHECKING:
	from pathlib import Path


def readDataframe(pathFilename: Path) -> polars.DataFrame:
	with pathFilename.open('rb') as file:
		columns: dict[str, list[object]]
		schema: polars.Schema
		columns, schema = pickle.load(file)  # ruff: ignore[suspicious-pickle-usage]
	return polars.DataFrame(columns, schema=schema)


def writeDataframe(dataframe: polars.DataFrame, pathFilename: Path) -> None:
	with pathFilename.open('wb') as file:
		pickle.dump((dataframe.to_dict(as_series=False), dataframe.schema), file)


def gatherObjects(values: polars.Series, indices: polars.Series) -> polars.Series:
	return polars.Series(values.name, map(polars.Series.to_list, map(values.gather, indices)), dtype=polars.Object)
