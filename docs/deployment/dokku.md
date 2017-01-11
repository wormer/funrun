# Deployment to Dokku platform

The following guide assumes that the [official command line client](http://dokku.viewdocs.io/dokku/community/clients/#bash-zsh-etc-dokku_clientsh) `dokku` is installed at the operator's machine.

## Initial setup

In a local operator copy:

```bash
DOKKU_HOST=dokku.me dokku apps:create funrun
dokku postgres:create funrun
dokku postgres:connect funrun < funrun.backup.sql
dokku postgres:link funrun funrun
dokku storage:mount /srv/funrun/media:/app/var/media
dokku config:set SECRET_KEY=$(pwgen -s 50 -n 1)
dokku config:set \
	ALLOWED_HOSTS=funrun.com \
	SENTRY_DSN=https://xxx:yyy@sentry.com/12345
git push dokku master
dokku domains:add funrun.com www.funrun.com
dokku redirect:set funrun www.funrun.com funrun.com
dokku letsencrypt funrun
```

The project is now accessible at <https://funrun.com>.

## Update production site

**ATTENTION: The production site is updated automatically! See [Deployment workflow](workflow.md) for details. Please only use this if Gitlab CI is disabled or broken.**

In a local operator copy:

```bash
git push dokku@dokku.me:funrun HEAD:master --force
```

This pushes the current local branch to Dokku.
