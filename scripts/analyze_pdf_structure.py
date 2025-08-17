#!/usr/bin/env python3
"""
Deep analysis of PDF translation approaches by different companies.
Examines PDF structure, fonts, text extraction methods, and layout preservation.
"""

import fitz  # PyMuPDF
import sys
import json
from pathlib import Path
from typing import Dict, List, Any
import hashlib

class PDFAnalyzer:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.filename = Path(pdf_path).name
        
    def analyze_structure(self) -> Dict[str, Any]:
        """Comprehensive PDF structure analysis."""
        analysis = {
            "filename": self.filename,
            "metadata": self._get_metadata(),
            "document_info": self._get_document_info(),
            "pages": [],
            "fonts": self._analyze_fonts(),
            "images": self._analyze_images(),
            "form_fields": self._analyze_forms(),
            "text_extraction": self._analyze_text_extraction(),
            "rendering_approach": self._determine_rendering_approach(),
        }
        
        # Analyze each page
        for page_num, page in enumerate(self.doc):
            page_analysis = self._analyze_page(page, page_num)
            analysis["pages"].append(page_analysis)
            
        return analysis
    
    def _get_metadata(self) -> Dict:
        """Extract PDF metadata."""
        metadata = self.doc.metadata
        return {
            "producer": metadata.get("producer", ""),
            "creator": metadata.get("creator", ""),
            "title": metadata.get("title", ""),
            "author": metadata.get("author", ""),
            "subject": metadata.get("subject", ""),
            "keywords": metadata.get("keywords", ""),
            "creationDate": str(metadata.get("creationDate", "")),
            "modDate": str(metadata.get("modDate", "")),
        }
    
    def _get_document_info(self) -> Dict:
        """Get general document information."""
        return {
            "page_count": self.doc.page_count,
            "is_encrypted": self.doc.is_encrypted,
            "is_form_pdf": self.doc.is_form_pdf,
            "is_reflowable": self.doc.is_reflowable,
            "is_repaired": self.doc.is_repaired,
            "pdf_version": getattr(self.doc, 'pdf_version', 'unknown'),
            "file_size": Path(self.pdf_path).stat().st_size,
        }
    
    def _analyze_fonts(self) -> Dict:
        """Analyze fonts used in the document."""
        fonts = {}
        for page in self.doc:
            for font in page.get_fonts():
                font_name = font[3]  # Font name
                if font_name not in fonts:
                    fonts[font_name] = {
                        "name": font_name,
                        "type": font[0],  # Font type
                        "encoding": font[2],  # Encoding
                        "pages_used": [],
                        "is_embedded": "+" in font_name,  # Embedded fonts often have + prefix
                    }
                fonts[font_name]["pages_used"].append(page.number)
        
        return fonts
    
    def _analyze_images(self) -> Dict:
        """Analyze images in the document."""
        images_info = {
            "total_count": 0,
            "by_page": {},
            "formats": set(),
        }
        
        for page_num, page in enumerate(self.doc):
            image_list = page.get_images()
            if image_list:
                images_info["by_page"][page_num] = len(image_list)
                images_info["total_count"] += len(image_list)
                
                for img in image_list:
                    try:
                        xref = img[0]
                        pix = fitz.Pixmap(self.doc, xref)
                        images_info["formats"].add(pix.colorspace.name if pix.colorspace else "unknown")
                        pix = None
                    except:
                        images_info["formats"].add("unknown")
        
        images_info["formats"] = list(images_info["formats"])
        return images_info
    
    def _analyze_forms(self) -> Dict:
        """Analyze form fields if present."""
        forms_info = {
            "has_forms": self.doc.is_form_pdf,
            "field_count": 0,
            "field_types": [],
            "fields": []
        }
        
        if self.doc.is_form_pdf:
            for page in self.doc:
                widgets = page.widgets()
                for widget in widgets:
                    forms_info["field_count"] += 1
                    field_info = {
                        "field_name": widget.field_name,
                        "field_type": widget.field_type,
                        "field_value": widget.field_value,
                        "page": page.number
                    }
                    forms_info["fields"].append(field_info)
                    if widget.field_type not in forms_info["field_types"]:
                        forms_info["field_types"].append(widget.field_type)
        
        return forms_info
    
    def _analyze_text_extraction(self) -> Dict:
        """Analyze how text is stored and can be extracted."""
        text_info = {
            "extraction_methods": {},
            "total_characters": 0,
            "has_searchable_text": False,
            "text_rendering_mode": None,
        }
        
        # Try different extraction methods
        for page in self.doc[:3]:  # Sample first 3 pages
            # Raw text
            raw_text = page.get_text()
            text_info["extraction_methods"]["raw"] = len(raw_text) > 0
            
            # Text with layout preservation
            blocks = page.get_text("blocks")
            text_info["extraction_methods"]["blocks"] = len(blocks) > 0
            
            # Text as dict (detailed)
            text_dict = page.get_text("dict")
            text_info["extraction_methods"]["dict"] = len(text_dict.get("blocks", [])) > 0
            
            text_info["total_characters"] += len(raw_text)
            if len(raw_text) > 10:
                text_info["has_searchable_text"] = True
        
        return text_info
    
    def _analyze_page(self, page, page_num: int) -> Dict:
        """Detailed analysis of a single page."""
        # Get text blocks with positions
        blocks = page.get_text("blocks")
        
        # Get drawings/vectors
        drawings = page.get_drawings()
        
        page_info = {
            "page_number": page_num,
            "width": page.rect.width,
            "height": page.rect.height,
            "rotation": page.rotation,
            "text_blocks": len(blocks),
            "drawing_commands": len(drawings),
            "has_images": len(page.get_images()) > 0,
            "text_coverage": self._calculate_text_coverage(page, blocks),
            "is_scanned": self._is_likely_scanned(page, blocks),
        }
        
        return page_info
    
    def _calculate_text_coverage(self, page, blocks) -> float:
        """Calculate percentage of page covered by text."""
        if not blocks:
            return 0.0
        
        text_area = 0
        for block in blocks:
            if block[6] == 0:  # Text block (not image)
                x0, y0, x1, y1 = block[:4]
                text_area += (x1 - x0) * (y1 - y0)
        
        page_area = page.rect.width * page.rect.height
        return (text_area / page_area) * 100 if page_area > 0 else 0
    
    def _is_likely_scanned(self, page, blocks) -> bool:
        """Determine if page is likely a scanned image."""
        # If page has one large image and no/little text, likely scanned
        images = page.get_images()
        has_full_page_image = False
        
        if images:
            for img in images:
                try:
                    # Check if image covers most of the page
                    img_rect = page.get_image_bbox(img)
                    if img_rect:
                        img_area = img_rect.width * img_rect.height
                        page_area = page.rect.width * page.rect.height
                        if img_area / page_area > 0.8:
                            has_full_page_image = True
                            break
                except:
                    continue
        
        # Little to no text blocks suggests scanned
        has_minimal_text = len(blocks) < 3
        
        return has_full_page_image and has_minimal_text
    
    def _determine_rendering_approach(self) -> str:
        """Determine the likely approach used for PDF creation/translation."""
        # Analyze characteristics to determine approach
        
        # Check for rasterization
        total_pages = self.doc.page_count
        pages_with_images = sum(1 for p in self.doc if p.get_images())
        image_ratio = pages_with_images / total_pages if total_pages > 0 else 0
        
        # Check text preservation
        has_text = any(len(p.get_text()) > 10 for p in self.doc)
        
        # Check fonts
        fonts = self._analyze_fonts()
        embedded_fonts = sum(1 for f in fonts.values() if f["is_embedded"])
        
        # Determine approach
        if image_ratio > 0.8 and not has_text:
            return "FULL_RASTERIZATION"
        elif image_ratio > 0.8 and has_text:
            return "IMAGE_WITH_OCR_OVERLAY"
        elif embedded_fonts > 0 and has_text:
            return "TEXT_REPLACEMENT_WITH_EMBEDDING"
        elif has_text:
            return "TEXT_REPLACEMENT_NATIVE"
        else:
            return "UNKNOWN"
    
    def close(self):
        """Close the PDF document."""
        self.doc.close()


def compare_files(original_path: str, translated_path: str) -> Dict:
    """Compare original and translated PDFs to understand translation approach."""
    orig_analyzer = PDFAnalyzer(original_path)
    trans_analyzer = PDFAnalyzer(translated_path)
    
    orig_analysis = orig_analyzer.analyze_structure()
    trans_analysis = trans_analyzer.analyze_structure()
    
    comparison = {
        "original": orig_analysis,
        "translated": trans_analysis,
        "differences": {
            "page_count_changed": orig_analysis["document_info"]["page_count"] != trans_analysis["document_info"]["page_count"],
            "file_size_ratio": trans_analysis["document_info"]["file_size"] / orig_analysis["document_info"]["file_size"],
            "text_preserved": trans_analysis["text_extraction"]["has_searchable_text"],
            "fonts_changed": set(orig_analysis["fonts"].keys()) != set(trans_analysis["fonts"].keys()),
            "rendering_approach_changed": orig_analysis["rendering_approach"] != trans_analysis["rendering_approach"],
            "producer_software": trans_analysis["metadata"]["producer"],
        }
    }
    
    orig_analyzer.close()
    trans_analyzer.close()
    
    return comparison


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_pdf_structure.py <pdf_file> [translated_file]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if len(sys.argv) > 2:
        # Compare mode
        translated_path = sys.argv[2]
        comparison = compare_files(pdf_path, translated_path)
        print(json.dumps(comparison, indent=2, default=str))
    else:
        # Single file analysis
        analyzer = PDFAnalyzer(pdf_path)
        analysis = analyzer.analyze_structure()
        analyzer.close()
        
        print(json.dumps(analysis, indent=2, default=str))


if __name__ == "__main__":
    main()