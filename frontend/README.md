# Cuentee Frontend

Next.js application for Cuentee.

See the root [README](../README.md) for screenshots, architecture, environment variables, and local development instructions.

The pnpm version is pinned in `package.json` (`packageManager`). Docker installs
that exact version and copies `pnpm-workspace.yaml` before installing dependencies.
The workspace configuration allows install scripts only for `sharp` and
`unrs-resolver`; new dependencies requiring scripts must be reviewed and added
explicitly. Keep `--frozen-lockfile` enabled for reproducible builds.

To verify the production image from the repository root:

```sh
docker build --no-cache -t cuentee-frontend ./frontend
```

Both Docker and Compose probe `/api/health`, which returns `{"status":"ok"}`
without contacting Supabase or the API. This checks frontend liveness even when
external services are unavailable.
