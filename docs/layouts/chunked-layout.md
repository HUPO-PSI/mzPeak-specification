# Chunked Layout

The **chunked layout** treats one array — which must be sorted — as the "main"
axis, cutting it into chunks of a fixed size along that coordinate space (for
example steps of 50 m/z) and taking the same segments from the parallel arrays.
The main axis chunks' start, end, and a repeated index are recorded as columns;
each array may then be stored as-is or with an opaque transform (delta encoding,
Numpress, …). The start/end interval permits granular random access along *both*
the main axis and the source index. The top-level schema node is named `chunk`,
and the entity index column **MUST** be its first column.

<div class="mzp-figure" markdown>
<img src="../../assets/img/chunked_layout.png" alt="Chunked-layout schema: a top-level chunk group holding spectrum_index, mz_chunk_start and mz_chunk_end bounds, an encoded mz_chunk_values list, a chunk_encoding column, and an intensity list, with one table row per chunk." height="520"/>
</div>

<table class="chunk-table" markdown="0">
  <thead>
    <tr><th colspan="6">chunk</th></tr>
    <tr>
      <th>spectrum_index</th><th>mz_chunk_start</th><th>mz_chunk_end</th>
      <th>mz_chunk_values</th><th>chunk_encoding</th><th>intensity</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>200</td><td>250</td><td>[0.0013, …, 0.0013]</td><td>MS:1003089</td><td>[…]</td></tr>
    <tr><td>1</td><td>250</td><td>300</td><td>[0.0014, …, 0.0014]</td><td>MS:1003089</td><td>[…]</td></tr>
    <tr><td>1</td><td>500</td><td>550</td><td>[0.0014, …, 0.0015]</td><td>MS:1003089</td><td>[…]</td></tr>
    <tr><td>…</td><td>…</td><td>…</td><td>…</td><td>…</td><td>…</td></tr>
    <tr><td>2</td><td>200</td><td>250</td><td>[0.0013, …, 0.0013]</td><td>MS:1003089</td><td>[…]</td></tr>
    <tr><td>2</td><td>350</td><td>400</td><td>[0.0014, …, 0.0014]</td><td>MS:1003089</td><td>[…]</td></tr>
    <tr><td>2</td><td>400</td><td>450</td><td>[0.0013, …, 0.0014]</td><td>MS:1003089</td><td>[…]</td></tr>
  </tbody>
</table>

This example uses delta encoding for the m/z chunk values, which is reconstructed
with very high precision for 64-bit floats. The m/z values inside
`mz_chunk_values` are not visible to the page index, but the `_chunk_start` and
`_chunk_end` columns are. The chunk values remain subject to Parquet encodings,
so they can be byte-shuffled for further compression.

## Column naming rules

1. **`<entity>_index`** (integer) — the index key for the entity this chunk
   belongs to.
2. **`<array_name>_chunk_start`** (float64) — the first coordinate value in the
   chunk, inclusive. Its array-index `buffer_format` **MUST** be `chunk_start`.
3. **`<array_name>_chunk_end`** (float64) — the last coordinate value in the
   chunk, inclusive. Its array-index `buffer_format` **MUST** be `chunk_end`.
4. **`<array_name>_chunk_values`** (list) — the encoded coordinates from
   `array_name` according to `chunk_encoding`. Its array-index `buffer_format`
   **MUST** be `chunk_values`.
5. **`chunk_encoding`** (CURIE) — how `<array_name>_chunk_values` were encoded;
   see [Chunk encodings](#chunk-encodings). Its array-index `buffer_format`
   **MUST** be `chunk_encoding`.

All other columns are expected to be `list` arrays whose names are simply their
`array_name` (with `buffer_format` `chunk_secondary`), or surrogate arrays with
`buffer_format` `chunk_transform`.

## Splitting data into chunks

A chunk table may be partitioned in any pattern, as long as the chunks are
non-overlapping and ascending. The chunking procedure must be `null`-aware — in
particular, aware of the `null` pairs that mark masked regions. The granularity
is configurable, trading random-access granularity against compression
efficiency.

??? example "Python — partitioning into chunks of width *k* with null pairs present"
    ```python
    import pyarrow as pa

    def null_chunk_every(data: pa.Array, width: float) -> list[tuple[int, int]]:
        """
        Partition a sorted numerical array into segments spanning `width` units.
        This operation is null-aware, so sparse arrays can be partitioned.
        Returns the (start, end) index of each chunk.
        """
        start = None
        n = len(data)
        i = 0
        # Find the first non-null position
        while i < n:
            v = data[i]
            if v.is_valid:
                start = v.as_py()
                break
            else:
                i += 1

        # If we never found a non-null position, just return a single chunk
        if start is None:
            return [(0, n)]

        chunks = []
        offset = 0
        threshold = start + width
        i = 0
        while i < n:
            v = data[i]
            if v.is_valid:
                v = v.as_py()
                if v > threshold:
                    if ((i + 1) < n) and (not data[i + 1].is_valid):
                        while ((i + 1) < n) and (not data[i + 1].is_valid):
                            i += 1
                    # Avoid a chunk of length 1, especially a null point; if so,
                    # relax the width requirement.
                    if i - offset > 1:
                        chunks.append((offset, i))
                        offset = i
                    while threshold < v:
                        threshold += width
            # Look ahead: this value is null, but the next is not.
            elif ((i + 1) < n) and (data[i + 1].is_valid):
                i += 1
                v = data[i].as_py()
                if v > threshold:
                    i -= 1
                    chunks.append((offset, i))
                    offset = i
                    while threshold < v:
                        threshold += width
            i += 1
        if offset != n:
            chunks.append((offset, n))
        return chunks
    ```

??? info "Multi-dimensional chunking postponed for the future"
    Currently, chunking is only permitted in one dimension, the added complexity of chunking in multiple dimensions was not deemed necessary *yet*. Current instruments do not produce large enough and dense enough ion mobility dimensions to rival the m/z dimension for compression difficulty.

    There may come a time when we have high enough density that it becomes worthwhile to support by adding additional `chunk_start`, `chunk_end`, chunk_encoding`, and `chunk_values` columns. If you believe you have a use case, let us know!

## Chunk encodings

### Basic encoding

> Chunk-encoding CV term: [`MS:1000576` — no compression](http://purl.obolibrary.org/obo/MS_1000576)

When storing centroids, or sparse data that are not similarly spaced but still wanting the chunked layout,
no special encoding of the chunk values is necessary. Values within each chunk are written as-is to the
chunk-values array. This does not improve compressibility, but it keeps a consistent schema for other
entries that *would* benefit from a different encoding.

!!! note
    The start point is *excluded* from the chunk-values array.

### Delta encoding

> Chunk-encoding CV term: [`MS:1003089` — truncation, delta prediction and zlib compression](http://purl.obolibrary.org/obo/MS_1003089)

When data lie on a locally (*almost*) uniform grid using 64-bit floats,
compression improves by computing a delta encoding of the coordinates.

!!! note
    The start point is *excluded* from the chunk-values array.

??? example "Python — null-aware delta encode/decode"
    ```python
    import pyarrow as pa

    def null_delta_encode(data: pa.Array) -> pa.Array:
        """
        Delta-encode an Arrow array containing nulls. Nulls are encoded as null
        values and treated as 0.0 for the purpose of computing the next delta.
        """
        acc = []
        it = iter(data)
        # The first entry is the point of reference but not part of the delta
        # sequence unless it is `null`.
        last = next(it)
        if not last.is_valid:
            acc.append(last)

        for item in it:
            if item.is_valid:
                val = item.as_py()
                if last.is_valid:
                    acc.append(pa.scalar(val - last.as_py()))
                else:                       # treat the last value as 0.0
                    acc.append(item)
                last = item
            else:
                acc.append(item)            # carry the null forward
                last = item
        return pa.array(acc)


    def null_delta_decode(data: pa.Array, start: pa.Scalar) -> pa.Array:
        """Decode an Arrow array that was delta-encoded *with* nulls."""
        acc = []
        if not data[0].is_valid:
            if not data[1].is_valid:
                # started at a non-null value immediately followed by a null pair
                acc.append(start)
            start = pa.scalar(None, data.type)
        else:
            acc.append(start.as_py())
        last = start
        for item in data:
            if item.is_valid:
                val = item.as_py()
                if last.is_valid:
                    last = pa.scalar(val + last.as_py())
                    acc.append(last)
                else:                       # last value assumed zero
                    acc.append(item)
                    last = item
            else:
                acc.append(item)
                last = item
        return pa.array(acc)
    ```

### Numpress linear encoding

> Chunk-encoding CV term: [`MS:1002312` — MS-Numpress linear prediction compression](http://purl.obolibrary.org/obo/MS_1002312)

This uses the MS-Numpress linear-prediction method
([10.1074/mcp.O114.037879](https://www.mcponline.org/article/S1535-9476(20)33083-8/fulltext))
to compress the chunk values as raw bytes. Numpress produces a buffer of an
8-byte fixed point, a 4-byte value 0, a 4-byte value 1, and then 2-byte residuals
for all subsequent values. The array is therefore, by definition, not alignable
to a 4- or 8-byte type. It also has no concept of nullity, which makes it
**incompatible with [null marking](signal-data.md#null-marking)**.

To store Numpress-linear-encoded arrays, an extra column
`<array_name>_numpress_linear_bytes` is added alongside the
`<array_name>_chunk_values` column. It is a list of byte arrays
(`large_list<u8>` in Arrow parlance — **not** `large_binary`; see the
[discussion of string-type "optimisation"](https://arrow.apache.org/docs/format/Intro.html#variable-length-binary-and-string)).
Its array-index entry **MUST** have `buffer_format` `chunk_transform` and the
same array type, array name, data type, unit, and data-processing ID as the
`_chunk_values` column. The `transform` field **MUST** be `MS:1002312`.

!!! note
    The start point is *included* in the chunk-values array — it is a specific
    component of the Numpress-encoded bytes.

### Grid encoding

> Chunk-encoding CV term: [`MS:1003826` — coordinate grid encoding](http://purl.obolibrary.org/obo/MS_1003826)

This uses a pluggable coordinate model that maps *real* value to and from unsigned integer coordinates using
a pair of equations and a set of grid parameters. To store grid-encoded arrays for the chunk dimension, an
extra column group `<array_name>_grid` is added. Like in the [Numpress linear encoding](#numpress-linear-encoding) case, the `<array_name>_chunk_values` column is populated with an empty list when the chunked dimension is grid-encoded. Other arrays may be grid encoded using the same methods described here, such as an IM-MS spectrum's ion mobility array, if desirable. Only one distinction is made in the encoding of the grid indices, seen later in this section. When a grid model is used, it is encoded as a group/struct with the schema:

```
optional group <array_name>_grid {
    required binary grid_type (String);
    required group parameters (List) {
        repeated group list {
            required double item;
        }
    }
    required group indices (List) {
        repeated group list {
            required int32 item (Int(bitWidth=32, isSigned=false));
        }
    }
}
```

The `grid_type` column in the group is a string that contains the CV term CURIE for the model type deriving
from `MS:1003822|grid coordinate interpolation`, telling the reader how to use the other columns.  Currently,
there are two "open" grid model types, [`MS:1003824|linear grid interpolation`](http://purl.obolibrary.org/obo/MS_1003824)
which uses a scaled simple least squares model and [`MS:1003825|square root grid interpolation`](http://purl.obolibrary.org/obo/MS_1003825)
which does the same, but using the square root of real coordinates. The latter is a better theoretical fit for
time-of-flight mass analyzers, though it often lacks essential parameters from the hardware to be as accurate as
vendor proprietary models. There are provisions for adding vendor models or approximations of them to the
vocabulary.

The `parameters` column is a list of 64-bit floats that will be used to parameterize the grid model. The
order they are written is given by `grid_type`'s definition. The number of parameters *MAY* vary within rows of the same `grid_type` if the model permits it, and is expected to vary between different `grid_type` models in general. These parameters are used in index/coordinate conversion.

The `indices` column is a list of 32-bit (unsigned) integers that are mapped to the real 64-bit float coordinates
being encoded. These are produced for writing by using the grid model to convert real-valued coordinates *to* grid
indices. When reading, the grid model is used to convert *from* indices back to their equivalent real-valued
coordinates. It is possible that for some proprietary grids, only the *from* index conversion is publicly available, or an approximation thereof. Whether the grid encodes the chunk dimension or not, the starting grid index **MUST** be included in the `indices` column's array. The chunk dimension's `indices` column **MUST** be delta-encoded, this is done to improve compressibility of a sorted array of indices.

It must be noted that *unless* using a vendor-defined encoding, this is likely to be a lossy transformation.
The user **SHOULD** be able to set an error threshold for using the grid encodings. A model that would have errors exceeding the given threshold **SHOULD** fall back to use a different encoding. The linear grid can be
an order of magnitude less accurate than `MS-Numpress linear prediction` on profile data, but 30% smaller when
both are Zstandard compressed. On time-of-flight mass analyzers, the square root grid is marginally less accurate but
produces better compression, 50% smaller than `MS-Numpress linear prediction` on the same profile data. This is because its
grid indices are more consistently spaced relative to the real data. Additionally, on quantities with compressed dynamic
ranges like ion mobility, the linear grid is equal to or more accurate than `MS-Numpress linear prediction` while still being smaller.

#### Parquet column encoding for grid encoding columns

- The `grid_type` column should be encoded using `RLE_DICTIONARY`, the default behavior
- The `parameters` column's bit-level will vary from model to model, `RLE_DICTIONARY` is usually best still.
- The `indices` column, benefits from `BYTE_STREAM_SPLIT` most of the time, at least for the sorted dimension. However, when one index in particular dominates the result, such as when delta encoding profile data with consistent spacing or repeated values, `RLE_DICTIONARY` may still outperform it be a large margin.

TODO: Collect a larger corpus of data to plot this accuracy claim.

??? example "A worked example"

    The equations for [`MS:1003824|linear grid interpolation`](http://purl.obolibrary.org/obo/MS_1003824) are given
    with coefficients intercept $a$, slope $b$ and scale $s$:

    *from index*: $f(i) = (a + b × i)×(1/s)$

    *to index*: $g(v) = (v × s - a)×(1/b)$

    or in Python

    ```python
    class LinearGrid:
        intercept: float
        slope: float
        scale: float

        def from_index(
            self, index: int | npt.NDArray[np.uint32]
        ) -> float | npt.NDArray[np.float64]:
            value = (self.intercept + index * self.slope) / self.scale
            if isinstance(value, np.ndarray):
                return value.astype(np.float64)
            return value

        def to_index(
            self, value: float | npt.NDArray[np.float64]
        ) -> int | npt.NDArray[np.uint32]:
            value = (value * self.scale - self.intercept) / self.slope
            if isinstance(value, np.ndarray):
                return (value + 0.5).astype(np.uint32)
            return int(value + 0.5)
    ```


    Given $a=95.0$, $b=3.75e-7$ and $s=1.0$ we can compute the index `2190583200` maps to the coordinate `916.4687` using
    the *from index* equation, $(95.0 + 2190583200×3.75e-7)×(1/1)$. Conversely, the *to index* equation, $(916.4687×1 - 95.0)/3.75e-7$.

    The model [`MS:1003824|linear grid interpolation`](http://purl.obolibrary.org/obo/MS_1003824) can be learned from the raw
    data directly using simple linear regression:

    ```python
    def fit(values: npt.NDArray[np.float64], low: float, high: float, scale: float = 1.0):
        # The maximum value a 32-bit unsigned integer can take on
        slots = 4294967295
        # The spacing between points on a grid from *low* to *high* with the *scale* multiplier
        # is given by the total distance between those two scaled points divided by the total
        # number of positions along a grid storable in a 32-bit integer.
        step_size = (high * scale - low * scale) / slots

        values = values * scale
        # The initial grid indices for these observed values
        indices = ((values - (low * scale)) / step_size).astype(np.uint32)

        x_mean = indices.mean()
        y_mean = values.mean()
        # Regress values on the initial indices
        x_sub_mean = indices - x_mean
        y_sub_mean = values - y_mean

        slope = x_sub_mean.dot(y_sub_mean) / x_sub_mean.dot(x_sub_mean)
        intercept = y_mean - slope * x_mean
        return np.array([intercept, slope, scale])
    ```



## Opaque array transforms for *other* dimensions

Sometimes we prefer to store data in arrays other than the main axis lossily in non-uniform, unaligned, or otherwise
non-standard types that have no physical representation in Parquet. MS-Numpress's
short logged float (SLOF) and positive-integer encodings are good examples. While
Numpress-linear handles the coordinate dimension, opaque transforms can also
encode the *secondary* arrays in chunks. These columns are recorded in the array
index with `buffer_format` `chunk_transform`, and the `transform` field is the
CURIE for the relevant method — for example
[`MS:1002314`](http://purl.obolibrary.org/obo/MS_1002314) for MS-Numpress SLOF.
The column's physical type **MUST** be a list of byte arrays, though the type in
the array index **MUST** be the *decoded* array's real type. Column names
**SHOULD** be of the form `<array_name>_<transform_name>_bytes`, e.g.
`intensity_numpress_slof_bytes`.

??? question "Transform name or accession code?"
    We use a human readable name here, but it is not obviously stable. We could embed a CURIE in the column name like [MS_1002314](http://purl.obolibrary.org/obo/MS_1002314) instead for `intensity_MS_1002314_bytes`, but this is unnecessarily cryptic when the source of truth is the [array index](./signal-data.md#the-array-index)


## Reading a single entry from the chunked encoding

To read a single entry (spectrum, chromatogram, …) stored in chunks:

0. Identify which columns are annotated as `chunk_start`, `chunk_end`,
   `chunk_encoding`, and `chunk_values` in the
   [array index](signal-data.md#the-array-index). The `<entity_type>_index`
   column **MUST** be the first column in the table, so it always has index 0.
1. Find the row group containing the entry's index value via the row-group
   metadata. Optionally, if the page index is available, find the row ranges of
   the pages that contain that index.
2. Read the selected row group (or page row range) and filter to rows whose
   `<entity_type>_index` equals the entry's index.
3. Optionally, sort the rows by their `chunk_start` value — usually ascending for
   the quantity being measured.
4. Process each selected row, decoding its `chunk_values` according to
   `chunk_encoding` and any `transform` in the array index. Unpack the
   `chunk_secondary` columns and apply any transforms, accumulating each column's
   arrays across rows. Some transforms require additional information from the
   entity's metadata table.
5. If the entry has additional [auxiliary arrays](auxiliary-arrays.md), read and
   decode them from the metadata table.
