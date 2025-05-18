# Delivery State Machine Service - System Design

## High Level Introduction
This e-commerce app is for a business-to-customer model. It allows customers to browse and to buy books from my bookstore on a web app. Once a customer has selected books and made the payment, The books will be packed up and a delivery will be arranged from the physical book store to the address of the customer. As you see, this is a typical simplified e-commerce app, whose core functions can be split into sub-domains like product domain, customer domain, ordering domain, payment domain, delivery domain, and order management domain, in the language of micro-service software. Peripheral domains like operation domain (used by internal operators), communication domain, recommendation system domain are not included in this product design. For each domain, there is a domain owner, and a few microservices. 

Read the entity relation model of the core domains and core entities in [entity_relationship_model.puml](resources/entity_relationship_model.puml)

## System Architecture

### Service Components
- **API Layer**: FastAPI application handling HTTP requests and WebSocket connections
- **State Machine Engine**: Core business logic for state transitions
- **Event Processor**: Celery workers for async event processing
- **Message Queue**: RabbitMQ for event-driven communication
- **Database**: PostgreSQL for persistent storage
- **Cache Layer**: Redis for caching frequently accessed data
- **Monitoring**: Prometheus metrics and Grafana dashboards
- **Logging**: ELK stack for centralized logging

### Integration Points
- Payment Service (Event Consumer)
- Order Management Service (Event Producer)
- Third-party Delivery Partner API
- Customer Service API
- Operator Dashboard API

## Tech Design Specs
For this delivery-state-machine service, it will focus only on the state machine of the delivery domain. The followings are the business flow the delivery-state-machine service should cover:
- A delivery order should be created, once the user has made the payment of an ordering of books online. A delivery order record should be linked to only one ordering record, one customer, and one payment. That means, the delivery_order relational table should contain the foreign key of ordering record in the relational data model design
- In the happy path, a delivery order under goes the following states: CREATED, PICKED_UP, DELIVERED (confirmed by the third-party delivery partner), DELIVERY_CONFIRMED (confirmed by customer). Read [delivery_order_state_machine_happy_path.puml](resources/delivery_order_state_machine_happy_path.puml)
- This state machine should handle some simple exceptions. For example, in 1% probability, the delivery may fail, due to wrong customer address etc. Then the delivery order state will change from PICKED_UP to DELIVERY_FAILED. The DELIVERY_FAILED state should always be linked to a failure reason enum. Read [delivery_order_state_machine_exception.puml](resources/delivery_order_state_machine_exception.puml)
- Operators of my company should step in whenever a delivery state deviate out of the happy path. Take the above unhappy path for example, the delivery order state should be changed from DELIVERY_FAILED to PENDING_BY_OPERATOR. 
- The state machine graph of the delivery should be acyclic. For example, if the delivery fails, the delivery order state should not go back from PENDING_BY_OPERATOR to CREATED. We should create a new delivery order record for this ordering instead. So it's a one-to-many relationship between ordering records and delivery order records. 
- Use CORS design pattern for the delivery state events, as to split the write and read. 
- Write the delivery-state-machine service using FastAPI and Celery in Python. 
- Use AWS CloudFormation to maintain the state machine graph version in yaml. 
- The delivery-state-machine service should be listening to the payment service. Once the payment of an ordering is successful, and this is a physical book (not an e-book, according to the product attribute), the delivery order should be created, and a third-party delivery partner will be contacted for this delivery order. 
- Once picked up, the delivery partner will give me a delivery order number, I'll need to persist this delivery order number in my delivery order record, and mark the delivery order record as PICKED_UP. 
- Once delivered, the third-party delivery partner will send us a related message. We'll mark the delivery order as DELIVERED. 
- Once the customer confirms that the physical books have been received, the delivery order state will be transited to DELIVERY_CONFIRMED, and a related message will be sent to the order management microservice

## Non-Functional Requirements

### Performance
- API response time: 95th percentile under 200ms
- Event processing latency: 95th percentile under 500ms
- System should handle up to 1000 concurrent delivery orders
- Database query performance: 95th percentile under 100ms

### Scalability
- Horizontal scaling of API and worker nodes
- Database read replicas for high read loads
- Message queue partitioning for high throughput
- Cache distribution strategy

### Reliability
- 99.9% service availability
- Zero data loss guarantee
- Automatic failover for critical components
- Circuit breakers for external service calls

### Security
- Authentication using OAuth2/JWT
- Role-based access control (RBAC)
- API rate limiting
- Data encryption at rest and in transit
- Audit logging for all state changes

### Monitoring and Observability
- Real-time metrics dashboard
- Alerting system for anomalies
- Distributed tracing
- Error tracking and reporting
- Performance monitoring

## Deployment Strategy
- Containerized deployment using Docker
- Kubernetes orchestration
- Blue-green deployment strategy
- Automated CI/CD pipeline
- Infrastructure as Code (IaC) using AWS CloudFormation

## Disaster Recovery
- Multi-region deployment
- Automated backup strategy
- Recovery point objective (RPO): 5 minutes
- Recovery time objective (RTO): 1 hour

## Testing Strategy
- Unit testing (90% coverage)
- Integration testing
- End-to-end testing
- Performance testing
- Chaos testing
- Security testing

## Documentation
- API documentation (OpenAPI/Swagger)
- Architecture decision records (ADRs)
- Runbooks for common operations
- Troubleshooting guides
- Onboarding documentation

## Future Considerations
- Multi-tenant support
- Internationalization
- Advanced analytics
- Machine learning for delivery optimization
- Blockchain integration for delivery tracking
