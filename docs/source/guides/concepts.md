# Core Concepts

Tiny's senses are allowed to miss. An ear that invents a transcript poisons
the markdown cache. The only legal empty belief for Ear is `I did not catch words.`

| Field | Kind |
|---|---|
| `transcript` / `## Belief` | human words, or MISS |
| `pitch_mean_hz`, `energy`, F1/F2 | measurements |
| `class_manner`, `class_vowel` | inventory tag, not a word |

Ear is complete without Howl. The pipe exists so we can measure voiced /
F0-band / MISS accuracy against generated atoms.
