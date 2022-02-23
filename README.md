[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/stactools-packages/gbif/main?filepath=docs/installation_and_basic_usage.ipynb)

# stactools-gbif

- Name: gbif
- Package: `stactools.gbif`
- PyPI: https://pypi.org/project/stactools-gbif/
- Owner: @TomAugspurger
- Dataset homepage: http://example.com
- STAC extensions used:
  - [table](https://github.com/stac-extensions/table/)

A short description of the package and its usage.

## Examples

### STAC objects

- [Collection](examples/collection.json)
- [Item](examples/item/item.json)

### Command-line usage

Description of the command line functions

```bash
$ stac gbif create-item "az://gbif/occurrence/2021-04-13/occurrence.parquet" \
   item.json \
   --storage-options='{"account_name": "ai4edataeuwest"}'
```

Use `stac gbif --help` to see all subcommands and options.
