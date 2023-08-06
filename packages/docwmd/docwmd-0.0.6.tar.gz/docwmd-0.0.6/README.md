# Word Mover's Distance using Fast Word Mover's Distance

Calculates Word Mover's Distance using [Fast Word Mover's Distance](https://github.com/src-d/wmd-relax).

**Installation**

Before installing the package, check that you have already installed :
> [Numpy](https://pypi.org/project/numpy/)
>
> [wmd](https://pypi.org/project/wmd/)
>
> [NLTK](https://pypi.org/project/nltk/)
>
> [Spacy](https://pypi.org/project/spacy/)
>
> [en_core_web_lg](https://spacy.io/usage/models)

```
pip install numpy
pip install wmd
pip install nltk
pip install spacy
python -m spacy download en_core_web_lg
```

Then
```
pip install docwmd
```
Tested on Linux and macOS.

**Usage**

You must have the document you want to find the closest document as a string and the other documents as a list of strings.

```python
from docwmd import docWMD

calc = docWMD("Politician speaks to the media in Illinois.", ["The president greets the press in Chicago.", "The President delivers his inaugural address."])

print(calc.get_closest())
```

This returns the number of the nearest document and its distance.