---
name: understand-voxity
description: >-
  Explains Voxity's core concepts, how they connect, and how user-facing terms
  map to technical names: organizations (agents), conversations (threads), and
  calls (sessions), plus customers, opportunities, pipelines, stages, and
  communication channels. Read when explaining Voxity, interpreting its data,
  or deciding which records and relationships to use for a user's request.
---

# Understand Voxity data

Use natural product terms with users. Translate technical names when working
with tools: **organization → agent / agentId**, **conversation → thread**,
**call → session**.

## Organizations and customers

An **organization** is the business whose data you are working with. APIs and
storage commonly call this an `agent`. Keep related lookups within the same
organization; customer records are scoped to it.

A **customer** is the person/contact the organization interacts with. Their
record holds profile details, phone numbers, and channel identities. It connects
their opportunities, conversations, and calls. A customer can have multiple
opportunities and interactions.

Use customer IDs to connect records. Names, phone numbers, and social usernames
help find a customer but are not the customer's Voxity ID. A customer may have
multiple phone numbers or channel identities; do not assume matching names or
activity on another channel automatically establish the same customer.

## Opportunities, pipelines, and stages

An **opportunity** is a potential sale or business outcome being pursued with a
customer. It has its own name and customer link, and can have an owner, amount,
and qualification score. The customer is who; the opportunity is what the
business is pursuing.

A **pipeline** organizes a business process into **stages**. An opportunity
belongs to a pipeline and occupies a stage within it. Moving it changes its
stage while keeping the same opportunity and customer connection; stage changes
appear in the customer's history.

Each stage has a business name and a type: **open**, **won**, or **lost**.
Read the stage type to understand the outcome. For example, a pipeline might
use “New inquiry → Qualified → Proposal → Won,” with a Lost stage for deals
that do not proceed. These are illustrative names; use the organization's
actual pipeline and stages. Removing an opportunity is separate from losing it.

## Channels, conversations, and calls

A **communication channel** is how the organization communicates with a
customer: for example, phone, WhatsApp, Facebook, Instagram, Telegram, TikTok,
or a website chatbot. Channel identities and account IDs differ from Voxity
customer IDs.

A **conversation** (`thread`) is a customer's messaging history on a channel,
containing individual **messages** such as text and media. A customer can have
conversations across channels. The customer/channel lookup reuses an existing
conversation; do not treat every new exchange as a new thread. Conversation
activity and whether AI replies are enabled are separate settings.

A **call** (`session`) is an individual inbound or outbound phone call or
attempt. It has a status and may include a customer link, duration, recording,
transcript, and analysis. A failed or unanswered call is still a call record.
A call transcript may be labeled `conversation` in technical data; in that
context it means the call's spoken turns, rather than a messaging thread.

## Follow the relationships

Start with the organization, then identify the customer or opportunity relevant
to the request. For a deal, read its pipeline and stage. For communications,
follow the customer's conversations and calls.

Calls and conversations connect through the customer; sharing a customer does
not establish that every interaction concerns every opportunity. Use explicit
references or the interaction's content to connect it to a particular deal.

For maintenance sources and review decisions, see
[references/draft-review.md](references/draft-review.md).
