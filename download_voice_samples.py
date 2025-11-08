"""
Download ALL voice samples from Chatterbox demo storage
1. Downloads ALL files to assets/downloads for manual review
2. Copies default male/female to reference_voices/[lang]/
3. Prioritizes .wav files to save storage space
"""

import requests
import xml.etree.ElementTree as ET
from pathlib import Path
import shutil

# Storage bucket URL
BUCKET_URL = "https://storage.googleapis.com/chatterbox-demo-samples"

# Folders
DOWNLOADS_FOLDER = Path("src/assets/downloads")
REFERENCE_FOLDER = Path("src/assets/reference_voices")

# Language codes supported (23 languages)
LANGUAGES = ['ar', 'da', 'de', 'el', 'en', 'es', 'fi', 'fr', 'he', 'hi', 'it', 'ja', 'ko', 'ms', 'nl', 'no', 'pl', 'pt', 'ru', 'sv', 'sw', 'tr', 'zh']

# Default male/female voice mapping for each language (using .wav for smaller size)
DEFAULT_VOICES = {
    'en': {'male': 'samples/duff_stewie.wav', 'female': 'samples/duff_nikole.wav'},
    'ar': {'male': 'mtl_samples23lang/ar/infer-00.wav', 'female': 'mtl_samples23lang_split/ar_f/infer-00.wav'},
    'da': {'male': 'mtl_samples23lang/da/infer-00.wav', 'female': 'mtl_samples23lang/da/infer-00.wav'},
    'de': {'male': 'mtl_samples23lang/de/infer-00.wav', 'female': 'mtl_samples23lang/de/infer-00.wav'},
    'el': {'male': 'mtl_samples23lang/el/infer-00.wav', 'female': 'mtl_samples23lang/el/infer-00.wav'},
    'es': {'male': 'mtl_samples23lang/es/infer-00.wav', 'female': 'mtl_samples23lang/es/infer-00.wav'},
    'fi': {'male': 'mtl_samples23lang/fi/infer-00.wav', 'female': 'mtl_samples23lang/fi/infer-00.wav'},
    'fr': {'male': 'mtl_samples23lang/fr/infer-00.wav', 'female': 'mtl_samples23lang/fr/infer-00.wav'},
    'he': {'male': 'mtl_samples23lang/he/infer-00.wav', 'female': 'mtl_samples23lang/he/infer-00.wav'},
    'hi': {'male': 'mtl_samples23lang/hi/infer-00.wav', 'female': 'mtl_samples23lang/hi/infer-00.wav'},
    'it': {'male': 'mtl_samples23lang/it/infer-00.wav', 'female': 'mtl_samples23lang/it/infer-00.wav'},
    'ja': {'male': 'mtl_samples23lang/ja/infer-00.wav', 'female': 'mtl_samples23lang/ja/infer-00.wav'},
    'ko': {'male': 'mtl_samples23lang/ko/infer-00.wav', 'female': 'mtl_samples23lang/ko/infer-00.wav'},
    'ms': {'male': 'mtl_samples23lang/ms/infer-00.wav', 'female': 'mtl_samples23lang/ms/infer-00.wav'},
    'nl': {'male': 'mtl_samples23lang/nl/infer-00.wav', 'female': 'mtl_samples23lang/nl/infer-00.wav'},
    'no': {'male': 'mtl_samples23lang/no/infer-00.wav', 'female': 'mtl_samples23lang/no/infer-00.wav'},
    'pl': {'male': 'mtl_samples23lang/pl/infer-00.wav', 'female': 'mtl_samples23lang/pl/infer-00.wav'},
    'pt': {'male': 'mtl_samples23lang/pt/infer-00.wav', 'female': 'mtl_samples23lang/pt/infer-00.wav'},
    'ru': {'male': 'mtl_samples23lang/ru/infer-00.wav', 'female': 'mtl_samples23lang/ru/infer-00.wav'},
    'sv': {'male': 'mtl_samples23lang/sv/infer-00.wav', 'female': 'mtl_samples23lang/sv/infer-00.wav'},
    'sw': {'male': 'mtl_samples23lang/sw/infer-00.wav', 'female': 'mtl_samples23lang/sw/infer-00.wav'},
    'tr': {'male': 'mtl_samples23lang/tr/infer-00.wav', 'female': 'mtl_samples23lang/tr/infer-00.wav'},
    'zh': {'male': 'mtl_samples23lang/zh/infer-00.wav', 'female': 'mtl_samples23lang/zh/infer-00.wav'}
}

def download_sample_voices():
    """
    1. Download ALL audio files to assets/downloads
    2. Copy default male/female to reference_voices/[lang]/
    """
    
    print("🔍 Fetching list of available voice samples...")
    
    # Get bucket listing
    response = requests.get(BUCKET_URL)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch bucket listing: {response.status_code}")
        return
    
    # Parse XML
    root = ET.fromstring(response.content)
    namespace = {'s3': 'http://doc.s3.amazonaws.com/2006-03-01'}
    
    # Find all audio files
    all_files = []
    for contents in root.findall('s3:Contents', namespace):
        key = contents.find('s3:Key', namespace)
        size = contents.find('s3:Size', namespace)
        
        if key is not None and size is not None:
            file_key = key.text
            file_size = int(size.text)
            
            # Skip folders and duet_prompts
            if file_size > 0 and not file_key.startswith('duet_prompts'):
                if file_key.endswith('.wav') or file_key.endswith('.flac'):
                    all_files.append((file_key, file_size))
    
    print(f"✅ Found {len(all_files)} audio files")
    
    # Step 1: Download ALL files to downloads folder
    print(f"\n📥 Step 1: Downloading ALL files to {DOWNLOADS_FOLDER}...")
    DOWNLOADS_FOLDER.mkdir(parents=True, exist_ok=True)
    
    downloaded_all = 0
    total_size = 0
    
    for file_key, file_size in all_files:
        # Preserve folder structure
        output_path = DOWNLOADS_FOLDER / file_key
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Skip if already exists
        if output_path.exists():
            continue
        
        file_url = f"{BUCKET_URL}/{file_key}"
        
        try:
            response = requests.get(file_url)
            if response.status_code == 200:
                output_path.write_bytes(response.content)
                downloaded_all += 1
                total_size += len(response.content)
                
                if downloaded_all % 10 == 0:
                    print(f"   Downloaded {downloaded_all} files... ({total_size / 1024 / 1024:.1f} MB)")
        except:
            pass  # Silently skip failed downloads
    
    print(f"✅ Downloaded {downloaded_all} files ({total_size / 1024 / 1024:.1f} MB)")
    
    # Step 2: Copy default male/female voices to reference_voices
    print(f"\n📋 Step 2: Setting up default voices in {REFERENCE_FOLDER}...")
    REFERENCE_FOLDER.mkdir(parents=True, exist_ok=True)
    
    copied_count = 0
    for lang_code, voices in DEFAULT_VOICES.items():
        lang_folder = REFERENCE_FOLDER / lang_code
        lang_folder.mkdir(parents=True, exist_ok=True)
        
        print(f"   {lang_code.upper()}:", end=" ")
        
        # Copy male voice
        if voices['male']:
            source_path = DOWNLOADS_FOLDER / voices['male']
            dest_path = lang_folder / "male_default.wav"
            
            if source_path.exists():
                shutil.copy2(source_path, dest_path)
                copied_count += 1
            else:
                print(f"⚠️ Male not found", end=" ")
        
        # Copy female voice
        if voices['female']:
            source_path = DOWNLOADS_FOLDER / voices['female']
            dest_path = lang_folder / "female_default.wav"
            
            if source_path.exists():
                shutil.copy2(source_path, dest_path)
                copied_count += 1
                print("✅")
            else:
                print(f"⚠️ Female not found")
    
    print(f"\n✅ Setup complete!")
    print(f"\n📂 Folder structure:")
    print(f"   {DOWNLOADS_FOLDER}/ - ALL downloaded files for manual review")
    print(f"   {REFERENCE_FOLDER}/ - Default voices organized by language:")
    
    for lang_code in sorted(DEFAULT_VOICES.keys()):
        lang_folder = REFERENCE_FOLDER / lang_code
        if lang_folder.exists():
            files = list(lang_folder.glob('*.wav')) + list(lang_folder.glob('*.flac'))
            print(f"     {lang_code}/ ({len(files)} files)")
    
    print("\n💡 Check downloads folder to find more voices to add manually!")
    print("💡 Copy desired voices to reference_voices/[lang]/ folder")

if __name__ == "__main__":
    download_sample_voices()
