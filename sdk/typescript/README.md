# TypeScript client shape

This alpha source package defines the five production OCL operation shapes:

- `getContext`;
- `resolveNoun`;
- `explainField`;
- `getJoinPath`;
- `validateWriteIntent`.

It is intentionally marked private until a hosted endpoint, package namespace,
and release process exist. Import the source in experiments; do not claim that
an npm package has been published.

An invited alpha client passes its bearer token as the second constructor
argument:

```ts
const ocl = new OCLClient(process.env.OCL_URL!, process.env.OCL_TOKEN!);
const pack = await ocl.getContext("Which invoices are unpaid?", {
  odoo_version: "19.0",
  edition: "community",
  modules: ["account"],
});
```
