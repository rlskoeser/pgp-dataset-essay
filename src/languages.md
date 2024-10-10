# Languages in PGP documents

```js
const documents = FileAttachment("/data/documents.csv").csv();
```

```js
const mincountInput = Inputs.range(
  [10, 2000],
  // d3.extent(count_by_langset, (d) => d.total),
  { step: 1, label: "Minimum", value: 225 },
);
const mincount = Generators.input(mincountInput);
```

```js
// TODO: toggle to control whether secondary languages are included
// languages_secondary
```

width = ${width}

<div class="grid grid-cols-1">
<div>
<h2>Language combinations</h2>

Displaying language combinations that occur at least ${ mincount.toLocaleString() } times.

${mincountInput}

```js
import { upSetPlot } from "./components/upset.js";

const lang_documents = documents.filter((d) => d.languages_primary != "");

const count_by_langset = d3
  .rollups(
    lang_documents,
    (d) => d.length,
    (d) => d.languages_primary,
  )
  .map((x) => new Object({ languages: x[0] || "NA", total: x[1] }))
  .sort((a, b) => a.total - b.total);

// total in combinations; sort highest count first
const plot_langs = count_by_langset
  .filter((x) => x.total >= mincount)
  .sort((a, b) => b.total - a.total);

// rename variable so we pass in group and total
const groupTotals = plot_langs.map((x) => ({
  group: x.languages,
  total: x.total,
}));

display(upSetPlot(groupTotals, { width: width }));

//${resize((width) => Plot.barX([9, 4, 8, 1, 11, 3, 4, 2, 7, 5]).plot({width}))}
```

## All language combinations

```js
// display(Inputs.table(count_by_langset)); // .sort((a, b) => b.total - a.total)));
display(Inputs.table(count_by_langset)); //.sort((a, b) => a.languages < b.languages)));
```

---

<div class="note" label="About the UpSet Plot">

An UpSet plot shows data in more than three overlapping sets. The vertical bar chart in the upper portion of the chart shows the sizes of the groups, the horizontal bar chart at left shows the sizes of the individual sets, and the link chart or matrix shows how the groups combine individual sets.

This UpSet plot is implemented with Observable Plot and is inspired by an [earlier implementation by Torsten Sprenger](https://observablehq.com/@spren9er/upset-plots-with-observable-plot).

</div>
