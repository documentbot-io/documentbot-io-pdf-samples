# PDF Translation Test Samples

This repository contains representative PDF samples and their translated outputs for testing and evaluation:
- Text coverage & OCR recall
- Layout fidelity (line breaks, columns, tables)
- Complex scripts (RTL, CJK)
- Forms handling (AcroForm / XFA)
- PDF/A and graphics overlays

## Structure
- `originals/` — Source PDFs with format: `<category>.<src-lang>.<filename>.pdf`
- `translated/<provider>/` — Translated outputs organized by provider
- `pseudolocale/` — Pseudolocale "translations" generated locally to stress width/RTL without calling an API
- `scripts/` — `fetch.py` to download originals; `make_pseudolocale.py` to overlay pseudo text via PyMuPDF
- `docs/acceptance-checklist.md` — What to check for each category
- `samples/manifest.yaml` — Metadata for all PDF samples

## Naming Convention

### Original Files
`<category>.<src-lang>.<filename>.pdf`

Examples:
- `tax.en.irs-1040.pdf`
- `academic.en.bitcoin.pdf`
- `resume.en.engineer.pdf`

### Translated Files
Stored in `translated/<provider>/` with format:
`<category>.<src-lang>.<filename>.<dst-lang>.<provider>.pdf`

Examples:
- `translated/google/tax.en.irs-1040.vi.google.pdf`
- `translated/pdfguru/academic.en.bitcoin.zh-Hans.pdfguru.pdf`
- `translated/pdfsimpli/resume.en.engineer.es.pdfsimpli.pdf`

### Categories
- `tax` - Tax forms and government financial documents
- `forms` - Simple government forms
- `gov` - Government documents and applications
- `academic` - Academic papers with equations and references
- `finance` - Financial statements, invoices, and bank documents
- `travel` - Travel documents and boarding passes
- `resume` - CVs and resumes with complex formatting
- `ocr` - Scanned/image-heavy PDFs requiring OCR
- `restaurant` - Restaurant menus and food service documents
- `landscape` - Landscape-oriented corporate reports
- `book` - Literature and book-formatted documents

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
1. Add new originals to `originals/` folder using format: `<category>.<src-lang>.<filename>.pdf`
2. Update `samples/manifest.yaml` with metadata for new samples
3. Commit provider outputs to `translated/<provider>/` using format: `<category>.<src-lang>.<filename>.<dst-lang>.<provider>.pdf`
4. For pseudo, run `scripts/make_pseudolocale.py` and commit to `pseudolocale/`

## Licensing
- Prefer public domain / CC-licensed sources.
- If redistribution is ambiguous, store only metadata + fetch scripts.