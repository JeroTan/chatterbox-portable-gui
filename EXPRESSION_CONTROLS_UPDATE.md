# Expression Controls Update

## Changes Made

### Updated Expression Controls (`src/components/expression_controls.py`)

**Previous Issues:**
- Had 5 parameters: emotion, energy, speed, pitch, emphasis
- Only 2 parameters (energy, emphasis) were actually working
- Speed, pitch, and emotion were collected but never used by the TTS API
- No input boxes for direct value entry
- No reset buttons
- Incorrect parameter ranges

**New Implementation:**
Now properly aligned with Chatterbox TTS API documentation with intuitive semantic mapping:

1. **Energy (Expressiveness)** → maps to `exaggeration` parameter
   - Range: 0.25 - 2.0
   - Default: 0.70 (official Chatterbox default)
   - Tooltip guide:
     - 0.3-0.4: Very neutral
     - 0.5: Balanced
     - 0.7: Default (expressive)
     - 1.0+: Very dramatic

2. **Speed (Speech Rate)** → maps to `cfg_weight` parameter
   - Range: 0.01 - 1.0
   - Default: 0.40 (official Chatterbox default)
   - Tooltip guide:
     - 0.2-0.3: Faster speech
     - 0.4: Default
     - 0.5: Normal
     - 0.7-0.9: Slower, deliberate
   - **Semantic alignment**: Lower values = faster, higher values = slower

3. **Emphasis (Variation)** → maps to `temperature` parameter
   - Range: 0.05 - 5.0
   - Default: 0.90 (official Chatterbox default)
   - Tooltip guide:
     - 0.4-0.6: Consistent tone
     - 0.9: Default (varied)
     - 1.0+: Variable emphasis
   - **Controls variation/emphasis in delivery**

4. **Pitch (Semitones)** → post-processing pitch shift with Parselmouth (Praat)
   - Range: -12 to +12 semitones
   - Default: 0 (no change)
   - Tooltip guide:
     - -12 to -6: Lower pitch
     - 0: No change
     - +6 to +12: Higher pitch
     - Uses Praat for natural formant preservation
     - Best quality within ±6 semitones
   - **Applied after generation using Parselmouth library**
   - **Automatic fallback to librosa if Parselmouth unavailable**

**New UI Features:**
- ✅ Input boxes next to sliders for direct value entry
- ✅ Reset buttons (↻) to restore default values
- ✅ Tooltips explaining parameter effects
- ✅ 2 decimal precision for float values, 0 decimals for pitch
- ✅ Real-time sync between sliders and input boxes
- ✅ Value clamping to valid ranges

**Removed Parameters:**
- ❌ Emotion dropdown (not supported by Chatterbox TTS API)

### Updated TTS Generation (`src/features/generate.py`)

**Changes:**
1. **Corrected parameter mapping (SEMANTIC ALIGNMENT):**
   - Energy: maps to `exaggeration` (0.25-2.0) - expressiveness
   - **Speed: maps to `cfg_weight` (0.01-1.0) - speech rate (lower=faster, higher=slower)**
   - **Emphasis: maps to `temperature` (0.05-5.0) - variation in delivery**
   - Pitch: post-processing with `torchaudio.functional.pitch_shift`

2. **Added pitch shifting post-processing with Parselmouth (Praat):**
   - Uses professional phonetics software for natural voice manipulation
   - Preserves formants to prevent robotic sound
   - Applied after TTS generation
   - Converts semitones to frequency ratio: 2^(n/12)
   - Only applied if pitch_shift != 0
   - Progress callback shows pitch shift status
   - Automatic fallback to librosa if Parselmouth unavailable

3. **Added smooth progress bar animation:**
   - Exponential decay formula: new = current + (remaining / 16)
   - Updates every 1 second for fluid animation
   - Intelligent phasing: 30%→50%→85%→99%
   - Long generation warning after 30 seconds

3. **Updated debug output:**
   - Shows all 3 TTS parameters: exaggeration, cfg_weight, temperature
   - Shows pitch shift value when applied

## Chatterbox TTS API Reference

According to the official documentation (https://chatterboxtts.com/docs/api-readme):

```python
wav = model.generate(
    text,
    audio_prompt_path=audio_prompt_path,
    exaggeration=0.7,      # 0.25-2.0: Expressiveness level → Energy (default: 0.7)
    cfg_weight=0.4,        # 0.01-1.0: Speech rate (lower=faster) → Speed (default: 0.4)
    temperature=0.9        # 0.05-5.0: Variation/emphasis → Emphasis (default: 0.9)
)

# Post-processing pitch shift with Parselmouth (Praat)
if pitch_shift != 0:
    import parselmouth
    from parselmouth.praat import call
    
    sound = parselmouth.Sound(wav, sampling_frequency=sample_rate)
    pitch_factor = 2 ** (pitch_shift / 12.0)
    manipulation = call(sound, "To Manipulation", 0.01, 75, 600)
    pitch_tier = call(manipulation, "Extract pitch tier")
    call(pitch_tier, "Multiply frequencies", sound.xmin, sound.xmax, pitch_factor)
    call([pitch_tier, manipulation], "Replace pitch tier")
    wav = call(manipulation, "Get resynthesis (overlap-add)")
```

## Semantic Alignment Rationale

The parameter naming now makes intuitive sense:

- **Energy** controls how expressive/exaggerated the speech is ✓
- **Speed** controls how fast or slow the speech is (cfg_weight) ✓
- **Emphasis** controls variation and emphasis in delivery (temperature) ✓
- **Pitch** shifts the pitch up or down after generation ✓

Previously, "Speed" was mapped to `temperature` and "Emphasis" to `cfg_weight`, which was semantically backwards!

## Testing the Update

1. Launch the application
2. Navigate to expression controls
3. Try adjusting each parameter:
   - **Energy**: Notice expressiveness changes
   - **Speed**: Notice speech rate changes (lower=faster, higher=slower)
   - **Emphasis**: Notice variation in delivery
   - **Pitch**: Notice pitch shift up/down
4. Use sliders, input boxes, and reset buttons
5. Hover over labels for tooltips
6. Generate audio and verify all 4 parameters affect the output correctly

## Migration Notes

**For existing saved configurations:**
- Old configurations will use updated default values
- Energy values reset to 0.70 (official default)
- Speed values reset to 0.40 (official default)
- Emphasis values reset to 0.90 (official default)
- Pitch values default to 0 (no shift)

This is intentional to align with official Chatterbox TTS defaults.

## Recent Improvements (November 8, 2025)

### Parselmouth Integration
- Replaced simple pitch shifting with professional Praat algorithms
- Natural formant preservation prevents robotic sound
- Research-grade phonetics processing
- Automatic fallback to librosa for compatibility

### Progress Bar Enhancement
- Smooth exponential decay animation (divide by 16)
- Real-time updates every 1 second
- Intelligent phasing system
- Long generation warnings

---
**Date:** November 8, 2025
**Version:** 2.0 - Professional pitch shifting with Parselmouth + smooth progress animation
