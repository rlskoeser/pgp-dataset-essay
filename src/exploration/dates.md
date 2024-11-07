# PGP document dates

```js
const documents = FileAttachment("/data/documents.csv").csv();
```

How many documents have date information?

```js
const date_fields =['doc_date_standard', 'doc_date_original', 'doc_date_calendar', 'inferred_date_display', 'inferred_date_standard', 'inferred_date_rationale', 'inferred_date_notes'];

// count how many records have content for each field
let count_by_info = date_fields.map((f) => {
  // count based on field value not falsy (no empty string, no null, no zeroes)
	return {
    'field': f, 
    'total': documents.filter((x) => x[f]).length
  };
});
// uncomment for debug/check
//display(count_by_info);
```

```js
// filter to get counts for dcouments with any date in standard format
let any_dated_documents = documents.filter((x) => 
       (x.doc_date_standard || x.inferred_date_standard));

let date_on_doc = documents.filter((x) => x.doc_date_standard);
let inferred_date_docs = documents.filter((x) => x.inferred_date_standard);
```
The current dataset includes ${ any_dated_documents.length.toLocaleString() } dated documents, of which ${ date_on_doc.length.toLocaleString() } have a date on the document itself and ${ inferred_date_docs.length.toLocaleString() } documents have inferred dates.


```js
display(Plot.plot({
  marginLeft: 200,
  title: "Documents with date information (count)",
  x: { label: "Number of documents", grid: true },
  y: { grid: true, label: "Date field" },
  marks: [
    Plot.barX(count_by_info, {
      y: "field",
      x: "total",
      fill: "var(--theme-foreground-focus)",
      width: width,
    }),
  ],
}));
```

What about as a percent of all documents?

```js
let total_documents = documents.length;
let percent_info = count_by_info.map((x) => {
	x.percent = (x.total / total_documents) * 100;
	return x;
});

display(Plot.plot({
  marginLeft: 200,
  title: "Documents with date information (% of all documents)",
  x: { label: "Number of documents", grid: true, domain: [0, 100]},
  y: { grid: true, label: "Date field" },

  marks: [
    Plot.barX(percent_info, {
      y: "field",
      x: "percent",
      fill: "var(--theme-foreground-focus)",
      width: width,
    }),
  ],
}));
```

* * * 

Documents over time, based on standardized date (date on document).

```js
// filter to documents with standardized date and set start/end/midpoint for graphing
let dated_documents = documents.filter((x) => x.doc_date_standard != "" & x.doc_date_standard != null).map((x) => {
	let date_parts = x.doc_date_standard.split("/");
	x.year_start = Number(date_parts[0].split("-")[0]);
	x.year_end = Number(date_parts[date_parts.length - 1].split("-")[0]);
	x.year_midpoint = x.year_start + (x.year_end - x.year_start) / 2.0;
	return x;
});
```

```js
display(Plot.plot({
  color: {legend: true},
  // marginLeft: 200,
  title: "Documents by date and calendar",
   x: { label: "Year", tickFormat: "r" },
   y: { grid: true, label: "Number of documents" },
  marks: [
 	Plot.rectY(dated_documents, Plot.binX({y: "count"}, {x: "year_midpoint", fill: "doc_date_calendar"})),
  ]
}));
```
