# Architecture

```{mermaid}
flowchart LR
    WAV[WAV / stdin] --> Ingest[ingest]
    Ingest --> Pair["stem.ear.wav + stem.ear.md"]
    Ingest --> Class[classify_pcm]
    Class --> Goertzel[F1 / F2 bins]
    Pair --> Tiny["/tiny/ear/"]
```
