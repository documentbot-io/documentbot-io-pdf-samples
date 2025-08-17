# PDF Translation Acceptance Checklist

Use this checklist to evaluate translated PDFs across different providers.

## Universal Checks (All Categories)

### Text Preservation
- [ ] All visible text is translated
- [ ] No text is missing or cut off
- [ ] Character encoding is correct (no mojibake/�)
- [ ] Punctuation is appropriate for target language

### Layout Fidelity
- [ ] Page breaks are preserved
- [ ] Margins and spacing are maintained
- [ ] Text doesn't overflow containers
- [ ] Alignment (left/right/center/justified) is preserved

### Visual Elements
- [ ] Images are preserved and not corrupted
- [ ] Logos and graphics remain in place
- [ ] Background colors/patterns are maintained
- [ ] Watermarks (if any) are preserved

## Category-Specific Checks

### simple
- [ ] Paragraphs flow correctly
- [ ] Bullet points are preserved
- [ ] Bold/italic formatting is maintained
- [ ] Headers and footers are translated

### ocr
- [ ] OCR accurately captures source text
- [ ] Mixed fonts are handled correctly
- [ ] Curved/rotated text is recognized
- [ ] Text over images is extracted

### tax / forms / forms-complex
- [ ] Form fields remain fillable (if originally fillable)
- [ ] Checkboxes and radio buttons work
- [ ] Field labels are translated
- [ ] Instructions are translated and readable
- [ ] Form structure/layout is intact
- [ ] XFA forms (if present) function correctly

### academic
- [ ] Equations remain intact or are properly rendered
- [ ] References/citations are preserved
- [ ] Two-column layout is maintained
- [ ] Tables are structured correctly
- [ ] Figure captions are translated

### resume
- [ ] Contact information is preserved
- [ ] Section headers are clear
- [ ] Icons (if any) are maintained
- [ ] Multi-column layout works
- [ ] Consistent formatting throughout

### finance / business
- [ ] Numbers and currency symbols are correct
- [ ] Tables maintain alignment
- [ ] Totals and calculations are preserved
- [ ] Date formats are appropriate for locale
- [ ] Headers/footers with page numbers work

### travel / logistics
- [ ] Barcodes are preserved and scannable
- [ ] QR codes remain functional
- [ ] Critical information is highlighted
- [ ] Mixed orientations handled correctly

### medical / legal
- [ ] Dense text is readable
- [ ] Boxed warnings/notices are preserved
- [ ] Legal disclaimers are complete
- [ ] Numbered sections maintain structure
- [ ] Critical safety information is prominent

### multilingual
- [ ] Multiple languages coexist correctly
- [ ] Language-specific formatting is preserved
- [ ] Mixed scripts don't interfere
- [ ] Accents and special characters work

### pdfa
- [ ] PDF/A compliance is maintained
- [ ] Embedded fonts work correctly
- [ ] Document remains archivable
- [ ] Metadata is preserved

### graphics
- [ ] Text over images is readable
- [ ] Transparency effects work
- [ ] Vector graphics are preserved
- [ ] Complex layouts don't break

### rtl (Arabic, Hebrew)
- [ ] Text flows right-to-left correctly
- [ ] Paragraph alignment is mirrored
- [ ] Numbers display correctly (LTR within RTL)
- [ ] Punctuation is mirrored appropriately
- [ ] Mixed LTR/RTL text works

### cjk
- [ ] Vertical text (if present) is handled
- [ ] Character spacing is appropriate
- [ ] Line breaking follows CJK rules
- [ ] Ruby text/furigana (if present) is preserved
- [ ] Font selection supports all characters

## Performance Metrics

### Quality Score (1-5)
- Text accuracy: ___
- Layout preservation: ___
- Visual fidelity: ___
- Functionality (forms/links): ___
- Overall usability: ___

### Technical Issues
- [ ] File size bloat (>2x original)
- [ ] Rasterization of vector content
- [ ] Loss of text selection capability
- [ ] Broken internal links/bookmarks
- [ ] Missing fonts/font substitution

## Provider Comparison Notes
Use this section to note provider-specific strengths/weaknesses:

Provider: ________________
- Strengths:
- Weaknesses:
- Best for categories:
- Avoid for categories:
- Special configurations needed: