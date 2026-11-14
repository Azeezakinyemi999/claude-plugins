# Sources and evidence

This file is **identical in both skills**. Change both copies together.

## Three access paths

At the top of every report, state which paths **actually ran**, for
example: *"Research paths: public research ran (web search, 7 sources);
structured access not configured; direct evidence from 2 supplied files."*
Never imply a path ran when it didn't.

**Your own background knowledge is not a research path and not a
source.** If web tools are unavailable or blocked, write *"public research
did not run (no web tools)"*. Background knowledge may shape which
questions to ask and which datasets to name, but never the numbers in a
memo, an evidence log or a calculation, even with a URL added "for
verification".

### 1. Public research

Use this when web tools are available in the session (web search, web
fetch). Choose sources from the market definition, the geography and the
question. There is no fixed list.

- **Official statistics:** for example [Census data](https://data.census.gov/),
  [FRED](https://fred.stlouisfed.org/), national statistics offices, and
  sector regulators.
- **Public filings:** for example [SEC EDGAR](https://www.sec.gov/edgar/search/),
  for competitors' revenue, segments and risk factors.
- **Public competitor offers:** pricing pages, terms and feature lists.
  Record the date viewed.
- **Sector and local sources:** trade associations, government program
  data, local registries and published surveys.

Rules:

- Search with generic terms. Never put confidential supplied material in a
  query.
- If a source can't be reached, log it as **unavailable** and say how to
  verify the claim.
- Public indicators support context and size. Evidence that buyers will
  pay for **this offer** must come from the business or its customers.

### 2. Structured access, when configured

Use approved, read-only API or MCP access only if it **already exists** in
the session (the tools are listed, or `claude mcp list` shows them). A run
never adds credentials, connectors, paid feeds or account changes. The
skills must work with public research and supplied files alone.

For a dataset queried repeatedly, document it once:

| Dataset | Access method | Credentials or permission | Example filters | Fallback |
| --- | --- | --- | --- | --- |
| <name> | <MCP server and tool, or API endpoint> | <who grants it, read-only?> | <geography, period, segment> | <public source or supplied file> |

**Setup note (for the team, outside any run).** Add an MCP server with
`claude mcp add` ([docs](https://code.claude.com/docs/en/mcp)):

```bash
claude mcp add --transport http <name> <url>
```

```bash
claude mcp add --transport stdio <name> -- <command> [args...]
```

- `--scope project` writes `.mcp.json` so the team shares the server. Keep
  tokens out of that file: use `${VAR}` references, or `local` scope.
- Prefer read-only credentials, and connect only servers you trust.
- Check what is connected with `claude mcp list`, or `/mcp` inside a session.

### 3. Direct business and customer evidence

Use approved interviews, observed workflows, purchases, transactions,
actual usage, support records and delivery costs, supplied by the team.

- **Never invent** an interview, a run, a purchase or a result.
- Don't send confidential files or their contents to third parties.
- When desk research can't answer the question, recommend a field test as a
  test card.

## Evidence classes

Label every material claim with one class:

| Class | Meaning |
| --- | --- |
| supplied fact | Stated in the team's materials or by the user |
| published figure | From a public source, cited |
| observed behavior | Something people actually did, recorded (purchases, usage, an observed workflow) |
| estimate | Calculated from other inputs; calculation shown, a range where uncertain |
| untested assumption | Believed, but no evidence yet |

## Evidence strength

Rate it qualitatively, as **Strong / Moderate / Weak / None**, and always
give the reason. Don't use numeric scores. The guide follows Strategyzer's
[evidence strength](https://www.strategyzer.com/library/how-strong-is-your-innovation-evidence)
and is ordered from stronger to weaker:

- what people did, over what they say they'd do;
- a costly commitment (payment, deposit, signed letter of intent, time
  invested), over a click, a like or stated interest;
- the target segment, this offer and recent evidence, over the general market
  or old evidence;
- an independent sample of meaningful size, over friends, family or one
  anecdote.

## Evidence log

Keep the log in `ideas/<idea-id>/evidence-log.md`. Add one row per
**material claim**: a claim that a recommendation, number or threshold
depends on.

| ID | Claim | Class | Source or file | Date (published / observed) | Period | Geography | Segment | Units | Filters | Limitations | Strength (reason) | Verify by |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | | | | | | | | | | | | |

Reports and the handoff cite these IDs.

## Numbers

- Every number is one of three things: **sourced** (log ID), an
  **estimate** (calculation shown, as a low / base / high range where
  uncertain), or an **assumption** (labelled as one).
- Show the calculation, for example
  `600 qualified viewers × 5–15% conversion = 30–90 buyers; capped at capacity 60`.
- **Without research access**, don't state any external figure at all: no
  remembered statistics, market sizes, prices or growth rates. Keep the
  input as a named variable, show the formula, and name the exact dataset
  to check (`Source unavailable: verify via <dataset, table or series>`).
  Figures supplied by the user or in their files are still usable.
