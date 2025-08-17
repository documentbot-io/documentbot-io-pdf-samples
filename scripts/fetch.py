#!/usr/bin/env python3
"""
Fetch publicly available PDF samples from their official sources.
Only downloads PDFs that are clearly redistributable (public domain, CC licensed, etc.)
"""

import os
import sys
import yaml
import hashlib
import requests
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

# Configuration
SAMPLES_DIR = Path(__file__).parent.parent / "samples"
MANIFEST_FILE = SAMPLES_DIR / "manifest.yaml"
ORIGINALS_DIR = SAMPLES_DIR / "originals"
USER_AGENT = "Mozilla/5.0 (PDF Sample Fetcher for Testing)"
CHUNK_SIZE = 8192

# Public domain / freely available samples
FETCH_URLS = {
    "irs-1040": "https://www.irs.gov/pub/irs-pdf/f1040.pdf",
    "irs-w9": "https://www.irs.gov/pub/irs-pdf/fw9.pdf",
    "bitcoin-whitepaper": "https://bitcoin.org/bitcoin.pdf",
    # Add more URLs as they are verified to be redistributable
}

class PDFFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
        self.manifest = self._load_manifest()
    
    def _load_manifest(self) -> Dict:
        """Load the manifest.yaml file."""
        if not MANIFEST_FILE.exists():
            print(f"Error: Manifest file not found at {MANIFEST_FILE}")
            sys.exit(1)
        
        with open(MANIFEST_FILE, 'r') as f:
            return yaml.safe_load(f)
    
    def _get_file_hash(self, filepath: Path) -> str:
        """Calculate SHA256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def _download_file(self, url: str, dest_path: Path) -> bool:
        """Download a file from URL to destination path."""
        try:
            print(f"  Downloading from: {url}")
            response = self.session.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Create parent directory if it doesn't exist
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Download with progress indication
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\r  Progress: {progress:.1f}%", end='', flush=True)
            
            print()  # New line after progress
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"  Error downloading: {e}")
            return False
    
    def fetch_sample(self, sample_id: str, sample_info: Dict) -> bool:
        """Fetch a single PDF sample."""
        # Determine the destination path
        category = sample_info.get('category', 'uncategorized')
        filename = sample_info.get('filename', f"{sample_id}.pdf")
        dest_path = ORIGINALS_DIR / category / filename
        
        # Check if file already exists
        if dest_path.exists():
            print(f"  File already exists: {dest_path}")
            return True
        
        # Check if we have a URL for this sample
        source_url = sample_info.get('source_url')
        if not source_url:
            # Check our hardcoded URLs
            source_url = FETCH_URLS.get(sample_id)
        
        if not source_url:
            print(f"  No URL available for automatic download")
            return False
        
        # Check if this is a redistributable license
        license_type = sample_info.get('license', '').lower()
        redistributable = license_type in [
            'public-domain', 'cc-by', 'cc-by-sa', 'cc0', 
            'mit', 'apache-2.0', 'bsd'
        ]
        
        if not redistributable and license_type != 'arxiv':
            print(f"  Skipping due to unclear redistribution rights (license: {license_type})")
            print(f"  Please download manually from: {source_url}")
            return False
        
        # Download the file
        return self._download_file(source_url, dest_path)
    
    def fetch_all(self, sample_ids: Optional[List[str]] = None):
        """Fetch all or specified PDF samples."""
        samples = self.manifest.get('samples', [])
        
        for sample in samples:
            sample_id = sample.get('id')
            if not sample_id:
                continue
            
            # Skip if specific samples requested and this isn't one
            if sample_ids and sample_id not in sample_ids:
                continue
            
            print(f"\nProcessing: {sample_id}")
            
            # Check source type
            source = sample.get('source', '')
            if source in ['generated', 'synthetic', 'scan']:
                print(f"  Skipping - requires manual creation (source: {source})")
                continue
            
            # Try to fetch
            if self.fetch_sample(sample_id, sample):
                print(f"  Successfully fetched: {sample_id}")
            else:
                print(f"  Could not fetch: {sample_id}")
    
    def generate_placeholder(self, sample_id: str):
        """Generate a placeholder PDF for testing."""
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        
        sample = next((s for s in self.manifest.get('samples', []) 
                      if s.get('id') == sample_id), None)
        
        if not sample:
            print(f"Sample {sample_id} not found in manifest")
            return
        
        category = sample.get('category', 'uncategorized')
        filename = sample.get('filename', f"{sample_id}.pdf")
        dest_path = ORIGINALS_DIR / category / filename
        
        if dest_path.exists():
            print(f"File already exists: {dest_path}")
            return
        
        # Create directory if needed
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generate simple placeholder PDF
        c = canvas.Canvas(str(dest_path), pagesize=letter)
        c.drawString(100, 750, f"Placeholder PDF: {sample_id}")
        c.drawString(100, 730, f"Category: {category}")
        c.drawString(100, 710, f"This is a placeholder for testing.")
        c.drawString(100, 690, "Replace with actual sample when available.")
        
        # Add sample text for simple documents
        if category == 'simple':
            c.drawString(100, 650, "Sample Text Content")
            c.drawString(100, 630, "Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
            c.drawString(100, 610, "• Bullet point one")
            c.drawString(100, 590, "• Bullet point two")
            c.drawString(100, 570, "• Bullet point three")
        
        c.save()
        print(f"Generated placeholder: {dest_path}")

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Fetch PDF samples for testing")
    parser.add_argument('samples', nargs='*', help='Specific sample IDs to fetch')
    parser.add_argument('--all', action='store_true', help='Fetch all samples')
    parser.add_argument('--placeholder', help='Generate placeholder for specific sample')
    
    args = parser.parse_args()
    
    fetcher = PDFFetcher()
    
    if args.placeholder:
        fetcher.generate_placeholder(args.placeholder)
    elif args.all or not args.samples:
        print("Fetching all available samples...")
        fetcher.fetch_all()
    else:
        print(f"Fetching specified samples: {args.samples}")
        fetcher.fetch_all(args.samples)
    
    print("\nDone!")
    print("\nNote: Some samples require manual creation or acquisition:")
    print("- Scanned documents (scan a physical menu, brochure, etc.)")
    print("- Generated samples (use Word/Google Docs to create)")
    print("- Synthetic data (bank statements, invoices)")
    print("- Samples with unclear licensing (download manually)")

if __name__ == "__main__":
    main()