# Sentence Mover's Distance using Sentence Transformers Package

Calculates Sentence Mover's Distance using [Fast Word Mover's Distance](https://github.com/src-d/wmd-relax) and the embeddings provided by Sentence Transformers.

**Installation**

Before installing the package, check that you have already installed :
> [Numpy](https://pypi.org/project/numpy/)
>
> [Sentence Transformers](https://pypi.org/project/sentence-transformers/)
>
> [wmd](https://pypi.org/project/wmd/)

Then
```
pip install stsmd
```
Tested on Linux and macOS.

**Usage**

You must have the document you want to find the closest document as a string and the other documents as a list of strings.

```python
from stsmd import SMD

calc = SMD("Politician speaks to the media in Illinois.", ["The president greets the press in Chicago.", "The President delivers his inaugural address."])

print(calc.get_closest())
```

This returns the number of the nearest document and its distance.