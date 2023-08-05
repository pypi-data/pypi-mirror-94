# LASER embeddings

[![Travis (.org) branch](https://img.shields.io/travis/yannvgn/laserembeddings/master?style=flat-square)](https://travis-ci.org/yannvgn/laserembeddings)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/laserembeddings?style=flat-square)
[![PyPI](https://img.shields.io/pypi/v/laserembeddings.svg?style=flat-square)](https://pypi.org/project/laserembeddings/)
[![PyPI - License](https://img.shields.io/pypi/l/laserembeddings.svg?style=flat-square)](https://github.com/yannvgn/laserembeddings/blob/master/LICENSE)

**Out-of-the-box multilingual sentence embeddings.**

![LASER embeddings maps similar sentences in any language to similar language-agnostic embeddings](https://raw.githubusercontent.com/yannvgn/laserembeddings/master/laserembeddings.gif)

laserembeddings is a pip-packaged, production-ready port of Facebook Research's [LASER](https://github.com/facebookresearch/LASER) (Language-Agnostic SEntence Representations) to compute multilingual sentence embeddings.

**Have a look at the project's repo ([master branch](https://github.com/yannvgn/laserembeddings) or [this release](https://github.com/yannvgn/laserembeddings/tree/v1.1.1)) for the full documentation.**

## Getting started

### Prerequisites

You'll need Python 3.6+ and PyTorch. Please refer to [PyTorch installation instructions](https://pytorch.org/get-started/locally/).

### Installation

```
pip install laserembeddings
```

#### Chinese language

Chinese is not supported by default. If you need to embed Chinese sentences, please install laserembeddings with the "zh" extra. This extra includes [jieba](https://github.com/fxsjy/jieba).

```
pip install laserembeddings[zh]
```

#### Japanese language

Japanese is not supported by default. If you need to embed Japanese sentences, please install laserembeddings with the "ja" extra. This extra includes [mecab-python3](https://github.com/SamuraiT/mecab-python3) and the [ipadic](https://github.com/polm/ipadic-py) dictionary, which is used in the original LASER project.

If you have issues running laserembeddings on Japanese sentences, please refer to [mecab-python3 documentation](https://github.com/SamuraiT/mecab-python3) for troubleshooting.

```
pip install laserembeddings[ja]
```


### Downloading the pre-trained models

```
python -m laserembeddings download-models
```

This will download the models to the default `data` directory next to the source code of the package. Use `python -m laserembeddings download-models path/to/model/directory` to download the models to a specific location.

### Usage

```python
from laserembeddings import Laser

laser = Laser()

# if all sentences are in the same language:

embeddings = laser.embed_sentences(
    ['let your neural network be polyglot',
     'use multilingual embeddings!'],
    lang='en')  # lang is only used for tokenization

# embeddings is a N*1024 (N = number of sentences) NumPy array
```

If the sentences are not in the same language, you can pass a list of language codes:
```python
embeddings = laser.embed_sentences(
    ['I love pasta.',
     "J'adore les pâtes.",
     'Ich liebe Pasta.'],
    lang=['en', 'fr', 'de'])
```

If you downloaded the models into a specific directory:

```python
from laserembeddings import Laser

path_to_bpe_codes = ...
path_to_bpe_vocab = ...
path_to_encoder = ...

laser = Laser(path_to_bpe_codes, path_to_bpe_vocab, path_to_encoder)

# you can also supply file objects instead of file paths
```

If you want to pull the models from S3:

```python
from io import BytesIO, StringIO
from laserembeddings import Laser
import boto3

s3 = boto3.resource('s3')
MODELS_BUCKET = ...

f_bpe_codes = StringIO(s3.Object(MODELS_BUCKET, 'path_to_bpe_codes.fcodes').get()['Body'].read().decode('utf-8'))
f_bpe_vocab = StringIO(s3.Object(MODELS_BUCKET, 'path_to_bpe_vocabulary.fvocab').get()['Body'].read().decode('utf-8'))
f_encoder = BytesIO(s3.Object(MODELS_BUCKET, 'path_to_encoder.pt').get()['Body'].read())

laser = Laser(f_bpe_codes, f_bpe_vocab, f_encoder)
```
