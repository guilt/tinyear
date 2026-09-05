# How-To: Classify

```python
from tinyear import classify_pcm
klass = classify_pcm(samples, 16000)
print(klass.manner, klass.vowel, klass.place, klass.ok)
```
