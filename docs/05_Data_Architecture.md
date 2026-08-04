# 05 - Data Architecture

**Project:** Enterprise Lakehouse Platform

**Version:** 1.0

**Author:** Sanjay K J

**Date:** August 2026

---

# 1. Purpose

This document defines the enterprise data architecture for the Lakehouse Platform.

It describes how business data flows from operational systems into analytical datasets while ensuring scalability, reliability, governance, and data quality.

The architecture follows the Medallion Architecture (Bronze, Silver, Gold) and leverages Delta Lake to provide ACID transactions, schema evolution, versioning, and reliable incremental processing.

This document acts as the foundation for all implementation, orchestration, monitoring, and reporting activities.

---

# 2. Data Architecture Overview

The platform adopts a layered data architecture where datasets progressively improve in quality and business value.

```

```
              Enterprise Sources

                     │

                     ▼

              Landing Zone (Raw Files)

                     │

                     ▼

             Bronze Layer (Raw Delta)

                     │

                     ▼

         Silver Layer (Validated Data)

                     │

                     ▼

       Gold Layer (Business Analytics)

                     │

      ┌──────────────┼───────────────┐
      ▼              ▼               ▼

 Power BI      Databricks SQL     AI / ML

```

Each layer has a clearly defined responsibility and ownership.

---

# 3. Data Domains

The platform organizes datasets by business domain.

| Domain | Description |
|---------|-------------|
| Reservations | Hotel reservation transactions |
| Inventory | Room inventory availability |
| Pricing | Rate plans and pricing rules |
| Customer | Customer master information |
| Property | Hotel and property metadata |
| Revenue | Revenue and occupancy metrics |
| Configuration | Business configuration tables |
| Audit | Pipeline execution logs |
| Metadata | Pipeline configuration and control tables |

Each domain is independently deployable while remaining part of the unified Lakehouse.

---

# 4. Source Systems

The platform ingests data from multiple enterprise systems.

| Source | Type | Frequency |
|---------|------|-----------|
| CRS | Flat Files | Daily |
| MDP | CSV Files | Daily |
| Reservation System | Database | Hourly |
| Inventory System | API | Hourly |
| Pricing Engine | Database | Daily |
| Historical Benchmark | Delta Table | Daily |
| Property Configuration | CSV | On Demand |

Each source maintains independent ingestion pipelines.

---

# 5. Landing Zone

The Landing Zone stores source files exactly as received.

## Responsibilities

- Original file preservation
- Metadata capture
- File validation
- Duplicate detection
- Audit logging

### Folder Structure

```

landing/

crs/

mdp/

reservation/

inventory/

pricing/

```

Files are immutable after ingestion.

---

# 6. Bronze Layer

## Purpose

The Bronze Layer stores raw enterprise data in Delta format.

No business transformations are applied.

### Characteristics

- Immutable
- Append-only
- Source-aligned schema
- Full historical retention
- Delta format

### Standard Columns

| Column | Purpose |
|----------|----------|
| ingestion_timestamp | Pipeline execution timestamp |
| source_system | Source identifier |
| file_name | Source filename |
| load_date | Processing date |
| batch_id | Pipeline batch identifier |

---

# 7. Silver Layer

## Purpose

The Silver Layer contains cleansed and standardized enterprise datasets.

### Processing Activities

- Schema validation
- Data type normalization
- Duplicate removal
- Null handling
- Data quality checks
- Business rule validation
- Surrogate key generation
- Slowly Changing Dimensions

### Characteristics

- Trusted data
- Enterprise standard schema
- Business validation applied
- Optimized for downstream processing

---

# 8. Gold Layer

The Gold Layer exposes business-ready analytical datasets.

## Characteristics

- Fact tables
- Dimension tables
- Aggregated metrics
- KPI datasets
- Reporting models
- AI feature datasets

Typical consumers include:

- Power BI
- Databricks SQL
- Machine Learning
- Data Scientists

---

# 9. Data Catalog

Enterprise datasets are governed using Unity Catalog.

Example hierarchy:

```

Enterprise

├── Bronze

│ ├── reservation

│ ├── pricing

│ ├── inventory

│

├── Silver

│ ├── reservation

│ ├── pricing

│ ├── inventory

│

└── Gold

├── revenue

├── analytics

└── reporting

```

The catalog provides:

- Data discovery
- Lineage
- Access control
- Metadata management

---

# 10. Naming Standards

## Tables

```

bronze_reservation

silver_reservation

gold_daily_revenue

```

---

## Pipelines

```

ingest_reservation

transform_inventory

build_gold_revenue

```

---

## Jobs

```

daily_bronze_load

silver_validation

gold_reporting

```

---

# 11. Data Modeling Strategy

The platform uses multiple modeling techniques depending on the processing stage.

| Layer | Modeling Style |
|---------|----------------|
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

- Large datasets
- Incremental loads
- Partitioned
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

Dimension tables use surrogate keys for analytical joins.

---

# 14. Slowly Changing Dimensions

The platform supports SCD Type 2 where historical tracking is required.

Typical dimensions include:

- Hotel
- Customer
- Rate Program
- Room Configuration

Standard columns:

- Effective Date
- Expiration Date
- Current Flag
- Version

---

# 15. Delta Lake Design

All analytical tables are stored using Delta Lake.

Key capabilities:

- ACID Transactions
- Time Travel
- Schema Evolution
- MERGE Operations
- OPTIMIZE
- VACUUM

Delta format is the default storage format across all layers.

---

# 16. Partition Strategy

Partitioning is applied to improve query performance.

Primary partition columns include:

- Business Date
- Country
- Region
- Property
- Market

Partitioning decisions are based on query access patterns rather than source structure.

---

# 17. File Formats

| Layer | Format |
|---------|---------|
| Landing | CSV / JSON / Parquet |
| Bronze | Delta |
| Silver | Delta |
| Gold | Delta |

Delta is selected to provide transactional consistency and efficient storage.

---

# 18. Schema Evolution

The architecture supports controlled schema evolution.

Supported scenarios:

- New nullable columns
- Optional business attributes
- Backward-compatible changes

Breaking schema changes require version-controlled deployment.

---

# 19. Data Quality Strategy

Quality checks are executed before promotion between layers.

Validation categories:

- Schema validation
- Null checks
- Duplicate detection
- Range validation
- Referential integrity
- Business rule validation

Failed records are quarantined for investigation.

---

# 20. Metadata Management

Pipeline metadata is centrally managed.

Metadata includes:

- Source information
- Pipeline configuration
- Batch history
- Watermarks
- Audit logs
- Processing statistics

Metadata enables reusable, metadata-driven pipelines.

---

# 21. Data Retention

Retention policies vary by layer.

| Layer | Retention |
|---------|-----------|
| Landing | 30 Days |
| Bronze | Permanent |
| Silver | Permanent |
| Gold | Permanent |
| Audit Logs | 365 Days |

Retention is configurable based on regulatory requirements.

---

# 22. Backup and Recovery

Recovery strategy includes:

- Delta Time Travel
- Version History
- Automated Snapshots
- Disaster Recovery Procedures
- Multi-environment Deployment

Recovery objectives are defined according to business criticality.

---

# 23. Data Lineage

Lineage is maintained from ingestion to consumption.

```

Source System

↓

Landing

↓

Bronze

↓

Silver

↓

Gold

↓

Power BI

↓

Business Reports

```

Lineage information supports governance, auditing, and impact analysis.

---

# 24. Future Expansion

The architecture is designed to support future capabilities including:

- Real-time streaming ingestion
- Change Data Capture (CDC)
- Machine Learning Feature Store
- Data Sharing
- Data Mesh
- Generative AI Applications
- Vector Search
- Semantic Layer
- Multi-cloud deployment

---

# 25. Key Design Principles

The data architecture is built on the following principles:

- Single source of truth
- Immutable raw data
- Layered transformations
- Metadata-driven processing
- Idempotent pipelines
- Schema governance
- Automated quality validation
- Secure data access
- Scalability by design
- Enterprise observability

---

# 26. Summary

The Enterprise Lakehouse Platform adopts a scalable, governed, and modular data architecture centered on the Medallion Architecture and Delta Lake.

By separating raw ingestion, validation, business transformation, and analytical consumption into distinct layers, the platform ensures high data quality, operational resilience, and extensibility. This architecture establishes the foundation for the Low-Level Design (LLD) documents, where ingestion pipelines, transformation logic, orchestration, governance, monitoring, and deployment are specified in implementation detail.