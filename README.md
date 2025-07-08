# Transcript Sanitizer

A simple Python tool to clean up messy HTML transcript files from video conferencing platforms like TLDV, Zoom, or Teams. Converts raw HTML transcripts into clean, readable text files organized by speaker.

## What it does

Takes those ugly HTML transcript files that are full of tags and formatting, and turns them into clean text files you can actually read. It automatically:

- Extracts speaker names from the HTML structure
- Organizes dialogue by speaker
- Creates a chronological version showing the conversation flow
- Cleans up all the HTML tags and formatting
- Handles multiple files at once

## Quick start

1. **Drop your `.raw` files into the `input/` folder**
2. **Run the script:**
   ```bash
   python3 transcript_cleaner.py
   ```
3. **Find your cleaned files in the `output/` folder**

That's it! Each input file gets two output files:
- `filename_by_speaker.txt` - All dialogue grouped by speaker
- `filename_chronological.txt` - Conversation in order

## Example

**Before** (messy HTML):
```html
<p data-index="0">
  <span data-speaker="true"><span>John</span></span>
  <span data-clipped="false" data-speaker="false">Hello</span>
  <span data-clipped="false" data-speaker="false">there!</span>
</p>
```

**After** (clean text):
```
1. John: Hello there!
```

## Folder structure

```
transcript-sanitizer/
├── input/                    # Put your .raw files here
│   ├── meeting-001.raw
│   ├── meeting-002.raw
│   └── ...
├── output/                   # Cleaned files appear here
│   ├── meeting-001_by_speaker.txt
│   ├── meeting-001_chronological.txt
│   └── ...
├── transcript_cleaner.py     # The main script
└── README.md
```

## Custom usage

If you want to use different folders:

```bash
python3 transcript_cleaner.py --input /path/to/raw/files --output /path/to/output
```

## Requirements

- Python 3.6 or higher
- No extra packages needed (uses only standard library)

## Supported formats

The script is designed for HTML transcripts with this structure:
- `<p>` tags with `data-index` attributes
- `<span>` tags with `data-speaker="true"` for speaker names
- `<span>` tags with `data-clipped` attributes for dialogue text

This covers most modern video conferencing platforms that export HTML transcripts.

## Troubleshooting

**No speakers found?**
- Check that your HTML has `data-speaker="true"` attributes
- Make sure the file is UTF-8 encoded

**Empty output?**
- Verify your files have `.raw` extension
- Check that the HTML contains actual dialogue content

**Encoding errors?**
- The script expects UTF-8 files
- Re-save your files in UTF-8 if needed

## Why I built this

I was tired of manually cleaning up transcript files from video meetings. The raw HTML exports are hard to read and full of formatting noise. This tool automates the cleanup process so you can focus on the actual content.

## License

MIT License - feel free to use, modify, and distribute. 