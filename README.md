# PDF Translation Test Samples

This repository contains a comprehensive test corpus for evaluating PDF translation algorithms and implementations. It serves as a reference dataset for the Vietnam engineering team developing DocumentBot's PDF translation capabilities.

## Repository Purpose

This repository provides:
- **Representative PDF samples** across document categories and complexity levels
- **Translated outputs** from major PDF translation providers (Google, PDFSimpli, PDFGuru)
- **Deep technical analysis** of existing translation algorithms and approaches
- **Testing framework** for evaluating translation quality and performance
- **Benchmarking data** for comparing different translation strategies

## For Engineering Teams

### What This Repository Contains

1. **Test Corpus**: 14 carefully selected PDF documents representing real-world use cases
2. **Translation Samples**: Complete translation sets in Vietnamese (Google, PDFSimpli) and Spanish (PDFGuru)
3. **Algorithm Analysis**: Technical deep-dive into how existing providers handle PDF translation
4. **Evaluation Tools**: Scripts for analyzing PDF structure, fonts, and rendering approaches
5. **Performance Data**: File size impacts, processing characteristics, and quality metrics

### Key Engineering Insights

- **Algorithm Discovery**: Three distinct approaches identified through reverse engineering
- **Performance Benchmarks**: File size changes, processing characteristics, and quality trade-offs
- **Technical Specifications**: Font handling, form preservation, vector graphics retention strategies
- **Implementation Patterns**: How to detect and classify different translation approaches

## Repository Structure

```
├── originals/                     # Source PDFs (<category>.<src-lang>.<filename>.pdf)
├── translated/
│   ├── google/                    # Google Translate Vietnamese translations  
│   ├── pdfsimpli/                 # PDFSimpli Vietnamese translations
│   └── pdfguru/                   # PDFGuru Spanish translations
├── analysis/                      # Technical analysis and benchmarking data
├── scripts/
│   ├── analyze_pdf_structure.py   # PDF analysis and comparison tool
│   ├── fetch.py                   # Download public domain samples
│   └── create_placeholder.py      # Generate test PDFs
├── docs/
│   └── acceptance-checklist.md    # Quality evaluation criteria
└── samples/
    └── manifest.yaml              # Metadata for all PDF samples
```

## Document Categories

- **Government Forms** (`tax`, `forms`, `gov`) - Interactive PDFs with form fields
- **Academic Papers** (`academic`) - Complex layouts with equations and references
- **Business Documents** (`finance`, `resume`) - Professional documents with tables
- **Scanned Documents** (`ocr`, `restaurant`) - Image-based PDFs requiring OCR
- **Complex Layouts** (`landscape`, `book`) - Multi-column and specialized formatting

## Naming Conventions

### Original Files
`<category>.<src-lang>.<filename>.pdf`

Examples:
- `tax.en.irs-1040.pdf`
- `academic.en.attention.pdf` (Transformer paper)
- `resume.en.engineer.pdf`

### Translated Files
`<category>.<src-lang>.<filename>.<dst-lang>.<provider>.pdf`

Examples:
- `translated/google/tax.en.irs-1040.vi.google.pdf`
- `translated/pdfsimpli/academic.en.attention.vi.pdfsimpli.pdf`
- `translated/pdfguru/resume.en.engineer.es.pdfguru.pdf`

---

# PDF Translation Algorithm Analysis

## Executive Summary

Through methodical analysis of PDF file structure, fonts, rendering methods, and text extraction algorithms, we've identified three fundamentally different approaches to PDF translation used by major providers. Each company has developed distinct strategies for handling text replacement, layout preservation, and complex document elements.

## Research Methodology

The analysis examined actual PDF bytes using PyMuPDF to understand:
- Font handling and embedding strategies
- Text rendering and positioning methods
- Form field preservation approaches
- Image rasterization patterns
- File size changes and compression
- Metadata and producer signatures

## Algorithm Discovery

### 🔵 Google Translate: Hybrid Rasterization + OCR Overlay

**Core Algorithm**: Complete page rasterization with text overlay

**Technical Implementation**:
1. **Page Rasterization**: Converts each PDF page into a raster image
2. **OCR Text Overlay**: Places translated text as searchable overlay on the image
3. **Form Destruction**: All interactive elements are completely removed

**Key Technical Characteristics**:
- **Producer Software**: PDFium (Google's PDF library)
- **Font Strategy**: Simple system fonts only (NotoSansMono-Regular, Helvetica)
- **File Size Impact**: 2.5x increase for forms, 35% decrease for academic papers
- **Form Handling**: Complete destruction (23 form fields → 0 form fields)
- **Vector Graphics**: All converted to raster (71 drawing commands → 0)

**Strengths**:
- Perfect layout preservation (original layout becomes immutable image)
- Handles complex documents (equations, tables, multi-column) flawlessly
- Consistent output regardless of document complexity

**Weaknesses**:
- Destroys accessibility (screen readers cannot access rasterized content)
- Eliminates all interactivity (forms, buttons, links)
- Significant file size increases for simple documents

**📖 [Read the complete deep dive analysis of Google's approach →](analysis/Google_PDF_Translation_Deep_Dive.md)**

---

### 🟢 PDFSimpli: Intelligent Text Replacement with Preservation

**Core Algorithm**: Smart text substitution with structure preservation

**Technical Implementation**:
1. **Text Analysis**: Identifies translatable text blocks while preserving structure
2. **Smart Font Substitution**: Uses iText library for sophisticated font handling
3. **Form Preservation**: Maintains interactive elements while translating labels
4. **Vector Retention**: Preserves original drawing commands and layout elements

**Key Technical Characteristics**:
- **Producer Software**: iText Core 8.0.5 (Apryse Group NV, WorkSimpli Software)
- **Font Strategy**: Maintains original font characteristics when possible
- **File Size Impact**: 9x increase for forms (140KB → 1.3MB)
- **Form Handling**: **Only provider that preserves all form fields**
- **Vector Graphics**: Fully retained (preserves 71 drawing commands)

**Strengths**:
- Only solution maintaining interactive PDF forms
- Full text searchability and accessibility
- Maintains crisp vector graphics and scalable text
- Professional output with original functionality

**Weaknesses**:
- Massive file size increases (up to 57x for some documents)
- Potential font licensing issues with proprietary embedded fonts
- More prone to text overflow with significant length changes

---

### 🟡 PDFGuru: Native Text Substitution with Minimal Modification

**Core Algorithm**: Direct text replacement with minimal structural changes

**Technical Implementation**:
1. **Direct Text Substitution**: Replaces content while maintaining PDF structure
2. **Metadata Preservation**: Keeps original document metadata intact
3. **Conservative Font Handling**: Minimal changes to font embedding
4. **Selective Processing**: Adapts strategy based on document type

**Key Technical Characteristics**:
- **Producer Software**: Often preserves original (Designer 6.5, pdfTeX)
- **Font Strategy**: Context-dependent, preserves original fonts when possible
- **File Size Impact**: Extreme increases (57x for forms: 140KB → 8MB)
- **Form Handling**: Variable results
- **Text Preservation**: Generally maintains searchability

**Strengths**:
- Preserves original metadata and creator information
- Least invasive approach to PDF structure
- Adapts processing based on document complexity

**Weaknesses**:
- Highly variable quality depending on source document
- Most severe file size increases observed
- Cannot handle purely scanned/image-based documents

## Comparative Technical Analysis

### Performance by Document Type

| Document Type | Google | PDFSimpli | PDFGuru |
|---------------|--------|-----------|---------|
| **Government Forms** | Perfect layout, forms destroyed | Forms preserved, large files | Extreme file bloat |
| **Academic Papers** | Perfect layout, smaller files | Good quality, moderate bloat | Good quality, significant bloat |
| **Scanned Documents** | Often fails/refused | Can process | Mixed results |

### Technical Approach Comparison

| Aspect | Google | PDFSimpli | PDFGuru |
|--------|--------|-----------|---------|
| **Core Method** | Rasterize + OCR | Text Replacement | Direct Substitution |
| **Form Handling** | Destroy | Preserve | Variable |
| **Font Strategy** | System fonts only | Smart substitution | Preserve original |
| **File Size Impact** | 35%-250% | 200%-900% | 400%-5700% |
| **Accessibility** | Poor (rasterized) | Excellent | Good |
| **Vector Graphics** | Lost | Preserved | Preserved |

## Engineering Recommendations

### For Production Systems

1. **Choose PDFSimpli** for documents requiring form functionality and accessibility
2. **Use Google** for presentation materials where visual layout is paramount
3. **Avoid PDFGuru** in production due to extreme file size increases

### Implementation Strategy

- **Document Classification**: Implement different strategies based on document type
- **Form Detection**: Use `is_form_pdf` flag to route documents appropriately
- **File Size Monitoring**: Implement size limits and compression strategies
- **Quality Metrics**: Test text searchability, form functionality, and visual fidelity

### Algorithm Detection Signatures

Each provider leaves distinct technical fingerprints:

**Google Detection**:
- Producer: "PDFium" or empty
- Image count equals page count
- Zero drawing commands in output
- Font names become simple system fonts

**PDFSimpli Detection**:
- Producer contains "iText Core" and "WorkSimpli Software"
- Form fields preserved (`is_form_pdf` remains true)
- Drawing commands retained
- Significant text block multiplication

**PDFGuru Detection**:
- Producer preserves original software name
- Extreme file size increases
- Variable text preservation
- Inconsistent approach between document types

## Tools and Analysis

### PDF Analysis Script
Use `scripts/analyze_pdf_structure.py` to:
- Compare original and translated PDF structures
- Analyze font embedding and substitution strategies
- Measure file size impacts and compression ratios
- Detect rendering approach changes

### Evaluation Framework
- **Quality Metrics**: Text accuracy, layout preservation, functionality retention
- **Performance Metrics**: File size ratios, processing time, memory usage
- **Accessibility Testing**: Screen reader compatibility, text searchability

This analysis provides concrete technical evidence for implementing DocumentBot's PDF translation capabilities with full understanding of existing market approaches and their trade-offs.

## Development Setup

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Download public samples
python scripts/fetch.py --all

# Analyze specific documents
python scripts/analyze_pdf_structure.py originals/tax.en.irs-1040.pdf translated/google/tax.en.irs-1040.vi.google.pdf
```

## Language Support

- **English** (en) - Source language for all documents
- **Vietnamese** (vi) - Google and PDFSimpli translations
- **Spanish** (es) - PDFGuru translations

## Contributing

1. Add new originals with proper naming: `<category>.<src-lang>.<filename>.pdf`
2. Update `samples/manifest.yaml` with document metadata
3. Include provider outputs following naming convention
4. Run analysis tools to document technical characteristics

## Licensing

Most samples are public domain (government forms, academic papers) or fair use for research. See `samples/LICENSES.md` for details.