from mendeley import Mendeley
from hestia_earth.schema import Bibliography

from hestia_earth.extend_bibliography.bibliography_apis.utils import ORINGAL_FIELD, extend_bibliography, biblio_title


def _author_to_actor(author):
    return {
        'firstName': author.first_name,
        'lastName': author.last_name,
        'scopusID': author.scopus_author_id
    }


def _citation_to_bibliography(citation):
    has_identifiers = citation and citation.identifiers is not None
    doi = citation.identifiers['doi'] if has_identifiers and 'doi' in citation.identifiers else None
    scopus = citation.identifiers['scopus'] if has_identifiers and 'scopus' in citation.identifiers else None
    abstract = citation.abstract if citation.abstract else ''
    return {
        'title': biblio_title(citation.title),
        'year': citation.year,
        'documentType': citation.type,
        'outlet': citation.source,
        'mendeleyID': citation.id,
        'abstract': abstract,
        'documentDOI': doi,
        'scopus': scopus
    }


def create_biblio(citation, key: str, value: str):
    biblio = Bibliography()
    # save title here since closest citation might differ
    biblio.fields[ORINGAL_FIELD + key] = value if citation else None
    biblio.fields[key] = value
    authors = list(map(_author_to_actor, citation.authors if citation else []))
    bibliography = _citation_to_bibliography(citation) if citation else {}
    (extended_biblio, actors) = extend_bibliography(authors, citation.year) if citation else ({}, [])
    return (
        {**biblio.to_dict(), **bibliography, **extended_biblio},
        actors
    ) if citation else (biblio.to_dict(), [])


def _exec_search_by_title(session, value: str):
    items = session.catalog.search(value.rstrip(), view='all').list(50).items
    # try a search with shorter value if no results found
    items = items if len(items) > 0 else session.catalog.search(value[:100].rstrip(), view='all').list(50).items
    return list(map(lambda x: {'title': x.title, 'item': x}, items))


def _exec_search_by_id(session, value: str): return session.catalog.get(value.rstrip(), view='all')


def _exec_search_by_documentDOI(session, value: str):
    return session.catalog.by_identifier(doi=value.rstrip(), view='all')


def _exec_search_by_scopus(session, value: str):
    return session.catalog.by_identifier(scopus=value.rstrip(), view='all')


SEARCH_BY_KEY = {
    'title': _exec_search_by_title,
    'mendeleyID': _exec_search_by_id,
    'documentDOI': _exec_search_by_documentDOI,
    'scopus': _exec_search_by_scopus
}


def exec_search(session, key: str): return lambda value: SEARCH_BY_KEY[key](session, value)


def get_client(**kwargs):
    mendel = Mendeley(client_id=int(kwargs.get('mendeley_username')), client_secret=kwargs.get('mendeley_password'))
    auth = mendel.start_client_credentials_flow()
    session = auth.authenticate()
    return session
