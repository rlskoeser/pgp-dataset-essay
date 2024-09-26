# Modeling and structuring fragmented information

The first phase towards implementing PGPv4 involved designing a data model to accurately capture the complex structure of the information and physical support of geniza documents. Developing the data model was a collaborative effort of co-creation as technologists on the research team learned the basics of geniza studies and historians and researchers on the team learned enough about data modeling to read and engage with data model diagrams. As part of this data modeling effort, we were forced to engage with long-standing debates in the geniza field as to whether the fragment or the document is the appropriate unit of analysis.

Using a relational data mode allows us to model the complex relationship between two key entities, documents and fragments. We define a document as a unified written text, such as a letter, a petition, or a contract. In common usage, when we refer to a fragment we mean the physical material, whether paper, parchment or papyrus, on which that text is written.. A fragment could contain more than one document, if the same piece of paper was reused for a different documentary purpose. A fragment could also contain less than one document, if the original document spanned several pieces of paper, or if the original paper was torn into pieces. However, strictly speaking, PGP fragment records correspond to a “shelfmark”, which is the identifier used by the owning institution to reference the material object. PGP is beholden to and benefits from major cataloging efforts by the institutions that have preserved and curated these fragmentary texts. For a small set of cases, a PGP fragment may actually reference a specific portion within a shelfmark, when smaller, typically unrelated, fragments have been cataloged together; we call these “multifragments.”

The complexity of the relationship between documents and fragments is due to the variety of possible combinations for how documents and fragments may overlap.

## Document Types

```js
const documents = FileAttachment("/data/documents.csv").csv();
```

```js
const count_by_type = d3
  .rollups(
    documents,
    (d) => d.length,
    (d) => d.type,
  )
  .map((x) => new Object({ type: x[0], count: x[1] }));
const most_common = count_by_type[0];
const second_most_common = count_by_type[1];
const total_unknown = count_by_type
  .filter((x) => x.type == "Unknown")
  .map((x) => x.total);
// display for debugging
//display(count_by_type);

// TODO: card with table of types and totals
```

PGP uses an intentionally simplified typology devised by Rustow and Krakowski to facilitate data entry. There are currently ${ documents.length.toLocaleString() } total documents in PGP. The most common types are ${ most_common.type } (${ most_common.count.toLocaleString() }) and ${ second_most_common.type } (${ second_most_common.count.toLocaleString() }).

```js
const plotTypes = Plot.plot({
  marginLeft: 200,
  x: { label: "Number of documents", grid: true },
  y: { grid: true, label: "Document Type" },
  marks: [
    Plot.barX(count_by_type, {
      y: "type",
      x: "count",
      fill: "var(--theme-foreground-focus)",
      width: width,
    }),
  ],
});
```

### Totals by Document Type

<div class="grid grid-cols-3">
  <div class="card">
    ${Inputs.table(count_by_type, {select:false})}
  </div>
  <div class="card grid-colspan-2">
  ${ plotTypes }
  </div>
</div>

The current dataset includes ${ total_unknown.toLocaleString() } documents with no type, which may mean they have not been fully cataloged and described, or in some rare cases that the document doesn't clearly fall into existing categories.

```js
// [check for overlap of unknown and stub records?].
```

## Languages and Scripts

As previously mentioned, geniza materials are written in a variety of medieval languages and scripts, including Judaeo-Arabic (Arabic written in Hebrew characters) and Ladino (or Judaeo-Spanish, also written in Hebrew characters).

To simplify the data structure, languages and script are modeled as a single entity that combines language and script information, so that both language and script are explicitly documented [todo: check how this is reflected in the data exports], but also so that the system could offer convenient labels where terms such as Hebrew, Arabic, or Judaeo-Arabic clearly and concisely convey both language and script (respectively written in Hebrew, Arabic, and Hebrew scripts). We also include explicit unknown languages and scripts, since geniza materials often include content that is difficult to identify, which may be of particular interest to scholars interested in tackling a challenge.
