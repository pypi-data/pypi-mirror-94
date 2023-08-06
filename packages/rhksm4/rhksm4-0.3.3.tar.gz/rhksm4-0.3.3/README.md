# rhk_sm4

A python package to read .sm4 files from RHK Technology.

Introduction
============
This pure Python package read .sm4 files from RHK Technology.

Installation
============

```
    pip install rhksm4
```

Usage
=====

The recommended import

```
    import rhksm4
```
See the docstring help for more detailed information.

Loading
-------

To load an .sm4 file

```
    f = rhksm4.load('path/to/file.sm4)
```
The instance f is a container of pages, which can be accessed by key,
and each page has its own attributes:

```
    p0 = f[0]
    p0.data
    p0.attrs
    p0.name
```

xarray dataset
--------------

The .sm4 file can be conveniently loaded as an xarray Dataset
(provided that xarray package is installed):

```
    ds = rhksm4.to_dataset('path/to/file.sm4')
    ds.IDxxxxx
```

NeXuS export
------------

The .sm4 file can be converted and saved to NeXuS file with
(nxarray package is required):

```
    rhksm4.to_nexus('path/to/file.sm4')
```
