# Secure GenAI Gateway

A learning project exploring how to secure access to a GenAI/LLM API using AWS API Gateway and IAM — controlling who can call the AI endpoint, rate-limiting requests, and logging usage for monitoring.

This project is an early exploration of a growing area in cloud security: securing AI/LLM integrations, not just traditional cloud infrastructure.

## The Problem

As companies plug LLMs into their products, the API endpoints that expose them become a new attack surface — unrestricted access, prompt injection, and data leakage are real emerging risks. This project is a first, small step toward understanding how to put basic security controls in front of an AI endpoint.

## What This Project Does (current scope)

- Routes requests to an LLM API through AWS API Gateway instead of exposing it directly
- Uses IAM-based authentication to control who can call the endpoint
- Logs every request via CloudWatch for basic monitoring/auditing
- Applies basic rate limiting to prevent abuse

## How It Works

- **API Gateway** sits in front of the LLM API call, acting as a controlled entry point
- **IAM policies** restrict which identities are allowed to invoke the endpoint
- **CloudWatch Logs** record each request for later review
- A Python Lambda function handles the actual call to the LLM API

## What I Learned (so far)

This project is helping me understand that securing AI tools uses the same fundamentals as securing any cloud API — IAM, logging, and access control — with a few new risks layered on top, like prompt injection, that traditional cloud security doesn't cover yet.

## Status

**Early-stage / in progress.** This is the most ambitious of my current projects and is being built incrementally as I learn more about both AWS API security and LLM-specific risks. Not yet a complete, deployable system — currently documenting architecture and building the first working version of the gateway.

## Tech Used

Python, AWS API Gateway, AWS IAM, AWS Lambda, Docker, GitHub Actions

## Author 

Vishal Ranjan 