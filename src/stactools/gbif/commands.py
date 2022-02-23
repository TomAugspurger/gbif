import logging
import json

import click

from stactools.gbif import stac

logger = logging.getLogger(__name__)


def create_gbif_command(cli):
    """Creates the stactools-gbif command line utility."""

    @cli.group(
        "gbif",
        short_help=("Commands for working with stactools-gbif"),
    )
    def gbif():
        pass

    @gbif.command(
        "create-collection",
        short_help="Creates a STAC collection",
    )
    @click.argument("destination")
    def create_collection_command(destination: str):
        """Creates a STAC Collection

        Args:
            destination (str): An HREF for the Collection JSON
        """
        collection = stac.create_collection()

        collection.set_self_href(destination)

        collection.save_object()

        return None

    @gbif.command("create-item", short_help="Create a STAC item")
    @click.argument("source")
    @click.argument("destination")
    @click.option("--storage-options")
    def create_item_command(source: str, destination: str, storage_options: str):
        """Creates a STAC Item

        Args:
            source (str): HREF of the Asset associated with the Item
            destination (str): An HREF for the STAC Collection
        """
        if storage_options:
            so = json.loads(storage_options)
        else:
            so = None
        item = stac.create_item(source, storage_options=so)

        item.save_object(dest_href=destination)

        return None

    return gbif
