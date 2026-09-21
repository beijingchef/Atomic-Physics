# Editing the course website

This is a Quarto website. Edit the `.qmd` files in this folder.

- `index.qmd`: course home page
- `schedule.qmd`: schedule
- `topics.qmd`: topic directory
- `part-1.qmd`, `part-2.qmd`, `part-3.qmd`: course parts
- `lorentz-model.qmd`: first topic skeleton
- `assignments.qmd`: preparation, homework, and solutions
- `resources.qmd`: references
- `_quarto.yml`: navigation and the explicit list of pages to render
- `styles.css`: appearance

## Preview and build

Run `quarto preview` in this folder for a live preview, or `quarto render` to build the website into `_site`.

The default configuration enables HTML only. PDF page size and margins are stored in `_quarto-pdf.yml` and apply when the `pdf` profile is explicitly enabled. To render one page to PDF, use:

```powershell
quarto render lorentz-oscillator.qmd --to pdf --profile pdf
```

Restart an already-running preview after changing the project configuration.

On this computer, if Quarto is not on PATH, use PowerShell:

```powershell
& 'C:\Users\zhaok\AppData\Local\Programs\Quarto\bin\quarto.cmd' preview
```

To add a topic, create a `.qmd` file, add it to `project.render` in `_quarto.yml`, and link it from its course part and `topics.qmd`. Use `lorentz-model.qmd` as a starting point. Link to `.qmd` sources; Quarto resolves them to the rendered pages.

Only the explicitly listed course pages are rendered. Existing teaching files are not linked or included. Publish only the generated `_site` directory when ready, not the whole course folder.
