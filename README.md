# Table Data Management Project

This project provides a Python class `Table` designed to handle data tables stored in CSV, Pickle, and TXT formats. It supports various operations like loading, saving, printing, and manipulating the data. You can perform column-wise and row-wise calculations, set and get values, filter rows, and much more.

## Features

- **Load Data**: Supports loading data from `.csv` and `.pkl` files.
- **Save Data**: Can save data to `.csv`, `.pkl`, and `.txt` formats with options to split files into multiple parts based on row count.
- **Print Data**: Print tables in a user-friendly format with labels and values.
- **Column Operations**: Automatically detects data types and provides methods for operations like addition, subtraction, multiplication, and division.
- **Row Operations**: Retrieve specific rows or filter by row values.
- **Table Manipulation**: Combine and split tables, and set or get column values.
- **Column Type Management**: Dynamically detect or set column data types.
  

### Creating Tables

To create a `Table` object, initialize it with a filename:

```python
table = Table("my_table")
```

### Loading Tables
Loading a single file
```python
table.load_table("data.csv")
```

Loading multiple files
```python
table.load_table("data.csv", "data.pkl")
```

### Saving Tables
Save to CSV
```python
table.save_table(preferred_format='.csv')
```

Save to Pickle
```python
table.save_table(preferred_format='.pkl')
```

Save to TXT
```python
table.save_table(preferred_format='.pkl')
```

If you want to split large tables into smaller files based on the row count, use the `max_rows` argument

```python
table.save_table(write_down_name="output", max_rows=10)
```

### Table operations

Retrieve rows from `a` to `b`

```python
table.get_rows_by_number(a, b)
```

Retrieve exact rows by indexes (for instance `a`, `b`, `c`)
```python
table.get_rows_by_index(a, b, c)
```

If you want to created a new table with extracted rows, use `copy_table` argument

```python
table.get_rows_by_number(a, b, copy_table=True)
```
```python
table.get_rows_by_index(a, b, c, copy_table=True)
```

Get column types. Argument `by number` defines the form of data. If True, returns the data types by column index. If False, returns the data types by column label
```python
table.get_column_types(by_number=False)
```

Set column types. The column types can be set either by column index or by column label.Argument `by number` defines the form of data. Possible types for setting: `int`, `float`, `bool`, `str`
```python
table.set_column_types({'Age': 'int'}, by_number=False)
```


