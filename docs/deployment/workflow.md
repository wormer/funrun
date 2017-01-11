# Deployment workflow

Currently the project only has a production site, no testing servers.

## Production site

The production site is <https://funrun.co>.

It is deployed to Dokku platform, see [Deployment to Dokku platform](dokku.md) for details. The underlying platform server is `dokku.me`. Contact <teamlead@funrun.com> to have your SSH key added to the server.

The site updates automatically from `master` branch with Gitlab CI, as configured in `.gitlab-ci.yml` file in the project root.
