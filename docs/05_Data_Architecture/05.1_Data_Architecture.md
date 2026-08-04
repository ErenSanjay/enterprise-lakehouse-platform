# 05. Data Architecture

**Project:** Enterprise Hospitality Lakehouse Platform

**Document Version:** 1.0

**Author:** Sanjay K J

---

# 1. Purpose

The purpose of this document is to define the enterprise data architecture for the Hospitality Lakehouse Platform.

The platform consolidates operational and analytical data from multiple business systems into a unified Lakehouse built on the Medallion Architecture.

The architecture enables reliable reporting, advanced analytics, machine learning, and enterprise-wide data governance while maintaining scalability, data quality, and operational resilience.

---

# 2. Architecture Principles

The platform is designed around the following principles:

- Single Source of Truth
- Immutable Raw Data
- Metadata-Driven Pipelines
- Incremental Data Processing
- Data Quality by Design
- Secure-by-Default Architecture
- Enterprise Governance
- Scalable Distributed Processing
- Domain-Oriented Data Organization

---

# 3. Business Data Domains

The platform organizes data into business domains instead of application-specific systems.

| Domain | Description |
|----------|-------------|
| Reservations | Hotel reservation transactions |
| Inventory | Room availability and inventory |
| Pricing | Pricing recommendations and rate management |
| Room Configuration | Room types, room pools, bed types, rate programs |
| Property Master | Hotel metadata and hierarchy |
| Customer | Guest information |
| Benchmark | Historical occupancy and pricing benchmarks |
| Calendar | Holidays, seasons and special events |
| Audit | Pipeline execution metadata |
| Metadata | Pipeline configuration and operational metadata |

---

# 4. Source Systems

| Source System | Data Type | Ingestion Method | Frequency | Business Purpose |
|---------------|-----------|------------------|-----------|------------------|
| Property Management System (PMS) | Database | JDBC | Hourly | Reservations and occupancy |
| Central Reservation System (CRS) | CSV / REST API | Auto Loader | Hourly | Reservation transactions |
| Revenue Management System (RMS) | Database | JDBC | Daily | Pricing recommendations |
| Channel Manager | REST API | API | Hourly | OTA pricing and inventory |
| Hotel Configuration System | CSV | Auto Loader | Daily | Room types, room pools, rate programs |
| Enterprise Master Data | Database | JDBC | Daily | Property and organization master data |
| Historical Benchmark Repository | Delta Tables | Unity Catalog | Daily | Historical benchmark metrics |
| External Calendar API | REST API | API | Daily | Holidays and special events |

---

# 5. Data Ingestion Layer

The ingestion layer is responsible for collecting data from enterprise systems and loading it into the Landing Zone.

Supported ingestion mechanisms include:

- Databricks Auto Loader
- JDBC Connectors
- REST APIs
- Delta Sharing
- Batch File Ingestion
- Streaming (future enhancement)

Each ingestion pipeline captures:

- Source metadata
- File metadata
- Processing timestamp
- Batch identifier
- Data lineage information

---

# 6. Landing Zone

The Landing Zone stores incoming files exactly as received from source systems.

## Objectives

- Preserve original data
- Enable replayability
- Support audit requirements
- Capture ingestion metadata
- Isolate ingestion failures

### Folder Structure

```text
landing/

├── reservations/
├── inventory/
├── pricing/
├── room_configuration/
├── property_master/
├── customer/
├── benchmark/
├── calendar/
└── metadata/
```

Files remain immutable and are never modified after ingestion.

---

# 7. Medallion Architecture

The platform follows the Medallion Architecture.

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
 ┌──────┴────────┐
 ▼               ▼
BI Reports     AI / ML
```

---

# 8. Bronze Layer

The Bronze Layer stores raw enterprise data in Delta format.

### Characteristics

- Append-only
- Immutable
- Source-aligned schema
- Full historical retention
- Metadata enriched

Typical metadata columns include:

- ingestion_timestamp
- source_system
- load_date
- batch_id
- file_name

---

# 9. Silver Layer

The Silver Layer contains validated, standardized, and conformed datasets.

Processing activities include:

- Schema validation
- Data cleansing
- Duplicate removal
- Standardization
- Business rule validation
- Null handling
- Data enrichment
- Surrogate key generation
- Slowly Changing Dimension processing

The Silver Layer serves as the enterprise's trusted data foundation.

---

# 10. Gold Layer

The Gold Layer provides business-ready datasets optimized for analytics and reporting.

Examples include:

### Fact Tables

- Fact Reservation
- Fact Revenue
- Fact Pricing
- Fact Occupancy

### Dimension Tables

- Hotel
- Room Type
- Rate Program
- Customer
- Calendar
- Market

Gold datasets are consumed by:

- Power BI
- Databricks SQL
- Machine Learning pipelines
- Executive dashboards
- Data Science workloads

---

# 11. Data Storage Standards

| Layer | Storage Format |
|---------|---------------|
| Landing | CSV / JSON / Parquet |
| Bronze | Delta |
| Silver | Delta |
| Gold | Delta |

---

# 12. Partition Strategy

Large datasets are partitioned using business-friendly attributes.

Primary partition columns include:

- Business Date
- Country
- Region
- Property
- Market

Partitioning decisions are based on expected query patterns and data volume.

---

# 13. Incremental Processing Strategy

Incremental ingestion minimizes unnecessary data processing.

Supported strategies include:

- Watermark Processing
- Merge-based Upserts
- CDC (future enhancement)
- Idempotent Processing
- Incremental Batch Loading

---

# 14. Data Quality Framework

Every pipeline performs automated quality validation.

Validation categories include:

- Schema Validation
- Null Checks
- Duplicate Detection
- Referential Integrity
- Range Validation
- Business Rule Validation

Invalid records are redirected to quarantine datasets for investigation.

---

# 15. Metadata Management

Operational metadata captured includes:

- Pipeline Name
- Batch ID
- Processing Time
- Execution Duration
- Source System
- Row Counts
- Validation Results
- Error Logs
- Pipeline Status

---

# 16. Data Governance

Governance is implemented using Unity Catalog.

Capabilities include:

- Role-Based Access Control
- Catalogs
- Schemas
- Table Permissions
- Column-Level Security
- Row-Level Security
- Data Lineage
- Audit Logs

---

# 17. Security

Security controls include:

- Identity-based Authentication
- Role-Based Authorization
- Encryption at Rest
- Encryption in Transit
- Secret Management
- Private Networking
- Audit Logging

---

# 18. Retention Policy

| Layer | Retention |
|---------|-----------|
| Landing | 30 Days |
| Bronze | Permanent |
| Silver | Permanent |
| Gold | Permanent |
| Audit Logs | 365 Days |

---

# 19. Backup and Recovery

Recovery mechanisms include:

- Delta Time Travel
- Version History
- Automated Snapshots
- Disaster Recovery
- Multi-Environment Deployment

---

# 20. Data Lineage

The platform maintains end-to-end lineage from ingestion to consumption.

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
 ┌──────┴────────┐
 ▼               ▼
Power BI       AI / ML
```

Lineage enables:

- Impact Analysis
- Regulatory Compliance
- Debugging
- Governance
- Operational Monitoring

---

# 21. Future Enhancements

The architecture is designed to support future capabilities including:

- Change Data Capture (CDC)
- Real-Time Streaming
- Delta Live Tables
- Feature Store
- Data Mesh
- Vector Search
- Semantic Layer
- Cross-Cloud Data Sharing

---

# 22. Summary

The Enterprise Hospitality Lakehouse Platform implements a modern Medallion Architecture that separates raw ingestion, standardized processing, and business-ready analytics into clearly defined layers.

The architecture emphasizes scalability, governance, performance, data quality, and maintainability while providing a robust foundation for enterprise reporting, advanced analytics, and AI-driven decision-making.