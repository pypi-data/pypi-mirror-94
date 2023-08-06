from datetime import datetime
import sqlite3

import pytest  # type: ignore [import]
import pytz

from strava_offline import config
from strava_offline import sqlite
from strava_offline.strava import StravaAPI


def database():
    return sqlite.database(config.DatabaseConfig(strava_sqlite_database=":memory:"))


def strava(tmp_path):
    token = tmp_path / "token.json"
    token.write_text('{"access_token": "token"}')
    cfg = config.StravaApiConfig(strava_token_filename=str(token))
    return StravaAPI(config=cfg, scope=[])


@pytest.mark.vcr
def test_sync_bikes(tmp_path):
    with database() as db:
        # initial sync
        sqlite.sync_bikes(strava=strava(tmp_path), db=db)

        # check that we have all the bikes we expect
        bikes = [list(row) for row in db.execute(
            "SELECT id, name FROM bike ORDER BY id")]
        assert bikes == [
            ['b123456', 'bike1'],
            ['b234567', 'bike2'],
            ['b345678', 'bike3'],
        ]

        # delete one bike
        db.execute("DELETE FROM bike WHERE id = 'b123456'")

        # sync again
        sqlite.sync_bikes(strava=strava(tmp_path), db=db)

        # recheck that we have all the bikes we expect
        bikes = [list(row) for row in db.execute(
            "SELECT id, name FROM bike ORDER BY id")]
        assert bikes == [
            ['b123456', 'bike1'],
            ['b234567', 'bike2'],
            ['b345678', 'bike3'],
        ]


@pytest.mark.vcr
def test_sync_activities(tmp_path):
    before = datetime.fromtimestamp(1610000000, tz=pytz.utc)

    with database() as db:
        # initial sync
        sqlite.sync_activities(strava=strava(tmp_path), db=db, before=before)

        # check that we have all the activities we expect
        activities = [list(row) for row in db.execute(
            "SELECT id FROM activity ORDER BY id")]
        assert activities == [
            [1234567890],
            [1234567892],
            [1234567894],
            [1234567896],
            [1234567898],
            [1234567900],
            [1234567902],
            [1234567904],
            [1234567906],
            [1234567908],
            [1234567910],
            [1234567912],
        ]

        # delete newest and oldest activity
        db.execute("DELETE FROM activity WHERE id = 1234567890 OR id = 1234567912")

        # sync again
        sqlite.sync_activities(strava=strava(tmp_path), db=db, before=before)

        # recheck that we have all the activities we expect
        activities = [list(row) for row in db.execute(
            "SELECT id FROM activity ORDER BY id")]
        assert activities == [
            [1234567890],
            [1234567892],
            [1234567894],
            [1234567896],
            [1234567898],
            [1234567900],
            [1234567902],
            [1234567904],
            [1234567906],
            [1234567908],
            [1234567910],
            [1234567912],
        ]

        # delete newest activity
        db.execute("DELETE FROM activity WHERE id = 1234567912")

        # sync again, but only incrementally
        sqlite.sync_activities_incremental(strava=strava(tmp_path), db=db, before=before)

        # recheck that we have all the activities we expect
        activities = [list(row) for row in db.execute(
            "SELECT id FROM activity ORDER BY id")]
        assert activities == [
            [1234567890],
            [1234567892],
            [1234567894],
            [1234567896],
            [1234567898],
            [1234567900],
            [1234567902],
            [1234567904],
            [1234567906],
            [1234567908],
            [1234567910],
            [1234567912],
        ]


@pytest.mark.vcr
def test_migration_bikes(tmp_path):
    db_uri = "file:test_migration_bikes?mode=memory&cache=shared"
    cfg = config.DatabaseConfig(strava_sqlite_database=db_uri)
    db_keep_in_memory = sqlite3.connect(db_uri)

    with sqlite.database(cfg) as db:
        sqlite.sync_bikes(strava=strava(tmp_path), db=db)
        db.execute("UPDATE bike SET name = 'xxx'")
        db.execute("PRAGMA user_version = 0")
        db.commit()

    with sqlite.database(cfg) as db:
        bikes = [row['name'] for row in db.execute(
            "SELECT name FROM bike ORDER BY id LIMIT 1")]
        assert bikes == ['bike1']

    db_keep_in_memory.close()


@pytest.mark.vcr
def test_migration_activities(tmp_path):
    db_uri = "file:test_migration_activities?mode=memory&cache=shared"
    cfg = config.DatabaseConfig(strava_sqlite_database=db_uri)
    db_keep_in_memory = sqlite3.connect(db_uri)

    before = datetime.fromtimestamp(1610000000, tz=pytz.utc)

    with sqlite.database(cfg) as db:
        sqlite.sync_activities(strava=strava(tmp_path), db=db, before=before)
        db.execute("UPDATE activity SET name = 'xxx'")
        db.execute("PRAGMA user_version = 0")
        db.commit()

    with sqlite.database(cfg) as db:
        activities = [row['name'] for row in db.execute(
            "SELECT name FROM activity ORDER BY id LIMIT 1")]
        assert activities == ['name1']

    db_keep_in_memory.close()
