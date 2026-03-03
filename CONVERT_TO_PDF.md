# Convert Technical Document to PDF

## Option 1: Using Pandoc (Recommended)

### Install Pandoc
```bash
# Windows (using Chocolatey)
choco install pandoc

# Mac
brew install pandoc

# Linux
sudo apt-get install pandoc
```

### Convert to PDF
```bash
pandoc TECHNICAL_SOLUTION.md -o TECHNICAL_SOLUTION.pdf --pdf-engine=xelatex -V geometry:margin=1in
```

---

## Option 2: Using Online Converter

1. Go to https://www.markdowntopdf.com/
2. Upload `TECHNICAL_SOLUTION.md`
3. Click "Convert"
4. Download PDF

---

## Option 3: Using VS Code

1. Install extension: "Markdown PDF"
2. Open `TECHNICAL_SOLUTION.md`
3. Right-click → "Markdown PDF: Export (pdf)"
4. PDF will be saved in same directory

---

## Option 4: Using Chrome/Edge

1. Open `TECHNICAL_SOLUTION.md` in VS Code
2. Press `Ctrl+Shift+V` (preview)
3. Right-click preview → "Open in Browser"
4. In browser: `Ctrl+P` → "Save as PDF"

---

## Option 5: Using Word

1. Open `TECHNICAL_SOLUTION.md` in VS Code
2. Copy all content
3. Paste into Microsoft Word
4. Format as needed
5. File → Save As → PDF

---

## Recommended Settings

**Page Size:** A4 or Letter  
**Margins:** 1 inch all sides  
**Font:** Arial or Calibri, 11pt  
**Line Spacing:** 1.15 or 1.5  

---

## Quick Command (if Pandoc installed)

```bash
pandoc TECHNICAL_SOLUTION.md -o TECHNICAL_SOLUTION.pdf
```

This will create `TECHNICAL_SOLUTION.pdf` ready for submission!
