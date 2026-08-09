# TypeScript client shape

This alpha source package defines the five production OCL operation shapes:

- `getContext`;
- `resolveNoun`;
- `explainField`;
- `getJoinPath`;
- `validateWriteIntent`.

It is intentionally marked private until a package namespace and release
process exist. The invitation runtime is live, but no npm package has been
published. Import the source directly only for experiments.

An invited alpha client passes its bearer token as the second constructor
argument:

```ts
const ocl = new OCLClient(
  "https://api.context.nanti.ai",
  process.env.OCL_TOKEN!,
);
const pack = await ocl.getContext("Which invoices are unpaid?", {
  odoo_version: "19.0",
  edition: "community",
  modules: ["account"],
});
```
