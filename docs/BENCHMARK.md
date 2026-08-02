# Benchmark and evidence plan

## 1. Purpose

The benchmark must answer a commercial and technical question:

> Does OCL cause materially more correct and safer Odoo outcomes than a strong
> connector plus raw schema, at an acceptable context, latency, and cost?

It is not a prompt beauty contest and not a set of screenshots.

## 2. Evaluation arms

Use the same model, connector capabilities, user permissions, tenant fixture,
tool budget, and task wording across arms.

### Arm A: connector only

The model receives tool descriptions and returned records, but no full schema
dump or OCL context.

### Arm B: connector plus raw schema

The model receives the strongest realistic schema metadata and concise generic
Odoo operation instructions. This is the primary baseline.

### Arm C: connector plus OCL

The model receives the same connector plus an assembled OCL context pack. Do not
give it additional tools or permissions unavailable to Arm B.

Optional diagnostic arms may test generic documentation RAG or full ontology
dumping, but marketing claims must center on the three stable arms.

## 3. Unit of evaluation

Each case contains:

- immutable case ID and benchmark version;
- user question or action intent;
- database fixture and environment digest;
- user, group, company, language, and timezone context;
- allowed connector operations;
- expected ambiguity/clarification behavior;
- ground-truth query or action result;
- semantic rubric;
- critical failure conditions;
- token, latency, and cost capture;
- disclosure class: public, private, or rotating.

## 4. Task levels

### Level 1: interpretation

Can the AI identify the correct business noun, model, discriminating domain,
time field, state, and company/currency considerations?

### Level 2: query plan

Can it choose valid fields, joins, aggregation grain, signs, filters, and tool
operations without silently changing the question?

### Level 3: executed result

Does the plan execute and return the independently computed correct result?

### Level 4: explanation

Does the answer state important scope, assumptions, and limitations without
inventing unavailable facts?

### Level 5: write intent

Does it select the appropriate business method or flow, identify preconditions,
respect permission context, request required approval, and avoid dangerous raw
field writes?

An answer cannot receive full credit for eloquent prose with a wrong result.

## 5. Initial task families

### Revenue this month

Vary:

- invoice versus journal-entry interpretation;
- posted and draft records;
- refunds;
- invoice date versus accounting date;
- multiple companies and currencies;
- tax-included versus untaxed request wording;
- recognition-policy ambiguity.

### Unpaid customer invoices

Vary:

- not paid versus partial versus in-payment;
- due and not-yet-due;
- credit notes;
- commercial customer/contact;
- residual amount currency;
- inaccessible records.

### Overdue vendor bills

Vary move type, state, due date, partial payment, company, currency, and access.

### Salesperson ownership

Vary invoice ownership, source order ownership, fallback behavior, missing
salesperson, and tempting wrong user fields.

### Products selling but understocked

Vary product template/variant grain, ordered versus delivered sales, cancelled
orders, warehouse, free/on-hand/forecast stock, reservations, and units.

### Customers bought X but not Y

Vary sales order versus posted invoice definition, refunds, time window,
commercial entities, variants, and duplicate join paths.

### Available to sell

Vary warehouse/location scope, on-hand versus free versus forecast, incoming and
outgoing moves, reservations, owner/consignment, company, and units.

## 6. Ground truth

Ground truth must be produced independently of the OCL entry wording.

Use:

- controlled fixture construction with known expected values;
- Odoo business methods and reports where they are the authority;
- independently reviewed ORM queries;
- accounting/inventory domain review;
- result digests committed before the final OCL entries are evaluated.

For convention-dependent questions such as revenue, the expected correct
behavior may be to ask a clarifying question. Scoring must reward that rather
than force a single universal definition.

## 7. Metrics

Primary:

- exact executed-result correctness;
- semantic query-plan correctness;
- critical unsafe-action rate;
- clarification correctness on ambiguous tasks.

Secondary:

- domain/filter completeness;
- join/grain correctness;
- state/date/company/currency correctness;
- negative-knowledge adherence;
- hallucinated field/model rate;
- token count by input category;
- latency and estimated model/API cost;
- context precision: selected entries that were actually needed;
- context recall: required entries present.

Report absolute percentage-point change and raw counts. Do not report only a
relative percentage improvement.

## 8. Write-safety scoring

Separate severity classes:

- Critical: destructive, irreversible, financial posting, security, or broad
  multi-record impact.
- High: material state transition, allocation, payment, stock, or customer impact.
- Medium: reversible but semantically consequential change.
- Low: ordinary reversible edit.

Measure:

- intervention recall by severity;
- false escalation rate;
- correct method/flow selection;
- approval request correctness;
- permission/security awareness;
- action execution result on disposable fixtures.

`validate_write_intent` is advisory. A caught risk is useful, but the benchmark
must still execute allowed test actions through Odoo and verify their outcome.

## 9. Model protocol

For each evaluated model:

- pin exact provider model ID and evaluation date;
- disclose system prompt and tool definitions where licensing permits;
- hold temperature/reasoning settings constant across arms;
- use multiple runs for nondeterministic models;
- randomize arm order;
- isolate conversations between cases;
- cap retries and tool calls equally;
- capture failures, refusals, and timeouts;
- never select only the best run for OCL.

The target "five models" means five meaningfully different model families or
providers, not five aliases of one snapshot.

## 10. Public and private sets

### Public set

Publish enough cases, fixtures, prompts, and scoring code for independent
reproduction and community improvement.

### Private sealed set

Keep a larger set private to reduce prompt/corpus overfitting and marketing
gaming. Restrict access, hash the case manifest before runs, and log access.

### Rotating set

Add cases from real, consented failure patterns after redaction and independent
reconstruction. Never copy customer data into the benchmark.

Publishing some tests builds trust. Keeping all tests secret prevents scrutiny.
Publishing all tests makes optimization leakage too easy. Use all three sets.

## 11. Claim-release checklist

Before publishing a comparison:

- benchmark version and dates are stated;
- all arms used equivalent capabilities;
- strongest baseline prompt was reviewed;
- task-family and aggregate results are shown;
- raw counts and confidence intervals/repeated-run variance are shown;
- failures and regressions are included;
- model IDs and settings are stated;
- token/cost methodology is stated;
- no case was added after seeing only the OCL result;
- result artifacts are archived;
- wording says what was measured, not "AI now understands all of Odoo."

## 12. Stage 3 sealed implementation

The first sealed Accounting suite contains ten private cases tied to immutable
Stage 2 fixture digests. It includes the five core questions and five
adversarial variants. Each case has a stable structured rubric for concepts,
clarifications, operations, warnings, and critical failures.

The runner prepares 30 prompts:

- connector only;
- connector plus a strong normalized raw ORM schema;
- the identical raw-schema arm plus an assembled OCL pack.

All arms share one backend command, model ID, question, operation allowlist,
timeout, and prompt ceiling. Raw answers are assigned opaque evaluation IDs.
The independent reviewer receives no case ID or arm. The private map is restored
only for deterministic scoring.

Blind observations use:

```json
{
  "document_kind": "ocl.benchmark_blind_observations",
  "schema_version": "0.1.0",
  "format": "ocl-benchmark-blind-observations-v1",
  "annotations": [
    {
      "evaluation_id": "ocl-eval.<opaque>",
      "observations": {
        "concepts": [],
        "clarifications": [],
        "operations": [],
        "warnings": [],
        "critical_failures": []
      }
    }
  ]
}
```

Rubric-code annotation is a review operation, not an LLM self-score. The
coordinator must archive the raw run, blinded answers, private mapping,
observations, and score report together while keeping the mapping unavailable
to the reviewer during annotation.
