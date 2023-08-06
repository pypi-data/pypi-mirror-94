Prisma Get Info
---------------------

#### Requirements
* Panorama with `cloud_services` plugin v1.8 or higher (Prisma Access)
* Python >=3.7 (may work on lower)
* Python modules:
    * pan-python >= 0.16.0 - 
    * tabulate >= 0.8.7 - <https://github.com/astanin/python-tabulate>
    * xmltodict

#### License
MIT

#### Installation:
* Via PIP: `pip install --upgrade prisma_get_info`
* Via download: Clone/Download, and from the directory run `./get_prisma_spn.py`

#### Usage:
Run `prisma_get_spn` or `prisma_get.spn.py` depending on how downloaded/installed.
```bash
edwards-mbp-pro:prisma_get_info aaron$ prisma_get_spn
Panorama Hostname: panorama-test.mydomain.org
Panorama Username: aaron
Panorama Password: 
us-east             us-southwest
------------------  ----------------------
us-east-clementine  us-southwest-kumarahou
                    us-southwest-poplar
edwards-mbp-pro:prisma_get_info aaron$
```

Can also use `--output-json-file` command line switch to save output as JSON file:

```json
{
    "us-east": [
        "us-east-clementine"
    ],
    "us-southwest": [
        "us-southwest-kumarahou",
        "us-southwest-poplar"
    ]
}
```

Full options available when run with `--help`.

#### Version
Version  | Changes
-------  | --------
**1.0.1**| Initial Release.

#### Arguments
```text
edwards-mbp-pro:prisma_get_info aaron$ prisma_get_spn --help
usage: prisma_get_spn [-h] [--host HOST] [--user USER] [--pass PASS] [--panorama-api-key PANORAMA_API_KEY]
                      [--tenant TENANT] [--output-json-file OUTPUT_JSON_FILE]

Prisma get Info (managed by Panorama).

optional arguments:
  -h, --help            show this help message and exit

API:
  These options change how this program connects to the API.

  --host HOST           Panorama hostname or IP (or ENV var PANORAMA_HOST). If not entered, will prompt.
  --user USER           Panorama username (or ENV var PANORAMA_USERNAME). If not entered, will prompt.
  --pass PASS           Panorama password (or ENV var PANORAMA_PASSWORD). If not entered, will prompt.
  --panorama-api-key PANORAMA_API_KEY
                        Authenticate with Panorama API KEY instead of username/password.
  --tenant TENANT       Tenant name (if multi-tenancy is enabled.)

Output:
  These options change how the output is generated.

  --output-json-file OUTPUT_JSON_FILE
                        Output as JSON to this specified file name
edwards-mbp-pro:prisma_get_info aaron$
```