# Self-Hosted HTTP Adapter Notes

## Purpose

This directory shows the minimal shape of a generic HTTP adapter for a self-hosted AWC worker.

## What it should do

- read invocation and healthcheck URLs from `metadata.platform_hints`;
- pass task/action/confidence data to the worker over HTTP;
- keep protocol validation and policy truth in `awc-spec`; and
- avoid introducing a hosted runtime abstraction or platform review logic.

## What it does not do

- no worker hosting;
- no authentication broker;
- no retry/orchestration system; and
- no platform ranking or review logic.
