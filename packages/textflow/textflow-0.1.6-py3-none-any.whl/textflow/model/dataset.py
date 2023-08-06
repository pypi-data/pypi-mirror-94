""" Base class and in-built dataset types. """

from textflow.utils.text import Tokenizer
from textflow.utils import Dictionary as Map, PluginManager

__all__ = [
    'Dataset',
    'datasets',
    'MultiLabelDataset',
    'SequenceLabelingDataset',
]

datasets = PluginManager()


class Dataset:
    def __init__(self, annotation_sets, tokenizer=None):
        self.records = self.build_dataset(annotation_sets, tokenizer=tokenizer)

    def build_dataset(self, annotation_sets, tokenizer):
        """Builds dataset from provided annotation sets

        :param annotation_sets: an iterable of annotation sets
        :param tokenizer: tokenizer function that returns (start, end, token string) of
        :return: records in dataset with labels by each annotator
        """
        raise NotImplementedError

    def build_item_tuples(self):
        """Make item tuples for annotation agreement

        :return: label item tuples
        """
        raise NotImplementedError

    @property
    def classes_(self):
        """List all classes of dataset if defined else return None

        :return: list of unique classes
        """
        return None

    @property
    def X(self):
        """Gets feature/independent variable of dataset

        :return: an iterable of feature/independent variable
        """
        raise NotImplementedError

    @property
    def y(self):
        """Gets target/dependent variable of dataset

        :return: an iterable of target/dependent variable
        """
        raise NotImplementedError


@datasets.register('sequence_labeling')
class SequenceLabelingDataset(Dataset):
    def build_dataset(self, annotation_sets, tokenizer=None):
        """Builds dataset from provided annotation sets

        :param annotation_sets: an iterable of annotation sets
        :param tokenizer: tokenizer function that returns (start, end, token string) of
        :return: records in dataset with labels by each annotator
        """
        if tokenizer is None:
            tokenizer = Tokenizer()
        records = dict()
        for annotation_set in annotation_sets:
            document = annotation_set.document
            if document.id in records:
                document = records[document.id]
            else:
                document = Map(
                    id=document.id,
                    id_str=document.id_str,
                    text=document.text,
                    tokens=tokenizer.tokenize(document.text),
                    labels=dict(),
                )
            # --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
            # set labels
            token_index = {}
            for tid, (s, e, _) in enumerate(document.tokens):
                for i in range(s, e):
                    token_index[i] = tid
            user = annotation_set.user
            if '__{}__'.format(user.username) in document.labels:
                labels = document.labels['__{}__'.format(user.username)]
            else:
                labels = [None for _ in document.tokens]
            for annotation in annotation_set.annotations:
                label_value = annotation.label.value
                annotation_span = annotation.span
                for tix in range(annotation_span.start,
                                 annotation_span.start + annotation_span.length):
                    if tix in token_index:
                        labels[token_index[tix]] = label_value
            document.labels['__{}__'.format(user.username)] = labels
            # --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
            records[document.id] = document
        for i in records:
            labels = records[i].labels.values()
            majority_vote = [sorted([(x, ll.count(x)) for x in set(ll)], key=lambda x: x[1])[-1][0] for ll in
                             zip(*labels)]
            records[i].labels['MAJORITY'] = majority_vote
        return records

    def build_item_tuples(self):
        """Make item tuples for annotation agreement

        :return: label item tuples
        """
        result = []
        for d in self.records.values():
            for coder, labels in d.labels.items():
                for index, (label, (_, _, token)) in enumerate(zip(labels, d.tokens)):
                    result.append((coder, '{}_{}'.format(d.id, index), label))
        return result

    @property
    def classes_(self):
        label_set = set()
        for d in self.records.values():
            for _, labels in d.labels.items():
                label_set.update(labels)
        return label_set

    @property
    def X(self):
        """Gets tokens for each sentence

        :return: list of tokens for each sentence
        """
        # select third position in tokens (i.e. index 2) to get string token
        # token tuple struct (start, end, token)
        X = [list(zip(*self.records[r].tokens))[2] for r in self.records]
        return X

    @staticmethod
    def _format_labels(tags):
        """Format labels by converting None to 'O'.

        :param tags: list of tags
        :return: formatted list of tags
        """
        return ['O' if t is None else t for t in tags]

    @property
    def y(self):
        """Gets (multi-class) labels for each token of each sentence

        :return: list of labels for each token of each sentence
        """
        X = [self._format_labels(self.records[r].labels['MAJORITY']) for r in self.records]
        return X


@datasets.register('classification')
class MultiLabelDataset(Dataset):
    def build_dataset(self, annotation_sets, tokenizer=None):
        """Builds dataset from provided annotation sets

        :param annotation_sets: an iterable of annotation sets
        :param tokenizer: tokenizer function that returns (start, end, token string) of
        :return: records in dataset with labels by each annotator
        """
        if tokenizer is None:
            tokenizer = Tokenizer()
        records = dict()
        for annotation_set in annotation_sets:
            document = annotation_set.document
            if document.id in records:
                document = records[document.id]
            else:
                document = Map(
                    id=document.id,
                    id_str=document.id_str,
                    text=document.text,
                    tokens=tokenizer.tokenize(document.text),
                    labels=dict(),
                )
            # --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
            # set labels
            user = annotation_set.user
            if '__{}__'.format(user.username) in document.labels:
                labels = document.labels['__{}__'.format(user.username)]
            else:
                labels = []
            for annotation in annotation_set.annotations:
                label_value = annotation.label.value
                labels.append(label_value)
            document.labels['__{}__'.format(user.username)] = labels
            # --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
            records[document.id] = document
        for i in records:
            labels = records[i].labels.values()
            min_num = int((len(labels)) / 2)
            label_counts = {}
            for ls in labels:
                for ll in set(ls):
                    if ll not in label_counts:
                        label_counts[ll] = 0
                    label_counts[ll] += 1
            majority_vote = [k for k, v in label_counts.items() if v > min_num]
            records[i].labels['MAJORITY'] = majority_vote
        return records

    def build_item_tuples(self):
        """Make item tuples for annotation agreement

        :return: label item tuples
        """
        result = []
        label_set = self.classes_
        for d in self.records.values():
            for coder, labels in d.labels.items():
                for label in label_set:
                    result.append((coder, '{}_{}'.format(d.id, label), str(label in labels)))
        return result

    @property
    def classes_(self):
        label_set = set()
        for d in self.records.values():
            for _, labels in d.labels.items():
                label_set.update(labels)
        return label_set

    @property
    def X(self):
        """Gets tokens for each sentence

        :return: list of tokens for each sentence
        """
        X = [self.records[r].text for r in self.records]
        return X

    @property
    def y(self):
        """Gets (multi-) label each sentence

        :return: list of labels of each document
        """
        y = [self.records[r].labels['MAJORITY'] for r in self.records]
        return y
