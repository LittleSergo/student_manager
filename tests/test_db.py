from sqlalchemy import inspect
from pytest import mark

from db import get_db


def test_init_db_command(runner):
    """Test cli command."""
    result = runner.invoke(args=['init-db'])
    assert result.exit_code == 0
    assert 'Initialized the database' in result.output


@mark.parametrize('table', ('student', 'group', 'course'))
def test_table_existing(app, table):
    engine = get_db()
    with engine.connect() as connection:
        assert table in inspect(connection).get_table_names()
