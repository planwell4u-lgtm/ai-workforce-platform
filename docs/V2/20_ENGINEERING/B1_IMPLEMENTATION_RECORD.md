# B1 Implementation Record — Tenant-Aware Identity and API Entry

**Status:** Implemented locally; pending owner review and controlled-environment release evidence.  
**Owner:** Platform Foundation and Security.  
**Date:** 2026-08-10

## Decisions and scope

- `GET /v1/tenant-context` is the first protected route.
- The controlled B1 sandbox verifies short-lived signed bearer tokens for one human and one workload identity. The API never issues tokens.
- Tenant and permission facts come only from the server-owned membership directory; client tenant values are not authority.
- B1 deliberately has no persistence or external identity-provider integration. B2 replaces the in-memory directory; release requires an approved issuer adapter and secret-manager key material.
- Audit evidence records a safe reason category, correlation, route, and allowed principal/tenant references; it never records bearer tokens.

## Validation

`tests/backend/test_b1_api.py` proves authorized human/workload access, missing/expired and wrong-environment identity rejection, revoked membership, insufficient permission, tenant resolution, correlation, and audit evidence.

## Authority and follow-up

This implements the B1 acceptance criteria in `01_FIRST_VERTICAL_SLICE_IMPLEMENTATION_BACKLOG.md`. Before release, confirm the approved identity issuer, tenant/membership source, signing-key custody and rotation, audit retention sink, and controlled sandbox environment.
