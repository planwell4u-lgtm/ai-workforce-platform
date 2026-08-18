# 04_DATA_VECTOR_AND_PGVECTOR_ARCHITECTURE

**Version:** 1.1  
**Status:** Approved  
**Owner:** Data Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines Data Platform's pgvector architecture for derived embeddings, vector indexes, similarity operations, rebuilds, invalidation, and operational evidence.

pgvector is a PostgreSQL extension selected under ADR-005. It supports vector representations; it does not own Knowledge or Memory truth, retrieval eligibility, subject access, publication, admission, or lifecycle.

# Purpose

Provide a tenant-safe, portable, observable vector foundation without making a vector row, nearest-neighbor result, embedding model, or index a public identity or authorization decision.

# Principles

## Derived Representation Only

Every vector links to an owning domain canonical reference, tenant/environment, representation version, embedding model/dimension, source revision, classification, lifecycle, and invalidation/deletion evidence. It is rebuildable and removable.

## Similarity Is Candidate Evidence

Similarity retrieves candidate representations. Knowledge/Memory and current tenant/subject/purpose/access contracts decide whether any candidate is eligible or returned.

## Filter Before Exposure

Tenant/environment and applicable domain access/lifecycle filters are mandatory. Index behavior, approximate search, or an externally supplied vector never bypasses those filters.

# Model

| Entity | Meaning | Must not become |
|---|---|---|
| VectorRepresentation | Derived embedding plus protected lineage. | Canonical record or access grant. |
| VectorIndexProfile | Approved model/dimension/distance/index/configuration version. | Domain retrieval policy. |
| VectorBuildRun | Evidence of embedding/index build, validation, and coverage. | Publication/admission decision. |
| VectorInvalidation | Link from source/lifecycle change to non-use/rebuild/delete requirement. | Deletion-policy authority. |
| SimilarityQueryEvidence | Protected query/profile/filter/result-quality evidence. | User-visible result or authorization. |

# Storage and Query Rules

Vectors use Data-owned pgvector configuration and versioned index profiles. Each representation records model, dimension, distance metric, source/revision, tenant/environment, classification, freshness, and lifecycle linkage. Schema/index changes are migrations with compatibility, capacity, rollback, and rebuild plans.

Queries are server-side, schema-validated, rate/cost bounded, tenant-filtered, and correlated to an approved domain request. Client, Agent, provider, or channel code does not query pgvector directly. Result candidates are revalidated by the owning domain before use.

# Lifecycle, Performance, and Recovery

Source correction, suppression, expiry, deletion, hold, access change, migration, or tenant lifecycle event invalidates affected vectors promptly. Logical non-use takes precedence; physical removal/rebuild follows governed lifecycle and evidence. Backup/restore revalidates current lifecycle/access and never resurrects ineligible vectors.

Data monitors build/index freshness, query latency, recall/quality evidence provided by owning domains, index size, capacity, filter behavior, invalidation lag, failure, and recovery. Approximate index settings may improve performance but cannot weaken filtering, tenant isolation, or domain eligibility.

# Boundaries

Knowledge owns source/provenance/publication/retrieval/citation rules. Memory owns subject-bound admission/use/lifecycle/retrieval rules. Security and Platform Foundation supply access and tenant facts. Data owns pgvector mechanism, lineage, capacity, and operational controls.

# Required Implementation Artifacts

| Artifact | Purpose |
|---|---|
| Vector profile standard | Defines model/dimension/distance/index/version and compatibility. |
| Lineage/invalidation contract | Defines source linkage, non-use, rebuild, deletion, hold, restore evidence. |
| Vector query service contract | Defines validated filters, scope, limits, result evidence, and domain revalidation. |
| Vector conformance suite | Proves tenant filtering, lifecycle, migration, recovery, performance, and no direct access. |

# Anti-Patterns

## Nearest Result Is Automatically Eligible

Similarity is candidate evidence; owning-domain and access controls decide use.

## Vector ID Is Domain Identity

It is an internal derived reference only.

## Rebuild Restores Deleted Data

Rebuild/restore first validates lifecycle, deletion, hold, tenant, and access status.

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-07 | Created Data pgvector architecture for derived representations, indexing, filtering, lifecycle, performance, and recovery. |
| 1.1 | 2026-08-07 | Approved after completeness, ownership, and long-term maintainability review. |
