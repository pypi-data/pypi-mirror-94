"""Test of the Alignment class pygamma_agreement.alignment"""

import numpy as np
import pytest
from pyannote.core import Annotation, Segment

from pygamma_agreement.alignment import SetPartitionError
from pygamma_agreement.alignment import UnitaryAlignment, Alignment
from pygamma_agreement.continuum import Continuum, Unit
from pygamma_agreement.dissimilarity import CombinedCategoricalDissimilarity


def test_alignment_checking():
    continuum = Continuum()
    annotation = Annotation()
    annotation[Segment(1, 5)] = 'Carol'
    annotation[Segment(6, 8)] = 'Bob'
    continuum.add_annotation('liza', annotation)

    annotation = Annotation()
    annotation[Segment(2, 6)] = 'Carol'
    continuum.add_annotation('pierrot', annotation)

    # checking valid alignment
    alignment = Alignment([], continuum=continuum)

    n_tuple = (('liza', Unit(Segment(1, 5), 'Carol')),
               ('pierrot', Unit(Segment(2, 6), 'Carol'))
               )
    unitary_alignment = UnitaryAlignment(n_tuple)
    alignment.unitary_alignments.append(unitary_alignment)

    # checking missing
    with pytest.raises(SetPartitionError):
        alignment.check(continuum)

    n_tuple = (('liza', Unit(Segment(6, 8), 'Bob')),
               ('pierrot', None)
               )
    unitary_alignment = UnitaryAlignment(n_tuple)
    alignment.unitary_alignments.append(unitary_alignment)

    # checking valid alignment
    alignment.check(continuum)

    # checking with extra tuple
    n_tuple = (('liza', Unit(Segment(6, 8), 'Bob')),
               ('pierrot', None)
               )
    unitary_alignment = UnitaryAlignment(n_tuple)
    alignment.unitary_alignments.append(unitary_alignment)

    # checking missing
    with pytest.raises(SetPartitionError):
        alignment.check(continuum)

def test_unitary_alignment():
    categories = ['Carol', 'Bob', 'Alice', 'Jeremy']
    cat = np.array([[0, 0.5, 0.3, 0.7],
                    [0.5, 0., 0.6, 0.4],
                    [0.3, 0.6, 0., 0.7],
                    [0.7, 0.4, 0.7, 0.]])
    combi_dis = CombinedCategoricalDissimilarity(
        categories=categories,
        delta_empty=0.5,
        cat_dissimilarity_matrix=cat,
        alpha=1)
    n_tuple = (('liza', Unit(Segment(12, 18), "Carol")),
               ('pierrot', Unit(Segment(12, 18), "Alice")),
               ('hadrien', None))
    unitary_alignment = UnitaryAlignment(n_tuple)

    assert (unitary_alignment.compute_disorder(combi_dis)
           ==
           pytest.approx(0.383, 0.001))

def test_alignment():
    continuum = Continuum()
    annotation = Annotation()
    annotation[Segment(1, 5)] = 'Carol'
    annotation[Segment(6, 8)] = 'Bob'
    annotation[Segment(12, 18)] = 'Carol'
    annotation[Segment(7, 20)] = 'Alice'
    continuum.add_annotation('liza', annotation)

    annotation = Annotation()
    annotation[Segment(2, 6)] = 'Carol'
    annotation[Segment(7, 8)] = 'Bob'
    annotation[Segment(12, 18)] = 'Alice'
    annotation[Segment(8, 10)] = 'Alice'
    annotation[Segment(7, 19)] = 'Jeremy'
    continuum.add_annotation('pierrot', annotation)
    annotation = Annotation()

    annotation[Segment(1, 6)] = 'Carol'
    annotation[Segment(8, 10)] = 'Alice'
    annotation[Segment(7, 19)] = 'Jeremy'
    annotation[Segment(19, 20)] = 'Alice'

    continuum.add_annotation('hadrien', annotation)

    categories = ['Carol', 'Bob', 'Alice', 'Jeremy']
    cat = np.array([[0, 0.5, 0.3, 0.7],
                    [0.5, 0., 0.6, 0.4],
                    [0.3, 0.6, 0., 0.7],
                    [0.7, 0.4, 0.7, 0.]])
    combi_dis = CombinedCategoricalDissimilarity(
        categories=categories,
        delta_empty=0.5,
        cat_dissimilarity_matrix=cat)
    set_unitary_alignments = []

    n_tuple = (('liza', Unit(Segment(1, 5), 'Carol')),
               ('pierrot', Unit(Segment(2, 6), 'Carol')),
               ('hadrien', Unit(Segment(1, 6), 'Carol')))
    unitary_alignment = UnitaryAlignment(n_tuple)
    set_unitary_alignments.append(unitary_alignment)

    n_tuple = (('liza', Unit(Segment(6, 8),'Bob')),
               ('pierrot', Unit(Segment(7, 8), 'Bob')),
               ('hadrien', Unit(Segment(8, 10), 'Alice')))
    unitary_alignment = UnitaryAlignment(n_tuple)
    set_unitary_alignments.append(unitary_alignment)

    n_tuple = (('liza', Unit(Segment(7, 20), 'Alice')),
               ('pierrot', Unit(Segment(7, 19), 'Jeremy')),
               ('hadrien', Unit(Segment(7, 19), 'Jeremy')))
    unitary_alignment = UnitaryAlignment(n_tuple)
    set_unitary_alignments.append(unitary_alignment)

    n_tuple = (('liza', Unit(Segment(12, 18), 'Carol')),
               ('pierrot', Unit(Segment(12, 18), 'Alice')),
               ('hadrien', None))
    unitary_alignment = UnitaryAlignment(n_tuple)
    set_unitary_alignments.append(unitary_alignment)

    n_tuple = (('liza', None),
               ('pierrot', Unit(Segment(8, 10), 'Alice')),
               ('hadrien', Unit(Segment(19, 20), 'Alice')))
    unitary_alignment = UnitaryAlignment(n_tuple)
    set_unitary_alignments.append(unitary_alignment)

    alignment = Alignment(set_unitary_alignments,
                          continuum=continuum,
                          check_validity=True)

    assert (alignment.compute_disorder(combi_dis)
            ==
            pytest.approx(5.35015024691358, 0.001))


def test_best_alignment():
    continuum = Continuum()
    annotation = Annotation()
    annotation[Segment(1, 5)] = 'Carol'
    annotation[Segment(6, 8)] = 'Bob'
    annotation[Segment(12, 18)] = 'Carol'
    annotation[Segment(7, 20)] = 'Alice'
    continuum.add_annotation('liza', annotation)

    annotation = Annotation()
    annotation[Segment(2, 6)] = 'Carol'
    annotation[Segment(7, 8)] = 'Bob'
    annotation[Segment(12, 18)] = 'Alice'
    annotation[Segment(8, 10)] = 'Alice'
    annotation[Segment(7, 19)] = 'Jeremy'
    continuum.add_annotation('pierrot', annotation)
    annotation = Annotation()

    annotation[Segment(1, 6)] = 'Carol'
    annotation[Segment(8, 10)] = 'Alice'
    annotation[Segment(7, 19)] = 'Jeremy'
    annotation[Segment(19, 20)] = 'Alice'

    continuum.add_annotation('hadrien', annotation)

    categories = ['Carol', 'Bob', 'Alice', 'Jeremy']
    cat = np.array([[0, 0.5, 0.3, 0.7],
                    [0.5, 0., 0.6, 0.4],
                    [0.3, 0.6, 0., 0.7],
                    [0.7, 0.4, 0.7, 0.]])
    combi_dis = CombinedCategoricalDissimilarity(
        categories=categories,
        delta_empty=0.5,
        cat_dissimilarity_matrix=cat)
    set_unitary_alignments = []

    n_tuple = (('liza', Unit(Segment(1, 5), 'Carol')),
               ('pierrot', Unit(Segment(2, 6), 'Carol')),
               ('hadrien', Unit(Segment(1, 6), 'Carol')))
    unitary_alignment = UnitaryAlignment(n_tuple)
    set_unitary_alignments.append(unitary_alignment)

    n_tuple = (('liza', Unit(Segment(6, 8), 'Bob')),
               ('pierrot', Unit(Segment(7, 8), 'Bob')),
               ('hadrien', Unit(Segment(8, 10), 'Alice')))
    unitary_alignment = UnitaryAlignment(n_tuple)
    set_unitary_alignments.append(unitary_alignment)

    n_tuple = (('liza', Unit(Segment(7, 20), 'Alice')),
               ('pierrot', Unit(Segment(7, 19), 'Jeremy')),
               ('hadrien', Unit(Segment(7, 19), 'Jeremy')))
    unitary_alignment = UnitaryAlignment(n_tuple)
    set_unitary_alignments.append(unitary_alignment)

    n_tuple = (('liza', Unit(Segment(12, 18), 'Carol')),
               ('pierrot', Unit(Segment(12, 18), 'Alice')),
               ('hadrien', None))
    unitary_alignment = UnitaryAlignment(n_tuple)
    set_unitary_alignments.append(unitary_alignment)

    n_tuple = (('liza', None),
               ('pierrot', Unit(Segment(8, 10), 'Alice')),
               ('hadrien', Unit(Segment(19, 20), 'Alice')))
    unitary_alignment = UnitaryAlignment(n_tuple)
    set_unitary_alignments.append(unitary_alignment)

    alignment = Alignment(set_unitary_alignments,
                          continuum=continuum,
                          check_validity=True)

    best_alignment = continuum.get_best_alignment(combi_dis)

    assert best_alignment.disorder == pytest.approx(0.31401409465020574,
                                                    0.001)
    assert best_alignment.disorder < alignment.compute_disorder(combi_dis)