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

<div class="grid grid-cols-1">
<div>
<h2>Language combinations</h2>

```js
// toggle to control whether secondary languages are included
const showLanguages = view(
  Inputs.select(["languages_primary", "languages_secondary"], {
    value: ["languages_primary"],
    label: "Include languages:",
    multiple: true,
  }),
);
```

${mincountInput}

Displaying language combinations from **${ showLanguages.join(", ") }** that occur at least **${ mincount.toLocaleString() } times**.
(${ lang_documents.length.toLocaleString() } documents)

```js
import { upSetPlot } from "/components/upset.js";
const lang_documents = documents.filter((d) => {
  // secondary lang implies primary; if it is included, filter on that field being not empty
  if (showLanguages.includes("languages_secondary")) {
    return d.languages_secondary != "";
  }
  // otherwise filter on primary language field
  return d.languages_primary != "";
});
const count_by_langset = d3
  .rollups(
    lang_documents,
    (d) => d.length,
    (d) => {
      let documentLangs = [];
      for (let showLang of showLanguages) {
        if (d[showLang]) {
          let languages = d[showLang]
            .split(",")
            .map((x) => x.trim())
            .filter((x) => x != "");
          documentLangs.push(...languages);
        }
      }
      return documentLangs.join(",");
    },
  )
  .map((x) => new Object({ languages: x[0] || "", total: x[1] }))
  .sort((a, b) => a.total - b.total);

// total in combinations; sort highest count first
const langGroupCount = count_by_langset
  .filter((x) => x.total >= mincount)
  .sort((a, b) => b.total - a.total);

// rename variable so we pass in group and total
const groupTotals = langGroupCount.map((x) => ({
  group: x.languages,
  total: x.total,
}));

display(upSetPlot(groupTotals, { width: width }));
```

## All combinations

This table shows all language combinations from **${ showLanguages.join(", ") }**.
Click the headings to change how the table is sorted.

```js
display(
  Inputs.table(count_by_langset, {
    select: false,
    sort: "languages",
    header: {
      languages: "Languages",
      total: "# of documents",
    },
  }),
);
```

---

<div class="note" label="About the UpSet Plot">

An UpSet plot shows data in more than three overlapping sets. The vertical bar chart in the upper portion of the chart shows the sizes of the groups, the horizontal bar chart at left shows the sizes of the individual sets, and the link chart or matrix shows how the groups combine individual sets.

This UpSet plot is implemented with Observable Plot and is inspired by an [implementation by Torsten Sprenger](https://observablehq.com/@spren9er/upset-plots-with-observable-plot).

</div>
