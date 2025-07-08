#!/usr/bin/env python3
"""
Transcript Cleaner Script

This script processes raw HTML transcript files and extracts clean dialogue
organized by speaker. It handles the TLDV transcript format and outputs
clean text files.

Simple folder structure:
- input/     : Put all your .raw files here
- output/    : Cleaned transcripts will be saved here

Usage:
    python3 transcript_cleaner.py
"""

import os
import re
import html
from pathlib import Path
from typing import List, Dict, Tuple
import argparse
from datetime import datetime


class TranscriptCleaner:
    def __init__(self, input_dir: str = "input", output_dir: str = "output"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def extract_speaker_and_text(self, html_content: str) -> List[Tuple[str, str]]:
        """
        Extract speaker names and their dialogue from HTML content.
        
        Args:
            html_content: Raw HTML string from transcript file
            
        Returns:
            List of tuples containing (speaker_name, dialogue_text)
        """
        transcript = []
        
        # Find all paragraph tags that contain speaker information
        # Pattern to match <p> tags with data-index attribute
        paragraph_pattern = r'<p[^>]*data-index="[^"]*"[^>]*>(.*?)</p>'
        
        paragraphs = re.findall(paragraph_pattern, html_content, re.DOTALL)
        
        for paragraph in paragraphs:
            # Extract speaker name from the paragraph
            speaker_match = re.search(r'<span[^>]*data-speaker="true"[^>]*>.*?<span>([^<]+)</span>', paragraph, re.DOTALL)
            
            if speaker_match:
                speaker_name = speaker_match.group(1).strip()
                
                # Extract all dialogue text from spans with data-clipped attribute
                # Look for spans that contain dialogue (not speaker info)
                dialogue_spans = re.findall(r'<span[^>]*data-clipped="[^"]*"[^>]*data-speaker="false"[^>]*>([^<]+)</span>', paragraph)
                
                if dialogue_spans:
                    # Join all dialogue words together with proper spacing
                    dialogue_text = ' '.join(dialogue_spans)
                    transcript.append((speaker_name, dialogue_text))
        
        return transcript
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text content.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        # Decode HTML entities
        text = html.unescape(text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Clean up punctuation
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        
        # Remove any remaining HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        return text.strip()
    
    def organize_by_speaker(self, transcript: List[Tuple[str, str]]) -> Dict[str, List[str]]:
        """
        Organize transcript by speaker.
        
        Args:
            transcript: List of (speaker, dialogue) tuples
            
        Returns:
            Dictionary with speaker names as keys and lists of dialogue as values
        """
        speakers = {}
        
        for speaker, dialogue in transcript:
            cleaned_dialogue = self.clean_text(dialogue)
            if cleaned_dialogue:
                if speaker not in speakers:
                    speakers[speaker] = []
                speakers[speaker].append(cleaned_dialogue)
        
        return speakers
    
    def format_output(self, speakers: Dict[str, List[str]], filename: str) -> str:
        """
        Format the cleaned transcript for output.
        
        Args:
            speakers: Dictionary of speakers and their dialogue
            filename: Original filename for header
            
        Returns:
            Formatted transcript text
        """
        output_lines = []
        
        # Header
        output_lines.append(f"TRANSCRIPT: {filename}")
        output_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output_lines.append("=" * 80)
        output_lines.append("")
        
        # Process each speaker
        for speaker, dialogues in speakers.items():
            output_lines.append(f"SPEAKER: {speaker}")
            output_lines.append("-" * 40)
            
            for i, dialogue in enumerate(dialogues, 1):
                # Clean up the dialogue text
                cleaned_dialogue = self.clean_text(dialogue)
                if cleaned_dialogue:
                    output_lines.append(f"{i}. {cleaned_dialogue}")
            
            output_lines.append("")
        
        return "\n".join(output_lines)
    
    def format_chronological_output(self, transcript: List[Tuple[str, str]], filename: str) -> str:
        """
        Format the transcript in chronological order showing conversation flow.
        
        Args:
            transcript: List of (speaker, dialogue) tuples in order
            filename: Original filename for header
            
        Returns:
            Formatted chronological transcript text
        """
        output_lines = []
        
        # Header
        output_lines.append(f"TRANSCRIPT (CHRONOLOGICAL): {filename}")
        output_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output_lines.append("=" * 80)
        output_lines.append("")
        
        # Process each dialogue entry in order
        for i, (speaker, dialogue) in enumerate(transcript, 1):
            cleaned_dialogue = self.clean_text(dialogue)
            if cleaned_dialogue:
                output_lines.append(f"{i}. {speaker}: {cleaned_dialogue}")
                output_lines.append("")
        
        return "\n".join(output_lines)

    def process_file(self, file_path: Path) -> bool:
        """
        Process a single transcript file.
        
        Args:
            file_path: Path to the raw transcript file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Processing: {file_path.name}")
            
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract speaker and dialogue
            transcript = self.extract_speaker_and_text(content)
            
            if not transcript:
                print(f"  Warning: No transcript data found in {file_path.name}")
                return False
            
            # Organize by speaker
            speakers = self.organize_by_speaker(transcript)
            
            if not speakers:
                print(f"  Warning: No valid speakers found in {file_path.name}")
                return False
            
            # Format output (by speaker)
            output_text = self.format_output(speakers, file_path.name)
            
            # Create output filename
            output_filename = file_path.stem + "_by_speaker.txt"
            output_path = self.output_dir / output_filename
            
            # Write output
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output_text)
            
            # Also create chronological format
            chronological_text = self.format_chronological_output(transcript, file_path.name)
            chronological_filename = file_path.stem + "_chronological.txt"
            chronological_path = self.output_dir / chronological_filename
            
            with open(chronological_path, 'w', encoding='utf-8') as f:
                f.write(chronological_text)
            
            print(f"  ✓ Created: {output_path.name}")
            print(f"  ✓ Created: {chronological_path.name}")
            print(f"  Speakers found: {', '.join(speakers.keys())}")
            
            return True
            
        except Exception as e:
            print(f"  ✗ Error processing {file_path.name}: {str(e)}")
            return False
    
    def process_all_files(self) -> None:
        """
        Process all .raw files in the input directory, skipping example files.
        """
        raw_files = [f for f in self.input_dir.glob("*.raw") if f.name != "example-meeting.raw"]
        
        if not raw_files:
            print(f"No .raw files found in {self.input_dir} (excluding example files)")
            return
        
        print(f"Found {len(raw_files)} transcript file(s) to process (excluding example files)")
        print(f"Input directory: {self.input_dir}")
        print(f"Output directory: {self.output_dir}")
        print("-" * 60)
        
        successful = 0
        failed = 0
        
        for file_path in raw_files:
            if self.process_file(file_path):
                successful += 1
            else:
                failed += 1
            print()
        
        print("-" * 60)
        print(f"Processing complete!")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Output files saved to: {self.output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Clean and organize transcript files")
    parser.add_argument("--input", "-i", default="input", 
                       help="Input directory containing .raw files (default: input)")
    parser.add_argument("--output", "-o", default="output",
                       help="Output directory for cleaned files (default: output)")
    
    args = parser.parse_args()
    
    cleaner = TranscriptCleaner(args.input, args.output)
    cleaner.process_all_files()


if __name__ == "__main__":
    main() 