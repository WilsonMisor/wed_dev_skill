# SaaS Disaster Recovery

Disaster recovery addresses failures beyond ordinary deployment rollback.

## Plan for applicable scenarios

1. Primary database loss or corruption.
2. Region or data centre outage.
3. Object storage failure.
4. Identity provider outage.
5. Payment provider outage.
6. DNS or certificate failure.
7. Credential compromise.
8. Deployment causing widespread corruption.
9. Queue or worker backlog crisis.
10. Critical vendor outage.

For each scenario define detection, decision owner, containment, recovery source, dependency order, RTO, RPO, communication, verification, and post recovery reconciliation.
