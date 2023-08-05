# History

0.0.5 (2021-02-05)
------------------

- Specify arrow version, as newer versions don't work well with 'days' directive in
  YAML (arrow is used in jinja2-time).

- Caches the config per endpoint. This includes a scenario folder option to supply
  a custom scenario folder location (per endpoint).


0.0.4 (2021-02-04)
------------------

- Fixed saving 'organisation_uuid' and 'result_folder' with the `api settings`
  command.

- First official release candidate as a typer app that introduces a plugin system.



0.0.3 (2020-12-21)

- Fixed settings context if config file is not yet available.


## 0.0.1b (2020-12-18)

- First (beta) pypi release.
