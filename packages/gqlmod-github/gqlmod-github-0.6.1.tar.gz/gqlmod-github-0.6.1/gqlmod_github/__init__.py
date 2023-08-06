"""
Provider for GitHub's v4 GraphQL API.
"""
import urllib.request

import graphql

from gqlmod.helpers.types import get_schema, get_type


def find_directive(ast_node, name):
    if ast_node is None:
        return {}
    for d in ast_node.directives:
        if d.name.value == name:
            break
    else:
        return {}

    return {
        arg.name.value: graphql.value_from_ast_untyped(arg.value)
        for arg in d.arguments
    }


class PreviewFinder(graphql.Visitor):
    def __init__(self):
        self.previews = set()

    def enter(self, node, key, parent, path, ancestors):
        schema = get_schema(node)
        if schema is None:
            return
        # The node itself
        if hasattr(schema, 'ast_node'):
            d = find_directive(schema.ast_node, 'preview')
            if d and 'toggledBy' in d:
                self.previews.add(d['toggledBy'])

        # The node's type
        ntype = get_type(node, unwrap=True)
        if hasattr(ntype, 'ast_node'):
            d = find_directive(ntype.ast_node, 'preview')
            if d and 'toggledBy' in d:
                self.previews.add(d['toggledBy'])


def _build_accept(previews):
    if isinstance(previews, (list, tuple, set)):
        if previews:
            return ', '.join(
                f"application/vnd.github.{p}+json"
                for p in previews
            )
        else:
            return "application/json"
    elif isinstance(previews, str):
        return f"application/vnd.github.{previews}+json"
    elif previews is None:
        return "application/json"
    else:
        raise TypeError(f"Can't handle preview {previews!r}")


class GitHubBaseProvider:
    endpoint = 'https://api.github.com/graphql'

    def __init__(self, token=None):
        self.token = token

    def _build_accept_header(self, variables):
        previews = variables.pop('__previews', set())
        return _build_accept(previews)

    def _build_authorization_header(self, variables):
        return f"Bearer {self.token}"

    # This can't be async
    def get_schema_str(self):
        with urllib.request.urlopen("https://docs.github.com/public/schema.docs.graphql") as fobj:
            return fobj.read().decode('utf-8')

    def codegen_extra_kwargs(self, gast, schema):
        visitor = PreviewFinder()
        graphql.visit(gast, visitor)
        return {
            '__previews': visitor.previews,
        }


try:
    from gqlmod.helpers.urllib import UrllibJsonProvider
except ImportError:
    pass
else:
    class GitHubSyncProvider(GitHubBaseProvider, UrllibJsonProvider):
        def build_request(self, query, variables):
            qvars = variables.copy()
            qvars.pop('__previews')
            req = super().build_request(query, qvars)
            req.add_header('Accept', self._build_accept_header(variables))
            req.add_header('Authorization', self._build_authorization_header(variables))
            return req


try:
    from gqlmod.helpers.aiohttp import AiohttpProvider
except ImportError:
    pass
else:
    class GitHubAsyncProvider(GitHubBaseProvider, AiohttpProvider):
        use_json = True

        def modify_request_args(self, variables, kwargs):
            super().modify_request_args(variables, kwargs)
            kwargs.setdefault('headers', {}).update({
                'Accept': self._build_accept_header(variables),
                'Authorization': self._build_authorization_header(variables)
            })
            kwargs['json']['variables'].pop('__previews', None)
