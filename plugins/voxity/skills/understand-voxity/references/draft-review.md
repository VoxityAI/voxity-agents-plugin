# Draft review — 2026-10-17

This is a proposed skill for joint review, based on the local `voxity` checkout.
It has not yet been confirmed as the team's canonical business vocabulary.
Read this file when reviewing or maintaining the skill, rather than for routine
Voxity data retrieval.

## Review decisions

- Purpose: everyday understanding and navigation, at the level a human user
  needs. Keep the entrypoint short and conceptual.
- Use “organization” in explanations, mapping it to technical `agent`/`agentId`.
  Likewise map conversation to thread and call to session.
- Cover organizations, customers, opportunities, pipelines/stages, channels,
  conversations, and calls. Omit detailed touches, activities, memories,
  workplaces, and storage mechanics from the entrypoint.
- Infer relationship guidance from source behavior rather than asking the
  user to supply technical invariants.

## Evidence inspected

Paths below are relative to the `voxity` repository, not this plugin repository.
They are maintainer provenance, not runtime dependencies or links requiring
plugin users to have the source checkout.

- `packages/shared/src/data/entities/agent/index.ts`: agent subcollections.
- `packages/shared/src/data/entities/agent/customer/index.ts`: customer profile,
  identities, workplace, and phone-number subcollection.
- `packages/services/src/customers/phoneNumbers/resolveCustomerFromPhoneNumber.ts`:
  agent-scoped phone resolution, including primary/secondary records and a
  legacy top-level phone fallback.
- `packages/shared/src/data/entities/agent/opportunity/index.ts`: customer
  association, pipeline/stage, owner, amount, score, and removal flag.
- `packages/shared/src/data/entities/agent/pipeline/{index.ts,stage/index.ts}`:
  pipeline structure and open/won/lost stage types.
- `packages/docs/api-reference/threads/{README.md,the-thread-object.md}`:
  explicit conversation/thread equivalence and public thread representation.
- `packages/shared/src/data/entities/agent/thread/{index.ts,message/index.ts,touch/index.ts}`:
  storage representation, independent state fields, message roles, touches.
- `packages/services/src/touches/{createActiveTouchIfNeeded.ts,closeActiveTouch.ts}`:
  active touch creation, closure, message references/counts, authorship checks.
- `packages/shared/src/data/entities/session/{index.ts,conversation/index.ts}`:
  call/session structure, optional customer, transcript turns/events.
- `packages/services/src/sessions/resolveCustomerBySession.ts`: explicit
  customer association and direction-dependent phone fallback.
- `packages/docs/api-reference/calls/the-call-object.md`: public call shape,
  duration in seconds, transcript and post-processing metadata.
- `packages/shared/src/data/entities/agent/customer/chat/index.ts`: typed
  timeline events for calls, messages, notes, and opportunity changes.
- `packages/docs/api-reference/customers/activity/the-activity-object.md`:
  public activity concept.
- `packages/docs/api-reference/customers/memory/{README.md,memory-organization.md}`:
  customer memories and context segments.
- `packages/docs/api-reference/workplaces/the-workplace-object.md` and
  `packages/docs/api-reference/customers/the-customer-object.md`: workplace
  meaning and primary workplace association.

## Additional relationship checks

- `packages/server/src/endpoints/_public/v1/customer/thread/create/index.ts`:
  rejects an existing customer/channel pair with `THREAD_ALREADY_EXISTS`.
- `packages/server/src/middlewares/entityChecks/requireOrCreateThreadChannel.ts`:
  finds/reuses a thread by customer and resolved channel, or creates one.
  This is observed API behavior, not proof of global database uniqueness.
- `packages/server/src/endpoints/_public/v1/opportunities/update/index.ts`:
  updates the opportunity and emits an opportunity-stage-changed customer
  history event when the stage ID changes.
- `packages/server/src/endpoints/_public/v1/opportunities/middlewares/pipelineStageExist.ts`:
  validates the requested stage within the selected pipeline. No mandatory
  sequential progression is established by this check, so the example in the
  skill illustrates a business process rather than an enforced transition graph.

## Limits of this exploration

This was a read-only source and documentation exploration. No production
customer data was inspected and no live MCP behavior was exercised. API docs
and storage definitions differ in field shape, so the draft teaches concepts
and defers exact parameters to the tool actually available. Cardinalities
shown as “can have multiple” describe supported relationships, not a promise
that channels or records are automatically reconciled.
