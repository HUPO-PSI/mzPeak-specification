# Point Layout

The **point layout** stores data arrays as-is in parallel columns alongside a
repeated index column. The top-level schema node is named `point` and is a group
with an arbitrary number of columns. The entity index column **MUST** be the
first column under `point`. All rows with the same index **MUST** be contiguous.

<figure class="mzp-figure" markdown>
<img src="../../assets/img/point_layout.svg" alt="Point-layout schema: a single top-level point group holding a repeated spectrum_index column alongside parallel mz and intensity columns, with one table row per data point." height="520"/>
</figure>

<table class="point-table" markdown="0">
  <thead>
    <tr><th colspan="3">point</th></tr>
    <tr><th>spectrum_index</th><th>mz</th><th>intensity</th></tr>
  </thead>
  <tbody>
    <tr><td>0</td><td>213.2</td><td>1002</td></tr>
    <tr><td>0</td><td>506.9</td><td>500</td></tr>
    <tr><td>0</td><td>758</td><td>405</td></tr>
    <tr><td>…</td><td>…</td><td>…</td></tr>
    <tr><td>2</td><td>329.1</td><td>50</td></tr>
    <tr><td>2</td><td>516.5</td><td>5002</td></tr>
    <tr><td>2</td><td>783.8</td><td>302</td></tr>
  </tbody>
</table>

This layout is simple, but carries several advantages:

- **Predicate filtering.** Scalar columns are easily filtered along the
  page-level range index, which makes multi-dimensional queries easy to write
  and optimise.
- **Transparent compression.** Arrays are encoded and compressed by Parquet, so
  the data is still stored compactly.

The trade-off: data **MUST** be stored as-is to keep the page index meaningful,
so no additional obscuring transformations (delta encoding, Numpress, etc.) may
be used. The [zero-run stripping](signal-data.md#zero-run-stripping) and
[null-marking](signal-data.md#null-marking) methods remain available, because
they only remove non-meaningful points from the array rather than transforming
the values that remain.

## Parallel time index

In addition to the `<entity_type>_index` column, the writer *MAY* include a parallel
`<entity_type>_time` column which **MUST** store the [scan start time](http://purl.obolibrary.org/obo/MS_1000016)
associated with that entity, stored as a scalar float64. This applies naturally to mass spectra, but is redundant
for chromatograms or traces. This column is not part of the array index.


## Reading a single entry from the point layout

To read a single entry (spectrum, chromatogram, …) stored in point layout:

0. Identify which columns are annotated in the [array index](signal-data.md#the-array-index).
   The `<entity_type>_index` column **MUST** be the first column in the table, so it always has index 0.
1. Find the row group containing the entry's index value via the row-group
   metadata. Optionally, if the page index is available, find the row ranges of
   the pages that contain that index.
2. Read the selected row group (or page row range) and filter to rows whose
   `<entity_type>_index` equals the entry's index.
3. Read all rows for all columns where the entry's index equals the entry's index.
   Apply any transforms to finish decoding the data. They may require first reading
   from the entity's metadata table.
4. If the entry has additional [auxiliary arrays](auxiliary-arrays.md), read and
   decode them from the metadata table.

