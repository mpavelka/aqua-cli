Aqua CLI
===

## Example usage

Add labels to selected repositories by their names

```sh
REPOSITORY_NAMES="
foobar/foobar-be
foobar/foobar-fe
"
echo "$REPOSITORY_NAMES" | python3 ./cli.py -k id --csv --no-header repositories-retrieve-selected --names-stdin | python3 ./cli.py repositories.labels.add --ids-stdin -l foobar
```
