# Github Globe

This is a little visualization of Github users throughout the world.
Check out an interactive version at [http://aasen.in/github_globe](http://aasen.in/github_globe)

![github users plotted on a globe](http://i.imgur.com/wHeJ9wG.png)

## Creating the Visualization

All data is provided by [GitHub Archive](http://www.githubarchive.org/)
and fetched via [Google BigQuery](https://developers.google.com/bigquery/).

Locations are provided by approximately 1 million of the 4 million GitHub users.
They are written in an informal syntax with varying specificity.
For example, `Seattle`, `Seattle, WA` and `United States` are all valid.

The 1,000 most common locations are passed through the [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding/)
and transformed into geographical coordinates.

Data is then grouped by coordinates, so `San Francisco`, `San Francisco, CA`, and `San Fran` are combined.

Finally, data is plotted on the [WebGL Globe](http://code.google.com/p/webgl-globe/).

## Anatomy of the Repo

All queries are stored in `master/fetch`.

Code to transform the data is in `master/transform`.

The visualization and WebGL globe are stored in the `gh-pages` branch.

## Problems

One problem is that locations vary in specificity.
Many people report only their country and leave out states, cities, and other identifiers.

To solve this, I could calculate the specificity of an address and leave out any broad locations
like `China`, `America`, and `California`.
However, since this would skew the data I decided not to.
If you disagree, [fork it](http://github.com/aaasen/github_globe/fork)!
