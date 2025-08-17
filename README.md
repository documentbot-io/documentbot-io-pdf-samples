# PDF Translation Test Samples

This repository contains representative PDF samples and their translated outputs for testing and evaluation:
- Text coverage & OCR recall
- Layout fidelity (line breaks, columns, tables)
- Complex scripts (RTL, CJK)
- Forms handling (AcroForm / XFA)
- PDF/A and graphics overlays

## Structure
- `samples/originals/` — Source PDFs by category (or `scripts/fetch.py` + `manifest.yaml` if we can't redistribute).
- `translated/` — Outputs from providers under a strict naming convention.
- `pseudolocale/` — Pseudolocale "translations" generated locally to stress width/RTL without calling an API.
- `scripts/` — `fetch.py` to download originals; `make_pseudolocale.py` to overlay pseudo text via PyMuPDF.
- `docs/acceptance-checklist.md` — What to check for each category.

## Naming Convention
`<filename>.<category>.<src-lng>.<dst-lng>.<provider>.pdf`

Examples:
- `irs-1040.tax.en.es.google.pdf`
- `bitcoin.academic.en.zh-Hans.pdfguru.pdf`
- `hello-letter.simple.en.ps-rtl.psgen.pdf`

### Categories
- `simple` - Basic text documents
- `ocr` - Scanned/image-heavy PDFs requiring OCR
- `tax` - Tax forms
- `academic` - Academic papers with equations and references
- `resume` - CVs and resumes with complex formatting
- `finance` - Financial statements and reports
- `business` - Invoices and business documents
- `travel` - Travel documents and boarding passes
- `logistics` - Shipping labels
- `medical` - Medical guides and leaflets
- `legal` - Legal documents
- `forms` - Simple forms
- `forms-complex` - Complex forms with XFA/AcroForm
- `gov` - Government documents
- `report` - Corporate reports with charts
- `multilingual` - Documents with multiple languages
- `pdfa` - PDF/A compliant documents
- `graphics` - Graphically complex brochures
- `rtl` - Right-to-left language documents
- `cjk` - CJK (Chinese, Japanese, Korean) documents

### Language Codes
Language codes use BCP-47 where helpful:
- `en` - English
- `es` - Spanish
- `vi` - Vietnamese
- `zh-Hans` - Chinese (Simplified)
- `ar` - Arabic
- `he` - Hebrew
- `fr` - French
- `pt` - Portuguese
- `ru` - Russian
- `ja` - Japanese

## Pseudolocale Profiles
- `ps-accents`: accent map for ASCII.
- `ps-expand`: +30–50% length.
- `ps-rtl`: reversed with bidi marks and mirrored punctuation.
- `ps-fullwidth`: fullwidth unicode forms.

## Fonts
Use Noto families for maximal glyph coverage. Embed fonts to keep outputs portable.

## Contributing
1. Add a new original under the correct category, or add its entry to `manifest.yaml` and run `scripts/fetch.py`.
2. Commit provider outputs to `translated/` using the naming scheme.
3. For pseudo, run `scripts/make_pseudolocale.py` and commit to `pseudolocale/`.

## Licensing
- Prefer public domain / CC-licensed sources.
- If redistribution is ambiguous, store only metadata + fetch scripts.