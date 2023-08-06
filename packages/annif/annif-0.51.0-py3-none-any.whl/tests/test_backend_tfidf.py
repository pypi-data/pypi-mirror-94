"""Unit tests for the TF-IDF backend in Annif"""

import pytest
import annif
import annif.backend
import annif.corpus
from annif.exception import ConfigurationException


def test_tfidf_default_params(project):
    tfidf_type = annif.backend.get_backend("tfidf")
    tfidf = tfidf_type(
        backend_id='tfidf',
        config_params={},
        project=project)

    expected_default_params = {
        'limit': 100  # From AnnifBackend class
    }
    actual_params = tfidf.params
    for param, val in expected_default_params.items():
        assert param in actual_params and actual_params[param] == val


def test_tfidf_train(datadir, document_corpus, project):
    tfidf_type = annif.backend.get_backend("tfidf")
    tfidf = tfidf_type(
        backend_id='tfidf',
        config_params={'limit': 10},
        project=project)

    tfidf.train(document_corpus)
    assert len(tfidf._index) > 0
    assert datadir.join('tfidf-index').exists()
    assert datadir.join('tfidf-index').size() > 0


def test_tfidf_train_input_limited(document_corpus, project):
    tfidf_type = annif.backend.get_backend("tfidf")
    tfidf = tfidf_type(
        backend_id='tfidf',
        config_params={'limit': 10, 'input_limit': 1},
        project=project)
    # Training on documents truncated to only one character fails
    with pytest.raises(ValueError) as excinfo:
        tfidf.train(document_corpus)
    assert 'empty vocabulary; perhaps the documents only contain stop words' \
        in str(excinfo)


def test_tfidf_train_negative_input_limit(document_corpus, project):
    tfidf_type = annif.backend.get_backend("tfidf")
    tfidf = tfidf_type(
        backend_id='tfidf',
        config_params={'limit': 10, 'input_limit': -1},
        project=project)
    with pytest.raises(ConfigurationException):
        tfidf.train(document_corpus)


def test_tfidf_suggest(project):
    tfidf_type = annif.backend.get_backend("tfidf")
    tfidf = tfidf_type(
        backend_id='tfidf',
        config_params={'limit': 10},
        project=project)

    results = tfidf.suggest("""Arkeologiaa sanotaan joskus myös
        muinaistutkimukseksi tai muinaistieteeksi. Se on humanistinen tiede
        tai oikeammin joukko tieteitä, jotka tutkivat ihmisen menneisyyttä.
        Tutkimusta tehdään analysoimalla muinaisjäännöksiä eli niitä jälkiä,
        joita ihmisten toiminta on jättänyt maaperään tai vesistöjen
        pohjaan.""")

    assert len(results) == 10
    hits = results.as_list(project.subjects)
    assert 'http://www.yso.fi/onto/yso/p1265' in [
        result.uri for result in hits]
    assert 'arkeologia' in [result.label for result in hits]


def test_tfidf_suggest_input_limited(project):
    tfidf_type = annif.backend.get_backend("tfidf")
    tfidf = tfidf_type(
        backend_id='tfidf',
        config_params={'limit': 10, 'input_limit': 1},
        project=project)

    results = tfidf.suggest("""Arkeologia.""")
    assert len(results) == 0


def test_suggest_params(project):
    tfidf_type = annif.backend.get_backend("tfidf")
    tfidf = tfidf_type(
        backend_id='tfidf',
        config_params={'limit': 10},
        project=project)
    params = {'limit': 3}

    results = tfidf.suggest("""Arkeologiaa sanotaan joskus myös
        muinaistutkimukseksi tai muinaistieteeksi. Se on humanistinen tiede
        tai oikeammin joukko tieteitä, jotka tutkivat ihmisen menneisyyttä.
        Tutkimusta tehdään analysoimalla muinaisjäännöksiä eli niitä jälkiä,
        joita ihmisten toiminta on jättänyt maaperään tai vesistöjen
        pohjaan.""", params)
    assert len(results) == 3


def test_tfidf_suggest_unknown(project):
    tfidf_type = annif.backend.get_backend("tfidf")
    tfidf = tfidf_type(
        backend_id='tfidf',
        config_params={'limit': 10},
        project=project)

    results = tfidf.suggest("abcdefghijk")  # unknown word

    assert len(results) == 0
