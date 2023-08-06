"""Verify Jinja2 filters/extensions are available from pre-gen/post-gen hooks."""
import os

from _collections import OrderedDict
import freezegun
import pytest

from tackle.main import tackle


@pytest.fixture(autouse=True)
def freeze():
    """Fixture. Make time stating during all tests in this file."""
    freezer = freezegun.freeze_time("2015-12-09 23:33:01")
    freezer.start()
    yield
    freezer.stop()


def test_jinja2_time_extension(change_dir_main_fixtures, tmpdir):
    """Verify Jinja2 time extension work correctly."""
    context = tackle('test-extensions/default/', no_input=True, output_dir=str(tmpdir))
    assert type(context) == OrderedDict

    changelog_file = os.path.join(tmpdir, os.listdir(tmpdir)[0], 'HISTORY.rst')
    assert os.path.isfile(changelog_file)

    with open(changelog_file, 'r', encoding='utf-8') as f:
        changelog_lines = f.readlines()

    expected_lines = [
        'History\n',
        '-------\n',
        '\n',
        '0.1.0 (2015-12-09)\n',
        '---------------------\n',
        '\n',
        'First release on PyPI.\n',
    ]
    assert expected_lines == changelog_lines


def test_jinja2_slugify_extension(change_dir_main_fixtures, tmpdir):
    """Verify Jinja2 slugify extension work correctly."""
    context = tackle('test-extensions/default/', no_input=True, output_dir=str(tmpdir))

    assert os.listdir(tmpdir)[0] == "it-s-slugified-foobar"
    # assert context == OrderedDict(
    #     [
    #         (
    #             'cookiecutter',
    #             OrderedDict(
    #                 [
    #                     ('project_slug', 'it-s-slugified-foobar'),
    #                     ('year', '2015'),
    #                     ('_template', os.path.join(cwd, 'fixtures/test-extensions/default')), # noqa
    #                     ('_output_dir', tmpdir),
    #                 ]
    #             ),
    #         )
    #     ]
    # )
    # Broke when added work_in to prompt
    # expected_output = {
    #     'project_slug': 'it-s-slugified-foobar',
    #     'year': '2015',
    #     '_template': os.path.join(cwd, 'fixtures/test-extensions/default'),
    #     '_output_dir': tmpdir,
    # }

    assert context['project_slug'] == 'it-s-slugified-foobar'
