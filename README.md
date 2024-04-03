# GraphDB Access Security Hub

> [!CAUTION]
> This project is still in very early stages of development. Use at your own risk.

> [!NOTE]
> We are looking for contributors to help us with this project!!!


GraphDB Access Security Hub (or just GASH) is an easy-to-use user authorization tool for microservices, based on [`Neo4j`](https://neo4j.com/docs/) database and minimalistic YAML policy config. It is build on top of modern technologies like [`Python 3.12`](https://www.python.org/), [`Pydantic 2+`](https://docs.pydantic.dev/latest/), [`FastStream 0.4+`](https://faststream.airt.ai/latest/) and [`pyneo4j-ogm 0.4+`](https://github.com/groc-prog/pyneo4j-ogm/blob/develop). GASH is currently a very young project, but we have ambicios plans for its future and are open to any feedback!

## Table of contents

- [What is GASH?](#what-is-gash)
- [Why GASH?](#why-gash)
- [Quickstart guide](#quickstart-guide)
    - [Configure a policy](#configure-a-policy)
    - [Start GASH](#start-gash)
    - [Add some entities](#add-some-entities)
    - [Get a permit](#get-a-permit)
- [Future Plans](#future-plans)
- [Policy File Reference](#policy-file-reference)
- [API Reference](#api-reference)
- [Deploy](#deploy)
- [Examples](#examples)
- [Testing](#testing)

## What is GASH?

GASH is an user authorization tool for microservices, highly inspired by such technologies as [`Google Zanzibar`](https://zanzibar.academy/) (and it's open analogue [`OpenFGA`](https://openfga.dev/)), [`OPA`](https://www.openpolicyagent.org/) and [`permit.io services`](https://permit.io/). Our main goal is to create an open-source, easy-to-use and flexible service that provides an async API (for now [`RabbitMQ`](https://www.rabbitmq.com/) only, but other brokers and protocols support is assumed) and implements RBAC (Users in GASH have roles, that define their rights opportunities according to the policy), a little ABAC (all entities, that will be described below, have basic attributes, that are defined in policy) and ReBAC (all entities are stored in graph-based db, and subject will only granted with permit, if it is linked to object, wheather directly or not).

## Why GASH?

The idea of this system went out of our team's development expirience of b2b services. Once we realized that our code is bloated with similar, but not same code for authorization, usually containing lots of queries to other microservices for context. We searched for the existing solutions and found out the following:

1. [`OPA`](https://www.openpolicyagent.org/) is the most popular solution, but it forces us to learn its policy language `rego` and stores data in memory in JSON format, so it was too general-purpose for us
2. [`permit.io`](https://permit.io/) offered plenty of services, especially [`ReBAC`](https://www.permit.io/rebac) that covered our needs, but it was proprietary, when we needed a self-hosted solution
3. [`OpenFGA`](https://openfga.dev/), also inspired by [`Google Zanzibar`](https://zanzibar.academy/) as [`permit.io's ReBAC`](https://www.permit.io/rebac) was also a good solution with modern SDK and detailed docs, but it had a bloated API, heavy JSON configs and enforsed logic of fully ReBAC authorization.

So we developed a system that will fit the following points: 

1. Fully self-hosted and open-source
2. Easy in use and configuration
3. Minimalistic async API
4. Iplementing best features of RBAC, ABAC and ReBAC
5. Using graph based database as dynamic authorization data storage

## Quickstart guide



### Configure a policy

Policy defines what roles

### Start GASH

### Add some entities

### Get a permit

## Future Plans

- [ ] Implement Python client library
- [ ] Move docs from readme to full-featured documentation site
- [ ] Optionaly return exceptions by RPC
- [ ] Add API methods for updating policy in runtime
- [ ] Implement HTTP API
- [ ] Implement custom CLI
- [ ] Support other brockers, that are supported by [`FastStream`](https://faststream.airt.ai/latest/)
- [ ] Extend policy with ABAC featues: permit/deny only if subject/object has/doesn't has attr, combinations of attrs, etc.
- [ ] Extend policy with graph-agnostic policies like rules for any user, rules for all objects of this type, etc.

## Policy File Reference

...

## API Reference

...

## Deploy

...
<!-- We recommend using GASH as  -->

## Examples

...

## Testing

...

