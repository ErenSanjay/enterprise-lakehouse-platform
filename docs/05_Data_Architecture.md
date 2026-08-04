# 05 - Data Architecture

**Project:** Enterprise Lakehouse Platform

**Version:** 1.0

**Author:** Sanjay K J

**Date:** August 2026

---

# 1. Purpose

This document defines the enterprise data architecture for the Enterprise Lakehouse Platform.

It describes how enterprise data is ingested, transformed, governed, and consumed across the platform while ensuring scalability, reliability, performance, and security.

The platform follows the **Medallion Architecture (Bronze, Silver, Gold)** using **Delta Lake** as the storage format.

---

# 2. Data Architecture Overview

The platform adopts a layered architecture where data progressively improves in quality and business value.

```text
Enterprise Sources
        │
        ▼
 Landing Zone
        │
        ▼
 Bronze Layer
        │
        ▼
 Silver Layer
        │
        ▼
 Gold Layer
        │
 ┌──────┴──────────┐
 ▼                 ▼
Power BI      ML / AI
```

Each layer has clearly defined responsibilities and ownership.

---

# 3. Data Domains

The platform is organized into business domains.

| Domain | Description |
|----------|-------------|
| Reservations | Reservation transactions |
| Inventory | Room inventory |
| Pricing | Pricing & Rate Programs |
| Customer | Customer Master |
| Property | Hotel Metadata |
| Revenue | Revenue Metrics |
| Configuration | System Configurations |
| Audit | Pipeline Audit Logs |
| Metadata | Pipeline Metadata |

---

# 4. Source Systems

| Source | Type | Frequency |
|----------|------|-----------|
| CRS | CSV | Daily |
| MDP | CSV | Daily |
| Reservation System | Database | Hourly |
| Inventory API | REST API | Hourly |
| Pricing Engine | Database | Daily |
| Historical Benchmark | Delta Table | Daily |

---

# 5. Landing Zone

The Landing Zone stores files exactly as received.

## Responsibilities

- Preserve raw files
- Capture metadata
- Validate filenames
- Detect duplicates
- Enable replay

### Folder Structure

```text
landing/
├── crs/
├── mdp/
├── reservation/
├── pricing/
└── inventory/
```

Files remain immutable.

---

# 6. Bronze Layer

## Purpose

Stores raw enterprise data in Delta format.

### Characteristics

- Raw
- Append-only
- Immutable
- Source-aligned schema
- Full history retained

### Standard Metadata Columns

| Column | Description |
|----------|-------------|
| ingestion_timestamp | Pipeline execution time |
| source_system | Source application |
| file_name | Original file |
| load_date | Processing date |
| batch_id | Pipeline batch identifier |

---

# 7. Silver Layer

## Purpose

Stores validated and standardized datasets.

### Processing

- Schema validation
- Data type normalization
- Duplicate removal
- Null handling
- Business rule validation
- Surrogate key generation
- SCD implementation

### Characteristics

- Trusted data
- Enterprise schema
- Clean datasets
- Ready for downstream processing

---

# 8. Gold Layer

Business-ready analytical datasets.

Examples:

- Revenue KPIs
- Occupancy Metrics
- Pricing Analytics
- Executive Reporting
- ML Features

Consumers:

- Power BI
- Databricks SQL
- Machine Learning
- Data Scientists

---

# 9. Unity Catalog Structure

```text
Enterprise

├── Bronze
│   ├── reservation
│   ├── inventory
│   └── pricing
│
├── Silver
│   ├── reservation
│   ├── inventory
│   └── pricing
│
└── Gold
    ├── analytics
    ├── reporting
    └── revenue
```

---

# 10. Naming Standards

## Tables

```text
bronze_reservation
silver_reservation
gold_daily_revenue
```

## Pipelines

```text
ingest_reservation
transform_pricing
build_gold_revenue
```

## Jobs

```text
daily_bronze_load
silver_validation
gold_reporting
```

---

# 11. Data Modeling Strategy

| Layer | Modeling Strategy |
|---------|------------------|
| Bronze | Source-Oriented |
| Silver | Normalized |
| Gold | Star Schema |

---

# 12. Fact Tables

Examples

- Fact Reservation
- Fact Revenue
- Fact Pricing
- Fact Occupancy

Characteristics

- Incremental
- Partitioned
- Large volume
- Optimized for analytics

---

# 13. Dimension Tables

Examples

- Customer
- Hotel
- Room Type
- Bed Type
- Rate Program
- Calendar

Dimensions use surrogate keys.

---

# 14. Slowly Changing Dimensions

Supported Strategy:

- SCD Type 2

Standard Columns

- Effective Date
- Expiration Date
- Current Flag
- Version

---

# 15. Delta Lake Design

All tables are stored using Delta Lake.

Features:

- ACID Transactions
- Time Travel
- MERGE
- Schema Evolution
- OPTIMIZE
- VACUUM

---

# 16. Partition Strategy

Primary partition columns:

- Business Date
- Country
- Region
- Market
- Property

Partitioning follows query access patterns.

---

# 17. File Formats

| Layer | Format |
|---------|--------|
| Landing | CSV / JSON / Parquet |
| Bronze | Delta |
| Silver | Delta |
| Gold | Delta |

---

# 18. Schema Evolution

Supported

- Nullable columns
- Optional attributes
- Backward-compatible changes

Breaking changes require deployment approval.

---

# 19. Data Quality Strategy

Validation includes:

- Schema validation
- Null checks
- Duplicate detection
- Referential integrity
- Range validation
- Business rule validation

Invalid records are quarantined.

---

# 20. Metadata Management

Managed metadata includes:

- Source information
- Pipeline configuration
- Watermarks
- Batch history
- Audit logs
- Processing metrics

---

# 21. Data Retention

| Layer | Retention |
|---------|-----------|
| Landing | 30 Days |
| Bronze | Permanent |
| Silver | Permanent |
| Gold | Permanent |
| Audit | 365 Days |

---

# 22. Backup and Recovery

Recovery mechanisms include:

- Delta Time Travel
- Version History
- Automated Snapshots
- Disaster Recovery
- Multi-environment deployment

---

# 23. Data Lineage

```text
Source Systems
      │
      ▼
Landing
      │
      ▼
Bronze
      │
      ▼
Silver
      │
      ▼
Gold
      │
      ▼
Power BI / AI
```

Lineage supports governance and impact analysis.

---

# 24. Future Expansion

The platform supports future capabilities:

- Real-time Streaming
- CDC
- Feature Store
- Data Sharing
- Data Mesh
- Vector Search
- Semantic Layer
- Multi-cloud Deployment

---

# 25. Design Principles

- Single Source of Truth
- Immutable Raw Data
- Layered Processing
- Metadata-driven Pipelines
- Idempotent Processing
- Automated Quality Validation
- Secure Access Control
- Enterprise Observability
- Scalable Architecture

---

# 26. Summary

The Enterprise Lakehouse Platform follows a modern Medallion Architecture built on Delta Lake.

By separating raw ingestion, validation, business transformation, and analytical consumption into independent layers, the platform delivers high-quality, governed, scalable, and maintainable data products that serve reporting, analytics, and AI workloads.