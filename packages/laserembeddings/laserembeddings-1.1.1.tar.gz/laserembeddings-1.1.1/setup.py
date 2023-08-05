# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['laserembeddings']

package_data = \
{'': ['*'], 'laserembeddings': ['data/*']}

install_requires = \
['numpy>=1.15.4,<2.0.0',
 'sacremoses==0.0.35',
 'subword-nmt>=0.3.6,<0.4.0',
 'torch>=1.0.1.post2,<2.0.0',
 'transliterate==1.10.2']

extras_require = \
{u'ja': ['mecab-python3>=1.0.1,<2.0.0', 'ipadic==1.0.0'],
 u'zh': ['jieba>=0.42.1,<0.43.0']}

setup_kwargs = {
    'name': 'laserembeddings',
    'version': '1.1.1',
    'description': 'Production-ready LASER multilingual embeddings',
    'long_description': '# LASER embeddings\n\n[![Travis (.org) branch](https://img.shields.io/travis/yannvgn/laserembeddings/master?style=flat-square)](https://travis-ci.org/yannvgn/laserembeddings)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/laserembeddings?style=flat-square)\n[![PyPI](https://img.shields.io/pypi/v/laserembeddings.svg?style=flat-square)](https://pypi.org/project/laserembeddings/)\n[![PyPI - License](https://img.shields.io/pypi/l/laserembeddings.svg?style=flat-square)](https://github.com/yannvgn/laserembeddings/blob/master/LICENSE)\n\n**Out-of-the-box multilingual sentence embeddings.**\n\n![LASER embeddings maps similar sentences in any language to similar language-agnostic embeddings](https://raw.githubusercontent.com/yannvgn/laserembeddings/master/laserembeddings.gif)\n\nlaserembeddings is a pip-packaged, production-ready port of Facebook Research\'s [LASER](https://github.com/facebookresearch/LASER) (Language-Agnostic SEntence Representations) to compute multilingual sentence embeddings.\n\n**Have a look at the project\'s repo ([master branch](https://github.com/yannvgn/laserembeddings) or [this release](https://github.com/yannvgn/laserembeddings/tree/v1.1.1)) for the full documentation.**\n\n## Getting started\n\n### Prerequisites\n\nYou\'ll need Python 3.6+ and PyTorch. Please refer to [PyTorch installation instructions](https://pytorch.org/get-started/locally/).\n\n### Installation\n\n```\npip install laserembeddings\n```\n\n#### Chinese language\n\nChinese is not supported by default. If you need to embed Chinese sentences, please install laserembeddings with the "zh" extra. This extra includes [jieba](https://github.com/fxsjy/jieba).\n\n```\npip install laserembeddings[zh]\n```\n\n#### Japanese language\n\nJapanese is not supported by default. If you need to embed Japanese sentences, please install laserembeddings with the "ja" extra. This extra includes [mecab-python3](https://github.com/SamuraiT/mecab-python3) and the [ipadic](https://github.com/polm/ipadic-py) dictionary, which is used in the original LASER project.\n\nIf you have issues running laserembeddings on Japanese sentences, please refer to [mecab-python3 documentation](https://github.com/SamuraiT/mecab-python3) for troubleshooting.\n\n```\npip install laserembeddings[ja]\n```\n\n\n### Downloading the pre-trained models\n\n```\npython -m laserembeddings download-models\n```\n\nThis will download the models to the default `data` directory next to the source code of the package. Use `python -m laserembeddings download-models path/to/model/directory` to download the models to a specific location.\n\n### Usage\n\n```python\nfrom laserembeddings import Laser\n\nlaser = Laser()\n\n# if all sentences are in the same language:\n\nembeddings = laser.embed_sentences(\n    [\'let your neural network be polyglot\',\n     \'use multilingual embeddings!\'],\n    lang=\'en\')  # lang is only used for tokenization\n\n# embeddings is a N*1024 (N = number of sentences) NumPy array\n```\n\nIf the sentences are not in the same language, you can pass a list of language codes:\n```python\nembeddings = laser.embed_sentences(\n    [\'I love pasta.\',\n     "J\'adore les p\xc3\xa2tes.",\n     \'Ich liebe Pasta.\'],\n    lang=[\'en\', \'fr\', \'de\'])\n```\n\nIf you downloaded the models into a specific directory:\n\n```python\nfrom laserembeddings import Laser\n\npath_to_bpe_codes = ...\npath_to_bpe_vocab = ...\npath_to_encoder = ...\n\nlaser = Laser(path_to_bpe_codes, path_to_bpe_vocab, path_to_encoder)\n\n# you can also supply file objects instead of file paths\n```\n\nIf you want to pull the models from S3:\n\n```python\nfrom io import BytesIO, StringIO\nfrom laserembeddings import Laser\nimport boto3\n\ns3 = boto3.resource(\'s3\')\nMODELS_BUCKET = ...\n\nf_bpe_codes = StringIO(s3.Object(MODELS_BUCKET, \'path_to_bpe_codes.fcodes\').get()[\'Body\'].read().decode(\'utf-8\'))\nf_bpe_vocab = StringIO(s3.Object(MODELS_BUCKET, \'path_to_bpe_vocabulary.fvocab\').get()[\'Body\'].read().decode(\'utf-8\'))\nf_encoder = BytesIO(s3.Object(MODELS_BUCKET, \'path_to_encoder.pt\').get()[\'Body\'].read())\n\nlaser = Laser(f_bpe_codes, f_bpe_vocab, f_encoder)\n```\n',
    'author': 'yannvgn',
    'author_email': 'hi@yannvgn.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yannvgn/laserembeddings',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
