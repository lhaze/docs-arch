<!-- markdownlint-disable MD001 MD012 MD024 MD028 -->
# Architecture Principles: Microservices

---

#### Martin Fowler, [*Characteristics of a Microservice Architecture*](https://martinfowler.com/articles/microservices.html)

> - Componentization via Services
> - Organized around Business Capabilities
> - Products not Projects
> - Smart endpoints and dumb pipes
> - Decentralized Governance
> - Decentralized Data Management
> - Infrastructure Automation
> - Design for failure
> - Evolutionary Design



##### Organized around Business Capabilities

> Any organization that designs a system (defined broadly) will produce a design whose structure is a copy of the organization's communication structure.
>
> -- Melvin Conway, 1968



##### Organized around Business Capabilities

![Conway's Law Disorganization](images/oabc1.png)



##### Organized around Business Capabilities

![Conway's Law Organization](images/oabc2.png)



##### Smart Endpoints & Dumb Pipes

> Applications built from microservices aim to be as decoupled and as cohesive as possible - they own their own domain logic and act more as filters in the classical Unix sense - receiving a request, applying logic as appropriate and producing a response. These are choreographed using simple RESTish protocols rather than complex protocols such as WS-Choreography or BPEL or orchestration by a central tool.



##### Design for failure

> Any service call could fail due to unavailability of the supplier, the client has to respond to this as gracefully as possible. Since services can fail at any time, it's important to be able to detect the failures quickly and, if possible, automatically restore service.



##### Design for failure - Synchronous calls considered harmful

> Any time you have a number of synchronous calls between services you will encounter the multiplicative effect of downtime. Simply, this is when the downtime of your system becomes the product of the downtimes of the individual components. You face a choice, making your calls asynchronous or managing the downtime.

> At www.guardian.co.uk they have implemented a simple rule on the new platform - one synchronous call per user request while at Netflix, their platform API redesign has built asynchronicity into the API fabric.
