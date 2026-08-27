## Project status

**The Alpha period is over.** From version 0.1.0 the three packages follow
semantic versioning: a public name is not removed, and what it means is not
changed, without a major version. That applies to the core and to both
backends.

### What is public

Everything a user of {{dist_name}} needs is re-exported from the top-level
`{{import_name}}` package, so nothing has to be imported from an internal
module. That re-exported set is the public API, and it is what the promise
above is about. Anything this package holds that is not re-exported is
internal and may change in any release.

The three packages share a version number and are released together, so the
version of one of them says which version of the other two it was built
against.
