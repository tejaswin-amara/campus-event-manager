# Stable version record

This document records the version policy for the handout-compliant production website. The target is the latest **stable and compatible** release, not an unreleased milestone or a version that forces a second application stack into the deployment.

## Production website versions

| Component | Previous target | Current target | Decision |
| --- | --- | --- | --- |
| Java runtime/compiler | Java 21 | **Java 25.0.3 LTS line** | Upgraded the Maven property, local validation toolchain, CI, and container images |
| Spring Boot | 3.4.13 | **4.1.0** | Upgraded the parent and validated the existing MVC, JPA, Security, Actuator, Flyway, Thymeleaf, and test stack |
| Springdoc OpenAPI | 2.8.5 | **3.1.0** | Upgraded for the Spring Boot 4 generation |
| Resilience4j | 2.2.0 / Spring Boot 3 adapter | **2.4.0 / Spring Boot 4 adapter** | Changed to `resilience4j-spring-boot4` because the application now targets Spring Boot 4 |
| Bucket4j | 8.7.0 | **8.10.1** | Upgraded the explicit rate-limiting dependency |
| Logstash Logback encoder | 7.4 | **9.0** | Upgraded the structured logging encoder |
| JaCoCo | 0.8.12 | **0.8.15** | Upgraded to the stable Java 26-capable release line while compiling the application on Java 25 |
| Maven Surefire | 3.5.2 | **3.5.4** | Upgraded to the latest stable patch line; the newer 3.6.0-M1 milestone is intentionally not used |
| Maven Wrapper distribution | 3.9.6 | **3.9.11** | Upgraded the reproducible build tool distribution |
| MySQL | 8.0.36 | **8.4 LTS** | Upgraded Compose and CI to the current long-term-support database line |
| Flyway integration | Direct Flyway libraries | **Spring Boot 4 `spring-boot-starter-flyway` + `flyway-mysql` 12.4.0** | Uses Boot 4’s modular auto-configuration plus the MySQL database module so MySQL 8.4 is recognized before Hibernate validation |
| GitHub Actions | checkout/setup/artifact/dependency-review/container majors 4/4/4/4/6 | **7/5/7/5/7** | Upgraded to the current stable action majors reported by GitHub releases |
| Container runtime | Eclipse Temurin Java 21 JDK/JRE Alpine | **Eclipse Temurin Java 25 JDK/JRE Alpine** | Keeps the build and runtime image aligned with the compiler target |

## Firebase-Addition reference repository

The Firebase-Addition repository was used as a product and architecture reference, not as a second production runtime. Its React/Firebase package manifests and lockfile are therefore not copied into the Spring website. The reference repository currently has an unsynchronized frontend lockfile: `npm ci` refuses to install because the lock is missing or mismatching `@emnapi` entries. Its Cloud Functions workspace installs and builds successfully when isolated.

The final website deliberately has no Firebase SDK, Firestore rules, Firebase service account, Cloud Functions deployment, mock Stripe endpoint, or client-side role authority. The portable recommendation concept has been rewritten as tested Java/MySQL logic, and the existing calendar/registration-link QR UX is retained. Firebase waitlisting, attendance tickets, certificates, FCM notification, social graph, and payments remain documented future bounded contexts until the relational model and security ownership are implemented end to end.

## Compatibility policy

A version is adopted only when it is stable, available from its official distribution channel, compatible with the application’s current architecture, and validated by the complete Maven verification suite, runtime smoke checks, load check, and secret-pattern review. Milestones, release candidates, and unrelated framework migrations are not introduced merely to make a version number look newer.

## Verification evidence

The upgrade is validated by `./mvnw -B verify` on Java 25, by the CI contract against MySQL 8.4, by the `flyway-mysql` 12.4.0 module resolving in Maven, by a packaged application running on an isolated port, by the health/OpenAPI smoke script, and by the concurrent health load script. The latest GitHub Actions repair run [32272882649](https://github.com/tejaswin-amara/campus-connect/actions/runs/32272882649) passed the CI build, tests, coverage, and container-build path. The sandbox’s available Ubuntu server is MySQL 8.0, which Flyway 12 intentionally rejects; local code verification can therefore use a manually migrated schema with Flyway disabled, while the committed CI/Compose path remains MySQL 8.4 and exercises automatic migrations. The test suite includes the hybrid recommendation tests and remains above the documented JaCoCo thresholds.

## References

[1]: https://spring.io/blog/2026/06/10/spring-boot-4 "Spring Boot 4.1.0 available now"
[2]: https://docs.spring.io/spring-boot/system-requirements.html "Spring Boot system requirements"
[3]: https://openjdk.org/projects/jdk/25/ "OpenJDK JDK 25 project"
[4]: https://maven.apache.org/docs/3.9.11/release-notes.html "Apache Maven 3.9.11 release notes"
[5]: https://www.jacoco.org/jacoco/trunk/doc/changes.html "JaCoCo change history"
[6]: https://central.sonatype.com/artifact/io.github.resilience4j/resilience4j-spring-boot4/2.4.0 "Resilience4j Spring Boot 4 artifact"
[7]: https://www.npmjs.com/package/firebase "Firebase JavaScript SDK package"
[8]: https://nodejs.org/en/about/previous-releases "Node.js release schedule"
[9]: https://github.com/tejaswin-amara/Campus-Connect-Firebase-Addition "Firebase-Addition reference repository"
