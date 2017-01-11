# Project structure

## Python requirements

Your immediate project requirements should go into `requirements.in`, then compiled with `pip-compile` and installed with `pip-sync`.

Do not edit `requirements.txt` directly.

## Python sources

All Python sources go into `src/` folder.

## Django settings

### Environment-independent settings

Settings that are common between different working environments (e.g. `INSTALLED_APPS` or `LOGIN_URL`) are configured in `src/funrun/settings.py`.

### Environment overrides

Settings that needs to be overriden in a specific environment (e.g. `ALLOWED_HOSTS`) are taken from `src/conf/local.py`, which is .gitignore'd.

### Sharing environment overrides

If setup for a specific environment (e.g. the production server) is to be shared via Git, put its settings into `src/conf/production.py`. On the production server, create a symlink:

```bash
ln -s src/conf/production.py local.py
```

## Static files

`django.contrib.staticfiles` is enabled and expects project static files at `static/`. The files become available under <http://funrun.com/static/>.

For production deployment, run `src/manage.py collectstatic` and add a rewrite rule pointing to `var/static`. With nginx, that would be:

```
location /static/ {
	alias /srv/funrun/var/static;  # or "root /srv/funrun/var;"
}
```

### `robots.txt` and friends

All files directly placed in `static/` folder (not in subfolders) will be also accessible as <http://funrun.com/filename.ext> (i.e. without the static prefix) with a special rule in `funrun.urls`. Typical uses are:

* `robots.txt`
* `favicon.ico`
* Google and other third-party domain verification meta files

## Dynamic data folder `var/`

Everything under `var/` is .gitignore'd. Use it for:

* `var/static/` (`manage.py collectstatic` destination)
* `var/media/` (media files)
* `var/venv/` (bundled virtualenv)
* `var/log/`, `var/backup/`, `var/run/` and similar uses

## `.gitignore`

Please don't put your `.pydevproject` and `.idea` ignores here. Put them in your `~/.gitignore` instead.
