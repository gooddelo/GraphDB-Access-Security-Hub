# GraphDB Access Security Hub

GraphDB Access Security Hub (or just GASH) is an easy-to-use user authorization tool for microservices, based on [`Neo4j`](https://neo4j.com/docs/) database and minimalistic YAML policy config. It is build on top of modern technologies like [`Python 3.12`](https://www.python.org/), [`Pydantic 2+`](https://docs.pydantic.dev/latest/), [`FastStream 0.4+`](https://faststream.airt.ai/latest/) and [`pyneo4j-ogm 0.4+`](https://github.com/groc-prog/pyneo4j-ogm/blob/develop). GASH is currently a very young project, but we have ambicios plans for its future and are open to any feedback!

## Table of contents

- [What is GASH?](#what-is-gash)
- [Why GASH?](#why-gash)
- [How it works?](#how-it-works)
- [Future Plans](#future-plans)
- [Policy File Reference](#policy-file-reference)
- [API Reference](#api-reference)
- [Deploy](#deploy)
- [Testing](#testing)

## What is GASH?

GASH is an user authorization tool for microservices, highly inspired by such technologies as [`Google Zanzibar`](https://zanzibar.academy/), [`OPA`](https://www.openpolicyagent.org/) and [`OPAL`](https://opal.ac/). Our main goal is to create an open-source, easy-to-use and flexible service , that provides an async API (for now [`RabbitMQ`](https://www.rabbitmq.com/) only, but other brokers and protocols support is assumed) and implements RBAC (Users in GASH have roles, that define their rights opportunities according to the policy), a little ABAC (all entities, that will be described below, have basic attributes, that are defined in policy) and ReBAC (all entities are stored in graph-based db, and subject will only granted with permit, if it is linked to object, wheather directly or not).

## Why GASH?

...

## How it works?

...

## Future Plans

...

## Policy File Reference

...

## API Reference

...

## Deploy

...

## Testing

...

