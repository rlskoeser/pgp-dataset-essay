import * as Plot from "npm:@observablehq/plot";
import { html } from "npm:htl";
import { Generators } from "observablehq:stdlib";

/**
 * Creates an UpSet plot by combining Observable Plot bar and link charts.
 *
 * @param {Array} data - An array of objects representing group memberships.
 *                       Each object should have:
 *                       - A 'group' property with comma-delimited string of set names
 *                         (e.g. "set 1, set 2, set 3")
 *                       - A 'total' property with the count for that group
 * @param {Object} options - Optional configuration settings; use to specify `width`
 * @returns {HTMLElement} The UpSet plot visualization as an HTML element
 */
export function upSetPlot(data, options = {}) {
  const {
    // NOTE: consider adding logic to control sorting by total or by alpha
    // sortBy = "count",
    width = 800,
  } = options;

  const fullWidth = Math.max(width, 500); // don't allow to go too narrow
  const lowerBarChartWidth = 240;

  // to ensure grouped set axes match across plots, store the domain
  const group_domain = data.map((x) => x.group);

  // the top portion of an upset plot is a vertical bar chart
  // showing the size of each group of sets
  const groupBarChart = Plot.plot({
    x: {
      axis: null,
      //padding: 0.2,
      //   round: false
      domain: group_domain,
    },
    y: {
      tickPadding: 2,
      line: true,
    },
    // width: fullWidth,
    // marginLeft: lowerBarChartWidth,
    width: fullWidth - lowerBarChartWidth,
    // marginLeft: 60,
    // x: {label: "Frequency"},
    // y: {label: null},
    // color: {legend: true},
    marks: [
      Plot.barY(data, { x: "group", y: "total" }),
      Plot.text(data, { x: "group", y: "total", text: "total", dy: -7 }),
      Plot.tip(data, Plot.pointerX({ x: "group", y: "total" })),
    ],
  });

  // the left lower portion of an upset plot is a horizontal bar chart
  // showing the size of each individual set

  // Generate a list of all unique sets and total counts from the data.
  // This creates an object with set names as keys and total as value
  const sets = data.reduce((accumulator, currentValue) => {
    currentValue.group.split(",").forEach((set) => {
      set = set.trim();
      if (accumulator[set] === undefined) {
        accumulator[set] = 0;
      }
      accumulator[set] += currentValue.total;
    });
    return accumulator;
  }, new Object());
  // restructure into named fields for plotting
  const set_totals = Object.entries(sets).map(([name, value]) => ({
    ["set"]: name,
    total: value,
  }));

  // adjust lower chart height slightly when displaying more sets
  const lowerChartHeight = Math.min(350, Math.max(200, set_totals.length * 30));

  const setBarChart = Plot.plot({
    width: lowerBarChartWidth,
    x: {
      axis: "top",
      line: true,
      reverse: true,
      label: null,
    },
    y: {
      axis: "right",
      tickSize: 0,
      label: null,
      // tickPadding: 7,
      insetTop: 2,
      round: false,
      padding: 0.1,
      align: 0,
    },
    height: lowerChartHeight,
    marginRight: 100,
    marks: [
      Plot.barX(set_totals, { y: "set", x: "total" }),
      Plot.text(set_totals, {
        y: "set",
        x: "total",
        text: "total",
        dx: -4,
        textAnchor: "end",
      }),
    ],
  });

  // the rightlower portion of an upset plot is a link plot
  // showing how the groups in the upper bar chart overlap
  // the sets in the left bar chart.
  // x-axis is the group name, y-axis is individual set

  const set_links = data.reduce((accumulator, currentValue) => {
    let group_name = currentValue.group;
    let group_sets = group_name.split(",").map((x) => x.trim());
    // when there is more than one group, create a link for each pair
    if (group_sets.length > 1) {
      group_sets.forEach((set, index, group) => {
        let next_index = index + 1;
        if (next_index < group.length) {
          accumulator.push({
            group: group_name,
            set1: set,
            set2: group[next_index],
          });
        }
      });
    } else {
      // when a group consists of a single set, link it to itself for display
      // TODO: could we always do this to simplify? (link last el to self)
      let set = group_sets[0];
      accumulator.push({
        group: group_name,
        set1: set,
        set2: set,
      });
    }
    return accumulator;
  }, new Array());

  const linkPlot = Plot.plot({
    x: {
      axis: null,
      domain: group_domain,
    },
    y: {
      axis: null,
      tickSize: 0,
    },
    width: fullWidth - lowerBarChartWidth,
    height: lowerChartHeight,
    marginTop: 30,
    marginBottom: 22,
    marks: [
      Plot.gridY({ strokeOpacity: 0.5 }),
      Plot.link(set_links, {
        x1: "group",
        x2: "group",
        y1: "set1",
        y2: "set2",
        marker: "circle",
        strokeWidth: 4,
      }),
    ],
  });

  const spacerChart = Plot.plot({ width: lowerBarChartWidth });

  // return as html, with a flex div to put lower charts side by side
  return html` <div style="display:flex">
    ${spacerChart}
    ${groupBarChart}
    </div>
    <div style="display:flex">${setBarChart} ${linkPlot}</div>
  </div>`;
}
