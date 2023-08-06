import json
from malaya.function import check_file, load_graph, generate_session
from malaya.text.bpe import (
    sentencepiece_tokenizer_bert,
    sentencepiece_tokenizer_xlnet,
)
from malaya.model.bert import TaggingBERT
from malaya.model.xlnet import TaggingXLNET


def transformer(
    path, s3_path, class_name, model = 'xlnet', quantized = False, **kwargs
):
    check_file(path[model], s3_path[model], quantized = quantized, **kwargs)
    if quantized:
        model_path = 'quantized'
    else:
        model_path = 'model'
    g = load_graph(path[model][model_path], **kwargs)

    try:
        with open(path[model]['setting']) as fopen:
            nodes = json.load(fopen)
    except:
        raise Exception(
            f"model corrupted due to some reasons, please run malaya.clear_cache('{class_name}/{model}/{size}') and try again"
        )

    if model in ['albert', 'bert', 'tiny-albert', 'tiny-bert']:
        if model in ['bert', 'tiny-bert']:
            tokenizer = sentencepiece_tokenizer_bert(
                path[model]['tokenizer'], path[model]['vocab']
            )

        if model in ['albert', 'tiny-albert']:
            from albert import tokenization

            tokenizer = tokenization.FullTokenizer(
                vocab_file = path[model]['vocab'],
                do_lower_case = False,
                spm_model_file = path[model]['tokenizer'],
            )

        return TaggingBERT(
            X = g.get_tensor_by_name('import/Placeholder:0'),
            segment_ids = None,
            input_masks = g.get_tensor_by_name('import/Placeholder_1:0'),
            logits = g.get_tensor_by_name('import/logits:0'),
            vectorizer = g.get_tensor_by_name('import/dense/BiasAdd:0'),
            sess = generate_session(graph = g, **kwargs),
            tokenizer = tokenizer,
            settings = nodes,
        )

    if model in ['xlnet', 'alxlnet']:
        tokenizer = sentencepiece_tokenizer_xlnet(path[model]['tokenizer'])
        return TaggingXLNET(
            X = g.get_tensor_by_name('import/Placeholder:0'),
            segment_ids = g.get_tensor_by_name('import/Placeholder_1:0'),
            input_masks = g.get_tensor_by_name('import/Placeholder_2:0'),
            logits = g.get_tensor_by_name('import/logits:0'),
            vectorizer = g.get_tensor_by_name('import/transpose_3:0'),
            sess = generate_session(graph = g, **kwargs),
            tokenizer = tokenizer,
            settings = nodes,
        )
