import gqlmod
import gqlmod_github
from gqlmod.providers import _mock_provider


class MockGithubProvider(gqlmod_github.GitHubBaseProvider):
    def __call__(self, query, variables):
        self.last_query = query
        self.last_vars = variables


def test_get_schema():
    assert gqlmod.providers.query_for_schema('github')
    assert gqlmod.providers.query_for_schema('github-sync')
    assert gqlmod.providers.query_for_schema('github-async')


def test_import():
    gqlmod.enable_gql_import()
    import queries  # noqa
    prov = MockGithubProvider()
    with _mock_provider('github', prov):
        queries.Login()
        assert prov.last_vars['__previews'] == set()

        queries.start_check_run(repo=123, sha="beefbabe")
        assert prov.last_vars['__previews'] == set()

        queries.append_check_run(repo=123, checkrun=456)
        assert prov.last_vars['__previews'] == set()

        queries.get_label(repo=123, name="spam")
        assert prov.last_vars['__previews'] == set()

        queries.get_check_run(id=123)
        assert prov.last_vars['__previews'] == set()

        queries.go_deploy(id=123, repo=456)
        assert prov.last_vars['__previews'] == {"flash-preview"}


def test_async_import():
    gqlmod.enable_gql_import()
    import queries_async  # noqa
    prov = MockGithubProvider()
    with _mock_provider('github-async', prov):
        queries_async.Login()
        assert prov.last_vars['__previews'] == set()

        queries_async.start_check_run(repo=123, sha="beefbabe")
        assert prov.last_vars['__previews'] == set()

        queries_async.append_check_run(repo=123, checkrun=456)
        assert prov.last_vars['__previews'] == set()

        queries_async.get_label(repo=123, name="spam")
        assert prov.last_vars['__previews'] == set()

        queries_async.get_check_run(id=123)
        assert prov.last_vars['__previews'] == set()

        queries_async.go_deploy(id=123, repo=456)
        assert prov.last_vars['__previews'] == {"flash-preview"}
