from __future__ import annotations

import typing as t
from unittest import TestCase
from unittest.mock import patch, call, MagicMock

from piccolo.apps.migrations.tables import Migration
from piccolo.apps.migrations.commands.backwards import backwards
from piccolo.apps.migrations.commands.forwards import forwards
from piccolo.utils.sync import run_sync
from tests.base import postgres_only
from tests.example_app.tables import (
    Band,
    Concert,
    Manager,
    Poster,
    Ticket,
    Venue,
)

if t.TYPE_CHECKING:  # pragma: no cover
    from piccolo.table import Table


TABLE_CLASSES: t.List[t.Type[Table]] = [
    Manager,
    Band,
    Venue,
    Concert,
    Ticket,
    Poster,
]


@postgres_only
class TestForwardsBackwards(TestCase):
    """
    Test the forwards and backwards migration commands.
    """

    def test_forwards_backwards_all_migrations(self):
        """
        Test running all of the migrations forwards, then backwards.
        """
        for app_name in ("example_app", "all"):
            run_sync(forwards(app_name=app_name, migration_id="all"))

            # Check the tables exist
            for table_class in TABLE_CLASSES:
                self.assertTrue(table_class.table_exists().run_sync())

            run_sync(
                backwards(
                    app_name=app_name, migration_id="all", auto_agree=True
                )
            )

            # Check the tables don't exist
            for table_class in TABLE_CLASSES:
                self.assertTrue(not table_class.table_exists().run_sync())

    def test_forwards_backwards_single_migration(self):
        """
        Test running a single migrations forwards, then backwards.
        """
        for migration_id in ["1", "2020-12-17T18:44:30"]:
            run_sync(
                forwards(app_name="example_app", migration_id=migration_id)
            )

            table_classes = [Band, Manager]

            # Check the tables exist
            for table_class in table_classes:
                self.assertTrue(table_class.table_exists().run_sync())

            run_sync(
                backwards(
                    app_name="example_app",
                    migration_id=migration_id,
                    auto_agree=True,
                )
            )

            # Check the tables don't exist
            for table_class in table_classes:
                self.assertTrue(not table_class.table_exists().run_sync())

    def test_forwards_unknown_migration(self):
        """
        Test running an unknown migrations forwards.
        """
        with self.assertRaises(SystemExit) as manager:
            run_sync(
                forwards(
                    app_name="example_app", migration_id="migration-12345"
                )
            )

        self.assertEqual(
            manager.exception.__str__(), "migration-12345 is unrecognised"
        )

    def test_backwards_unknown_migration(self):
        """
        Test running an unknown migrations backwards.
        """
        run_sync(forwards(app_name="example_app", migration_id="all"))

        with self.assertRaises(SystemExit) as manager:
            run_sync(
                backwards(
                    app_name="example_app",
                    migration_id="migration-12345",
                    auto_agree=True,
                )
            )

        self.assertTrue(
            manager.exception.__str__().startswith(
                "Unrecognized migration name - must be one of "
            )
        )

    @patch("piccolo.apps.migrations.commands.backwards.print")
    def test_backwards_no_migrations(self, print_):
        """
        Test running migrations backwards if none have been run previously.
        """
        with self.assertRaises(SystemExit) as manager:
            run_sync(
                backwards(
                    app_name="example_app",
                    migration_id="2020-12-17T18:44:30",
                    auto_agree=True,
                )
            )

        self.assertEqual(manager.exception.code, 0)
        self.assertTrue(
            print_.mock_calls[-1] == call("No migrations to reverse!")
        )

    @patch("piccolo.apps.migrations.commands.forwards.print")
    def test_forwards_no_migrations(self, print_: MagicMock):
        """
        Test running the migrations if they've already run.
        """
        run_sync(forwards(app_name="example_app", migration_id="all"))

        with self.assertRaises(SystemExit) as manager:
            run_sync(forwards(app_name="example_app", migration_id="all"))

        self.assertEqual(manager.exception.code, 0)
        self.assertTrue(
            print_.mock_calls[-1] == call("No migrations left to run!")
        )

    def test_forwards_fake(self):
        """
        Test running the migrations if they've already run.
        """
        run_sync(
            forwards(app_name="example_app", migration_id="all", fake=True)
        )

        for table_class in TABLE_CLASSES:
            self.assertTrue(not table_class.table_exists().run_sync())

        ran_migration_names = (
            Migration.select(Migration.name).output(as_list=True).run_sync()
        )

        self.assertEqual(
            ran_migration_names,
            # TODO - rather than hardcoding, might fetch these dynamically.
            [
                "2020-12-17T18:44:30",
                "2020-12-17T18:44:39",
                "2020-12-17T18:44:44",
            ],
        )

    def tearDown(self):
        for table_class in TABLE_CLASSES + [Migration]:
            table_class.alter().drop_table(
                cascade=True, if_exists=True
            ).run_sync()
