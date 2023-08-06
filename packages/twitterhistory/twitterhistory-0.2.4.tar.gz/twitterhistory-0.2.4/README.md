# Download a history of posts and user metadata from the microblogging service Twitter

***Twitterhistory*** **is in early BETA status. Using it in production might be an absolutely bad idea. If you encounter any issues, [please report them](https://gitlab.com/christoph.fink/twitterhistory/-/issues) and/or submit a merge request with a fix.**

This is a Python module to download a complete history of posts and user metadata from the microblogging service Twitter using its API’s as of 2021 latest version 2. Data are saved to an SQLAlchemy/GeoAlchemy2-compatible database (currently only PostgreSQL/PostGIS is fully supported, see also the [documention of GeoAlchemy2](https://geoalchemy-2.readthedocs.io/en/latest/)).

![screen shot](extra/images/screenshot.png)

The script will download all Twitter status messages up until the current time, and keep track of already downloaded time periods in a cache file (default location `~/.cache/twitterhistory.yml`). When started the next time, it will attempt to fill gaps in the downloaded data and catch up until the then current time. 

To use *twitterhistory* your API key (see further down) needs to be associated to an account with [academic research access](https://developer.twitter.com/en/portal/petition/academic/is-it-right-for-you).

If you use *twitterhistory* for academic research, please cite it in your publication: <br />
Fink, C. (2021): *twitterhistory: a Python tool to download historical Twitter data*. [doi:10.5281/zenodo.4471195](https://doi.org/10.5281/zenodo.4471195)

### Dependencies

The script is written in Python 3 and depends on the Python modules [blessed](https://blessed.readthedocs.io/), [GeoAlchemy2](https://geoalchemy-2.readthedocs.io/), [psycopg2](https://www.psycopg.org/), [PyYaml](https://pyyaml.org/), [Requests](https://2.python-requests.org/en/master/) and [SQLAlchemy](https://sqlalchemy.org/).

### Installation

```shell
pip install twitterhistory
```

### Configuration

Copy the example configuration file [twitterhistory.yml.example](https://gitlab.com/christoph.fink/twitterhistory/-/raw/master/twitterhistory.yml.example) to a suitable location, depending on your operating system: 

- on Linux systems:
    - system-wide configuration: `/etc/twitterhistory.yml`
    - per-user configuration: 
        - `~/.config/twitterhistory.yml` OR
        - `${XDG_CONFIG_HOME}/twitterhistory.yml`
- on MacOS systems:
    - per-user configuration:
        - `${XDG_CONFIG_HOME}/twitterhistory.yml`
- on Microsoft Windows systems:
    - per-user configuration:
        `%APPDATA%\twitterhistory.yml`

Adapt the configuration:

- Configure a database connection string (`connection_string`), pointing to an existing database (with the PostGIS extension enabled).
- Configure an API [OAuth 2.0 Bearer token](https://developer.twitter.com/en/docs/authentication/oauth-2-0) with access to the Twitter API v2 `twitter_oauth2_bearer_token`).
- Configure one or more search terms for the query (`search_terms`).

If you have a cache file from a previous installation in which already downloaded time periods are saved, copy it to `${XDG_CACHE_HOME}/twitterhistory.yml` or `%LOCALAPPDATA%/twitterhistory.yml` on Linux or MacOS, and Microsoft Windows, respectively.

### Usage

#### Command line executable

```shell
python -m twitterhistory
```

#### Python

Import the `twitterhistory` module. Instantiate a `TwitterHistoryDownloader`, and call its `download()` method.

```python
import twitterhistory

downloader = twitterhistory.TwitterHistoryDownloader()
downloader.download()
```

### Data privacy

By default, *twitterhistory* pseudonymises downloaded metadata, i.e., it replaces (direct) identifiers with randomised identifiers (generated using hashes, i.e., one-way ‘encryption’). This serves as one step of a responsible data processing workflow. However, other (meta-)data might nevertheless qualify as indirect identifiers, as they, combined or on their own, might allow re-identification of a person. If you want to use data downloaded using *twitterhistory* in a GDPR-compliant fashion, you have to follow up the data collection stage with data minimisation and further pseudonymisation or anonymisation efforts.

*twitterhistory* can keep original identifiers (i.e., skip pseudonymisation). To instruct it to do so, instantiate a `TwitterHistoryDownloader` with the parameter `pseudonymise_identifiers=False` or set the according parameter in the configuration file. Ensure that you fulfil all legal and organisational requirements to handle personal information before you decide to collect non-pseudonyismed data.

```python
import twitterhistory

downloader = twitterhistory.TwitterHistoryDownloader(
    pseudonymise_identifiers = False  # get legal advice and ethics approval before doing this
)
downloader.download()
```
