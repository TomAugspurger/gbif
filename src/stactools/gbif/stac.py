import json
import logging
import datetime

import importlib.resources
import pystac
import stac_table

logger = logging.getLogger(__name__)


def create_item(asset_href: str, storage_options=None, asset_extra_fields=None) -> pystac.Item:
    """
    Create a STAC item for a GBIF Parquet Dataset.

    Parameters
    ----------
    asset_href : str
        The path, including fsspec protocol if necessary, to the root of the parquet datasets.
    storage_options: dict[str, Any], optional
        Storage options used when creating the fsspec filesystem to read the metadata
    asset_extra_fields:
        Additional fields to include in the asset.

    Examples
    --------
    >>> create_item(
    ...     "az://gbif/occurrence/2021-04-13/occurrence.parquet",
    ...     storage_options=dict(account_name="ai4edataeuwest")
    ... )
    """
    date = datetime.datetime(*list(map(int, asset_href.split("/")[-2].split("-"))))
    date_id = f"{date:%Y-%m-%d}"

    item = pystac.Item(
        f"gbif-{date_id}",
        geometry={
            "type": "Polygon",
            "coordinates": [
                [
                    [180.0, -90.0],
                    [180.0, 90.0],
                    [-180.0, 90.0],
                    [-180.0, -90.0],
                    [180.0, -90.0],
                ]
            ],
        },
        bbox=[-180, -90, 180, 90],
        datetime=date,
        properties={},
    )

    result = stac_table.generate(
        asset_href,
        item,
        storage_options=storage_options,
        proj=False,
        asset_extra_fields=asset_extra_fields,
        count_rows=False,
    )

    column_descriptions = json.loads(importlib.resources.read_text("stactools.gbif", "column_descriptions.json"))
    for column in result.properties["table:columns"]:
        column["description"] = column_descriptions[column["name"]]

    result.validate()
    return result


def create_collection(asset_extra_fields=None):
    asset_extra_fields = asset_extra_fields or {}

    collection = pystac.Collection(
        "gbif",
        description="{{ collection.description }}",
        extent=pystac.Extent(
            spatial=pystac.collection.SpatialExtent([[-180, -90, 180, 90]]),
            temporal=pystac.collection.TemporalExtent([datetime.datetime(2021, 4, 13), None]),
        ),
    )
    # collection.extra_fields["table:columns"] = result.properties["table:columns"]
    collection.title = "Global Biodiversity Information Facility (GBIF)"

    pystac.extensions.item_assets.ItemAssetsExtension.add_to(collection)
    collection.extra_fields["item_assets"] = {
        "data": {
            "type": stac_table.PARQUET_MEDIA_TYPE,
            "title": "Dataset root",
            "roles": ["data"],
            **asset_extra_fields,
        }
    }

    collection.stac_extensions.append(stac_table.SCHEMA_URI)
    collection.keywords = ["GBIF", "Biodiversity", "Species"]
    collection.extra_fields["msft:short_description"] = (
        "An international network and data infrastructure funded by the world's "
        "governments providing global data that document the occurrence of species."
    )
    collection.extra_fields["msft:container"] = "gbif"
    collection.extra_fields["msft:storage_account"] = "ai4edataeuwest"
    collection.providers = [
        pystac.Provider(
            "Global Biodiversity Information Facility",
            roles=[
                pystac.provider.ProviderRole.PRODUCER,
                pystac.provider.ProviderRole.LICENSOR,
                pystac.provider.ProviderRole.PROCESSOR,
            ],
            url="https://www.gbif.org/",
        ),
        # pystac.Provider(
        #     "Microsoft",
        #     roles=[pystac.provider.ProviderRole.HOST],
        #     url="https://planetarycomputer.microsoft.com",
        # ),
    ]
    # collection.assets["thumbnail"] = pystac.Asset(
    #     title="Forest Inventory and Analysis",
    #     href=(
    #         "https://ai4edatasetspublicassets.blob.core.windows.net/"
    #         "assets/pc_thumbnails/gbif.png"
    #     ),
    #     media_type="image/png",
    # )
    collection.links = [
        pystac.Link(
            pystac.RelType.LICENSE,
            target="https://www.gbif.org/terms",
            media_type="text/html",
            title="Terms of use",
        )
    ]
    # collection.validate()
    return collection

