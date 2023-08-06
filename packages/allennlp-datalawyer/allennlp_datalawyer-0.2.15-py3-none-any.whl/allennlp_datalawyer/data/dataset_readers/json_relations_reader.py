import logging
import random

from itertools import combinations
from typing import Dict, List, Iterator, Any

from allennlp.data.dataset_readers.dataset_reader import DatasetReader
from allennlp.data.fields import TextField, SpanField, MetadataField, LabelField
from allennlp.data.instance import Instance
from allennlp.data.token_indexers import PretrainedTransformerIndexer, TokenIndexer

from allennlp_datalawyer.data.dataset_readers.base_json_reader import BaseJsonReader
from allennlp_datalawyer.data.dataset_readers.relations import Entity, Relation

logger = logging.getLogger(__name__)

valid_relations_mappings = {
    'PESSOA': ['FUNCAO'],
    'ORGANIZACAO': ['FUNCAO'],
    'PEDIDO': ['ATRIBUICAO', 'DECISAO', 'VALOR_PEDIDO'],
    'REFLEXO': ['ATRIBUICAO', 'DECISAO', 'VALOR_PEDIDO']
}


def get_relation_for_entities_pair(entity_1: Entity, entity_2: Entity, relations: List[Relation]) -> Relation:
    for _relation in relations:
        if _relation.matches_entities(entity_1, entity_2):
            return _relation
    return None


def is_relation_valid(entity_1: Entity, entity_2: Entity) -> bool:
    if entity_1.entity_type in valid_relations_mappings.keys():
        return entity_2.entity_type in valid_relations_mappings[entity_1.entity_type]
    return False


@DatasetReader.register("relations_reader")
class RelationsDatasetReader(BaseJsonReader):

    def __init__(self,
                 label_namespace: str = "labels",
                 max_negative_samples: int = 0,
                 max_negative_valid_samples: int = 0,
                 valid_relations_mapping: Dict[str, Any] = valid_relations_mappings,
                 token_indexers: Dict[str, TokenIndexer] = None,
                 random_seed: int = 13370,
                 **kwargs) -> None:
        super().__init__(token_indexers, **kwargs)

        self.no_relation_label = 'NO_RELATION'
        self.label_namespace = label_namespace
        self.max_negative_samples = max_negative_samples
        self.max_negative_valid_samples = max_negative_valid_samples
        self.valid_relations_mapping = valid_relations_mapping
        random.seed(random_seed)

    def _read(self, file_path: str) -> Iterator[Instance]:

        for sentence in self._load_sentences(file_path=file_path):
            context = [token.phrase for token in sentence.tokens]
            tokenized_context = self.tokenizer.tokenize(' '.join(context))

            if self.max_negative_samples > 0:
                # and all(
                # [suffix not in file_path for suffix in ['_dev.', '_test.', '_val.', '_valid.',
                #                                         '_dev_', '_test_', '_val_', '_valid_']]):

                negative_tuples = [(entity_1, entity_2) for entity_1, entity_2 in combinations(sentence.entities, 2)
                                   if
                                   get_relation_for_entities_pair(entity_1, entity_2, sentence.relations) is None]
                negative_valid_tuples = [negative_tuple for negative_tuple in negative_tuples if
                                         is_relation_valid(negative_tuple[0], negative_tuple[1])]
                negative_invalid_tuples = [negative_tuple for negative_tuple in negative_tuples if
                                           not is_relation_valid(negative_tuple[0], negative_tuple[1])]
                training_negative_valid_tuples = random.sample(negative_valid_tuples,
                                                               min(len(negative_valid_tuples),
                                                                   self.max_negative_valid_samples))
                training_negative_invalid_tuples = random.sample(negative_invalid_tuples,
                                                                 min(len(negative_invalid_tuples),
                                                                     self.max_negative_samples))

                for idx, (entity_1, entity_2) in enumerate(
                        training_negative_valid_tuples + training_negative_invalid_tuples):
                    sentence.relations.append(
                        Relation(rid=idx + len(sentence.relations),
                                 sentence_id=sentence.sentence_id,
                                 relation_type=self.no_relation_label,
                                 head_entity=entity_1, tail_entity=entity_2))

            for relation in sentence.relations:
                yield self.text_to_instance(context=context, relation=relation, tokenized_context=tokenized_context)

    def text_to_instance(self,
                         context: List[str],
                         relation: Relation,
                         tokenized_context: List[str]) -> Instance:
        fields = dict()

        if tokenized_context is None:
            tokenized_context = self.tokenizer.tokenize(' '.join(context))

        context_field = TextField(tokens=tokenized_context, token_indexers=self._token_indexers)
        fields["context"] = context_field

        fields["head"] = SpanField(span_start=relation.head_entity.span_start,
                                   span_end=relation.head_entity.span_end,
                                   sequence_field=context_field)
        # fields["head_entity"] = LabelField(label=relation.head_entity.entity_type,
        #                                    label_namespace="entities_labels")

        fields["tail"] = SpanField(span_start=relation.tail_entity.span_start,
                                   span_end=relation.tail_entity.span_end,
                                   sequence_field=context_field)
        # fields["tail_entity"] = LabelField(label=relation.tail_entity.entity_type,
        #                                    label_namespace="entities_labels")

        if relation.relation_type is not None:
            fields["labels"] = LabelField(label=relation.relation_type, label_namespace=self.label_namespace)

        # make the metadata
        fields["metadata"] = MetadataField(metadata={
            "relation": relation,
            "context": context,
            "context_tokens": tokenized_context
        })

        # fields["tokens"] = context_field
        #
        # fields["label"] = LabelField(label=relation.relation_type, label_namespace=self.label_namespace)

        return Instance(fields)
