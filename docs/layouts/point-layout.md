# Point Layout

The **point layout** stores data arrays as-is in parallel columns alongside a
repeated index column. The top-level schema node is named `point` and is a group
with an arbitrary number of columns. The entity index column **MUST** be the
first column under `point`.

<div class="mzp-figure" markdown>
<img src="../../assets/img/point_layout.png" alt="Point-layout schema: a single top-level point group holding a repeated spectrum_index column alongside parallel mz and intensity columns, with one table row per data point." height="520"/>
</div>

<table class="point-table" markdown="0">
  <thead>
    <tr><th colspan="3">point</th></tr>
    <tr><th>spectrum_index</th><th>mz</th><th>intensity</th></tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>213.2</td><td>1002</td></tr>
    <tr><td>1</td><td>506.9</td><td>500</td></tr>
    <tr><td>1</td><td>758</td><td>405</td></tr>
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
