from functools import partial
from malaya.text.bpe import load_yttm
from malaya.stem import _classification_textcleaning_stemmer, naive
from malaya.function import check_file, load_graph, generate_session
from malaya.text.bpe import (
    sentencepiece_tokenizer_bert,
    sentencepiece_tokenizer_xlnet,
)
from malaya.path import PATH_TOXIC, S3_PATH_TOXIC
from malaya.model.ml import MultilabelBayes
from malaya.model.bert import SigmoidBERT
from malaya.model.xlnet import SigmoidXLNET
from herpetologist import check_type

label = [
    'severe toxic',
    'obscene',
    'identity attack',
    'insult',
    'threat',
    'asian',
    'atheist',
    'bisexual',
    'buddhist',
    'christian',
    'female',
    'heterosexual',
    'indian',
    'homosexual, gay or lesbian',
    'intellectual or learning disability',
    'male',
    'muslim',
    'other disability',
    'other gender',
    'other race or ethnicity',
    'other religion',
    'other sexual orientation',
    'physical disability',
    'psychiatric or mental illness',
    'transgender',
    'malay',
    'chinese',
]

_transformer_availability = {
    'bert': {
        'Size (MB)': 425.6,
        'Quantized Size (MB)': 111,
        'micro precision': 0.86098,
        'micro recall': 0.77313,
        'micro f1-score': 0.81469,
    },
    'tiny-bert': {
        'Size (MB)': 57.4,
        'Quantized Size (MB)': 15.4,
        'micro precision': 0.83535,
        'micro recall': 0.79611,
        'micro f1-score': 0.81526,
    },
    'albert': {
        'Size (MB)': 48.6,
        'Quantized Size (MB)': 12.8,
        'micro precision': 0.86054,
        'micro recall': 0.76973,
        'micro f1-score': 0.81261,
    },
    'tiny-albert': {
        'Size (MB)': 22.4,
        'Quantized Size (MB)': 5.98,
        'micro precision': 0.83535,
        'micro recall': 0.79611,
        'micro f1-score': 0.81526,
    },
    'xlnet': {
        'Size (MB)': 446.6,
        'Quantized Size (MB)': 118,
        'micro precision': 0.77904,
        'micro recall': 0.83829,
        'micro f1-score': 0.80758,
    },
    'alxlnet': {
        'Size (MB)': 46.8,
        'Quantized Size (MB)': 13.3,
        'micro precision': 0.83376,
        'micro recall': 0.80221,
        'micro f1-score': 0.81768,
    },
}


def available_transformer():
    """
    List available transformer toxicity analysis models.
    """
    from malaya.function import describe_availability

    return describe_availability(
        _transformer_availability, text = 'tested on 20% test set.'
    )


def multinomial(**kwargs):
    """
    Load multinomial toxicity model.

    Returns
    -------
    result : malaya.model.ml.MultilabelBayes class
    """
    import pickle

    check_file(
        PATH_TOXIC['multinomial'], S3_PATH_TOXIC['multinomial'], **kwargs
    )

    try:
        with open(PATH_TOXIC['multinomial']['model'], 'rb') as fopen:
            multinomial = pickle.load(fopen)
        with open(PATH_TOXIC['multinomial']['vector'], 'rb') as fopen:
            vectorize = pickle.load(fopen)
    except:
        raise Exception(
            f"model corrupted due to some reasons, please run `malaya.clear_cache('toxic/multinomial')` and try again."
        )

    stemmer = naive()
    cleaning = partial(_classification_textcleaning_stemmer, stemmer = stemmer)

    bpe, subword_mode = load_yttm(PATH_TOXIC['multinomial']['bpe'])

    return MultilabelBayes(
        multinomial = multinomial,
        label = label,
        vectorize = vectorize,
        bpe = bpe,
        subword_mode = subword_mode,
        cleaning = cleaning,
    )


@check_type
def transformer(model: str = 'xlnet', quantized: bool = False, **kwargs):
    """
    Load Transformer toxicity model.

    Parameters
    ----------
    model : str, optional (default='bert')
        Model architecture supported. Allowed values:

        * ``'bert'`` - Google BERT BASE parameters.
        * ``'tiny-bert'`` - Google BERT TINY parameters.
        * ``'albert'`` - Google ALBERT BASE parameters.
        * ``'tiny-albert'`` - Google ALBERT TINY parameters.
        * ``'xlnet'`` - Google XLNET BASE parameters.
        * ``'alxlnet'`` - Malaya ALXLNET BASE parameters.

    quantized : bool, optional (default=False)
        if True, will load 8-bit quantized model. 
        Quantized model not necessary faster, totally depends on the machine.

    Returns
    -------
    result : malaya.model.bert.SigmoidBERT class
    """

    model = model.lower()
    if model not in _transformer_availability:
        raise Exception(
            'model not supported, please check supported models from `malaya.toxicity.available_transformer()`.'
        )

    check_file(
        PATH_TOXIC[model], S3_PATH_TOXIC[model], quantized = quantized, **kwargs
    )
    if quantized:
        model_path = 'quantized'
    else:
        model_path = 'model'
    g = load_graph(PATH_TOXIC[model][model_path], **kwargs)

    path = PATH_TOXIC

    if model in ['albert', 'bert', 'tiny-albert', 'tiny-bert']:
        if model in ['bert', 'tiny-bert']:
            from malaya.transformers.bert import (
                _extract_attention_weights_import,
            )
            from malaya.transformers.bert import bert_num_layers

            tokenizer = sentencepiece_tokenizer_bert(
                path[model]['tokenizer'], path[model]['vocab']
            )
        if model in ['albert', 'tiny-albert']:
            from malaya.transformers.albert import (
                _extract_attention_weights_import,
            )
            from malaya.transformers.albert import bert_num_layers
            from albert import tokenization

            tokenizer = tokenization.FullTokenizer(
                vocab_file = path[model]['vocab'],
                do_lower_case = False,
                spm_model_file = path[model]['tokenizer'],
            )

        return SigmoidBERT(
            X = g.get_tensor_by_name('import/Placeholder:0'),
            segment_ids = None,
            input_masks = g.get_tensor_by_name('import/Placeholder_1:0'),
            logits = g.get_tensor_by_name('import/logits:0'),
            logits_seq = g.get_tensor_by_name('import/logits_seq:0'),
            vectorizer = g.get_tensor_by_name('import/dense/BiasAdd:0'),
            sess = generate_session(graph = g, **kwargs),
            tokenizer = tokenizer,
            label = label,
            attns = _extract_attention_weights_import(
                bert_num_layers[model], g
            ),
            class_name = 'toxic',
        )

    if model in ['xlnet', 'alxlnet']:
        if model in ['xlnet']:
            from malaya.transformers.xlnet import (
                _extract_attention_weights_import,
            )
        if model in ['alxlnet']:
            from malaya.transformers.alxlnet import (
                _extract_attention_weights_import,
            )

        tokenizer = sentencepiece_tokenizer_xlnet(path[model]['tokenizer'])

        return SigmoidXLNET(
            X = g.get_tensor_by_name('import/Placeholder:0'),
            segment_ids = g.get_tensor_by_name('import/Placeholder_1:0'),
            input_masks = g.get_tensor_by_name('import/Placeholder_2:0'),
            logits = g.get_tensor_by_name('import/logits:0'),
            logits_seq = g.get_tensor_by_name('import/logits_seq:0'),
            vectorizer = g.get_tensor_by_name('import/transpose_3:0'),
            sess = generate_session(graph = g, **kwargs),
            tokenizer = tokenizer,
            label = label,
            attns = _extract_attention_weights_import(g),
            class_name = 'toxic',
        )
