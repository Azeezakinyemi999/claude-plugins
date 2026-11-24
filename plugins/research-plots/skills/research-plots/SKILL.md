---
name: research-plots
description: House plotting style for every data figure. White background, black text, a thick black frame and thick lines, large fonts, a few colour-blind-safe Okabe-Ito colours that keep one meaning across a project, labels next to the data instead of legends, real data only, and a vector PDF plus a 600 dpi PNG drawn at final print size. Ships a matplotlib style module and a checker for finished figures. Use when making, restyling, fixing or reviewing any data plot, chart or figure, in any tool (matplotlib, pgfplots or TikZ, plotly, a PowerPoint chart) and for any destination (paper, slides, poster, report, thesis or defence), even when the request says nothing about style, and when the user asks for a publication-quality, high-quality or high-definition plot. Where the dataviz skill or an older project style file disagrees, this skill wins; inside a Research Storyboard deck, keep the storyboard's role colours.
---

# Research plots

Figures a reader understands at a glance: thick black lines, large black text, a white background,
a few strong colours that mean the same thing in every figure, and only real data. This page gives
the rules and the numbers. `<skill>/assets/research_style.py` applies the numbers in matplotlib and
checks a finished figure. `<skill>/assets/approved_example.png`, where it exists, is the figure the
user approved; it holds unpublished data, so it stays on the user's machine and is not in the
published plugin. `<skill>` is the folder this SKILL.md is in. The skill draws and checks figures; it never invents a
value and never sends a figure anywhere.

## Hard rules

1. **Real data only.** Every value on a figure, and every number in its caption, is read by a script
   from a result file. Never invent, smooth, digitise from a picture, or round a value into a
   different claim. If the user gives only a picture, find the script and data that made it (step 2
   of the workflow), or ask for the file. With no data at all, draw a labelled schematic with no
   numbers.
2. **Writes only these, in the user's project:** the figure script, the figure files (PDF and PNG),
   the caption file, one copy of `research_style.py`, a README section on how to rebuild the
   figure, and the profile `.claude/research-plots-profile.md`. Give new files new names; replace an
   existing figure, script, style file or README section only when the user asks.
3. **Ask once for the profile.** On the first run in a repository, write the profile and ask the user
   to confirm it. Later runs read it without asking. Why: the Python environment, the project's
   colour mapping and its approved figures differ between projects and machines, and the user
   should only have to say them once.
4. **This page wins** over the dataviz skill and over older project style files. Inside a Research
   Storyboard deck, keep the storyboard's role colours; every other rule still applies.
5. **Nothing outward.** Never upload, send or share a figure.

## Files

| Path | Holds |
| --- | --- |
| `<skill>/assets/research_style.py` | the matplotlib settings (`use_research_style()`), the colours (`COLOURS`), `save()` for PDF and 600 dpi PNG, and `check_figure()` |
| `<skill>/assets/approved_example.png` | the figure the user approved, on the user's own machine only (not published). Look at it before you draw when it is there; otherwise section 1 is the reference |
| `<repo>/.claude/research-plots-profile.md` | this project's Python, style-module copy, colour mapping, approved figures and outdated style files (template at the end) |

`<repo>` is the project root: `git rev-parse --show-toplevel`, or the working folder outside git.

## What the user said

These are the user's own words. They are the source of every rule below.

- 2026-09-17, about a crowded slide: "hd publication quality plot", "plots with good font size,
  white background, sharp black text axis."
- 2026-09-19: "high-quality pdf plots" for the defence; "Use real data, make real high quality plots".
- 2026-09-23: "HIGH QUALITY VISUALS WITH GOOD PRIMARY APPEALING COLORS", "PRIORITIZE VISUALS AND PLOTS
  OVER BULKY TEXT", slide text "generally about 18 pt", and "Convert this plot to an editable powerpoint
  plot."
- 2026-11-06: "I prefer my figures to be high quality, HIGH DEFINITION, BLACK THICK VISIBLE LINES AND LARGE
  FONTS SIZES." The figure made for this request was approved with "Keep this version"; the
  numbers in section 1 are measured from it (a local copy is `assets/approved_example.png`).
- 2026-11-20, about a poster: use "black text", "not gray light text"; the colours were "not uniform and
  consistent", the result looked "AI-ish", and there was "a lot going on".
- 2026-11-23: LaTeX and pgfplots paper plots use the same text sizes as the matplotlib figures ("Yes, same
  sizes").

## 1. The numbers

All values come from the approved figure. Draw the figure at its final printed size, so that no one
scales it later and the text prints at the size stated here.

| item | value |
|---|---|
| width | 180 mm (double column of a paper); the approved figure is 180 x 128 mm |
| typeface | TeX Gyre Heros (a Helvetica clone that embeds), else Helvetica, else Arial; math in the same face |
| tick labels | 17 pt |
| axis titles | 20 pt |
| direct labels inside the plot | 16 pt, bold |
| frame and major ticks | 2.2 pt, black; minor ticks 1.5 pt; major ticks 9 pt long, minor ticks 5 pt |
| ticks | inside, on all four sides |
| data outlines and boxes | 4 pt |
| curves | at least 3 pt, always thicker than the frame; 4 pt when a panel has three curves or fewer |
| text colour | black, all text |
| background | white |
| grid | none |
| output | vector PDF with the font embedded and text kept as text (`pdf.fonttype` 42), and a 600 dpi PNG |

For a narrower figure, keep these text sizes and line widths. Use fewer ticks, shorter labels or fewer
panels instead of smaller text.

## 2. Colour

- Use the Okabe-Ito hues at full strength (`COLOURS` in the style module). They are colour-blind safe
  and they are the "primary appealing colors" the user asked for.
- Give the most important series black: the experiment, the reference, or the largest group.
- Keep one meaning for each colour across all figures of a project. Write the mapping once (a dict in
  the project's figure module, named in the profile) and import it in every figure script. Do not
  choose colours figure by figure. Different colours everywhere is what made the poster look AI-made.
- Use at most five hues in one figure. For more series, group them or use small multiples.
- Darken a hue that is too light for a thick line or a label: purple is `#B4508C`. Use yellow
  (`#F0E442`) only as a fill with a black outline and a hatch pattern, never as a line or as text.
- Use grey only for data marks that step back, for example raw points behind summary boxes or the model
  before a correction. Never use grey for text.
- Never let colour be the only difference between series. Add a line style, a marker shape or a hatch
  pattern, so that the figure also works in greyscale. In the approved figure the flow-reactor box is
  dashed.

## 3. Less on the figure

- Give each figure one message. Remove what does not carry it: titles inside the plot (the caption
  carries the title), grid lines, frames around legends, decoration.
- Put labels next to the data instead of in a legend. Write each label in its series colour and in bold,
  with its count where there is one (for example "Shock tubes, n = 10,535"). Put a white backing behind a
  label that sits on data. Use a legend only when direct labels do not fit.
- Where two curves nearly coincide, keep each label beside its own curve's end and push the lower label
  down; never let a label sit level with a different curve.
- Draw the largest group first, so that small groups stay visible. Keep the frame and the ticks on top of
  everything (`zorder`).
- Write units in parentheses: "Pressure (atm)". On a log axis of up to about six decades, show plain
  numbers (0.1, 1, 10, 100), not powers of ten; on a wider one, use powers of ten every two or three
  decades. Use thousands separators (10,535).
- On slides, the plot carries the message. Use short direct statements next to it, not paragraphs.

## 4. Real data, and numbers that come from files

- Write one script per figure. It reads the data, draws the figure, and writes the caption with every
  number filled in by code, headed "Do not edit the numbers by hand". Add a README section that says
  how to rebuild the figure.
- Assert in the script that no data point falls outside the axis limits. Say in the caption what was
  left out and why.

## 5. By destination

- **Paper**: 180 mm wide, PDF and PNG, plus the caption `.tex`. Use one sans-serif face across figures
  and a white background.
- **Slides**: make the figure at the size it has on the slide, so that its text reads at about 18 pt
  there. When the user may want to change the chart, build a native PowerPoint chart (pptx skill, bar,
  line or scatter) instead of a picture. Ask if you are not sure.
- **Poster**: the same rules at poster scale; black text that a reader can see from a distance.
- **pgfplots or TikZ data plots**: the same numbers as matplotlib (the user confirmed this on
  2026-11-23). Axis lines and major ticks 2.2 pt, data lines 4 pt, bar outlines black, tick labels
  17 pt and axis titles 20 pt at final size, all text black. A project's diagram style (small text, thin
  lines) is for schematics, not for plots; the profile names it.

## 6. Workflow

1. **Profile.** Read `<repo>/.claude/research-plots-profile.md`. If it doesn't exist:
   - find a Python that imports matplotlib: the project's own environment first (one where
     `python -m pip show <project>` finds the project, or the interpreter its editor settings name),
     then `python3`; test each with `python -c "import matplotlib"`;
   - look for existing figure scripts, a style module, a colour mapping, and older style files;
   - write the profile from the template below, show it, and ask the user once to confirm it.
2. **Data.** Find the result file and the script that made the figure. When the user gives only a
   picture, search the repository for the figure's axis titles and series names. Ask for the file if
   it isn't there. Read the old script before you change anything.
3. **Style module.** Copy `<skill>/assets/research_style.py` once into the project's figure folder,
   with a first line saying where it came from and that the copy is not edited. Figure scripts import
   the copy, so they rebuild without the skill installed. Record its path in the profile.
4. **Script.** Write one script per figure from the starting point below, with a new name next to the
   old one. Use the project's colour mapping; if the project has none, define it once and record where.
5. **Run it** with the profile's Python, then **Verify**.

Matplotlib starting point (after step 3):

```python
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from research_style import use_research_style, save, check_figure, COLOURS, MM, OUTLINE_PT, ANNOT_PT

use_research_style()
fig, ax = plt.subplots(figsize=(180 * MM, 128 * MM))
ax.scatter(x, y, s=7, color=COLOURS["grey_points"], alpha=0.4, rasterized=True)  # dense points: raster layer
ax.plot(xs, ys, color=COLOURS["black"], lw=OUTLINE_PT)
ax.text(x0, y0, "Shock tubes\n$n$ = 10,535", color=COLOURS["black"], fontsize=ANNOT_PT, fontweight="bold")
(x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
assert ((x >= x0) & (x <= x1) & (y >= y0) & (y <= y1)).all(), "a data point falls outside the axes"
for problem in check_figure(fig):
    print(problem)
save(fig, "figures/fig_name")  # figures/fig_name.pdf and figures/fig_name.png, 600 dpi, white
```

Rasterize dense scatter layers (`rasterized=True`). The PDF then keeps vector text and lines and stays
small. For rounded boxes on a log axis, label backings and the caption writer, read the approved
figure script if the profile names one.

## Verify

1. Open the PNG and look at it at the size it will print. Fix overlaps, clipped labels, labels that
   cover data, and labels that sit level with the wrong curve.
2. Render the PDF (for example `pdftoppm -png -r 150`) and check that it shows the same as the PNG;
   `pdffonts` should list the typeface as embedded.
3. Run `check_figure(fig)`. Fix each item, or tell the user why it stays. The check measures text size,
   grey text, typeface, text that runs off the figure, background, frame, line widths, grid and legends.
   It cannot see a label that covers a curve, clutter, or colours that change meaning between figures;
   judge those from the picture.
4. Check that every number on the figure and in the caption comes from a file.

## Hand-off

Tell the user, in a few sentences:

- the file paths (script, PDF, PNG, caption) and the figure's size;
- what changed from the old figure, and any rule on this page you didn't follow, with the reason;
- what `check_figure` reported, and whether you compared the PDF with the PNG;
- anything not done, such as a colour mapping that lives only in the new script.

## Profile template

`<repo>/.claude/research-plots-profile.md`:

```markdown
# research-plots profile: <repository name>

Written <YYYY-MM-DD> by the research-plots skill; confirmed by the user <YYYY-MM-DD>.
Edit it to steer the skill.

- **Python with matplotlib:** <interpreter path>; fallback `python3`
- **Style module copy:** <path of research_style.py in this repository>
- **Colour mapping:** <module and name of the dict that maps each series or category to a colour>, or none yet
- **Figure scripts and outputs:** <where figure scripts live and where they write>
- **Approved figures:** <script paths the user approved, and what to copy from each>
- **Diagram style (not for plots):** <path>, or none
- **Older style files not to copy:** <path: what is outdated about it>
- **Caption format:** <LaTeX figure environment, or plain text>
```
