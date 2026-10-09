# Review and deployment

All tasks are open. The original brief requires explicit owner approval before production deployment. Prepare the complete reviewable implementation and evidence before requesting that approval.

## D01 — Reviewable change and outstanding decisions

- [ ] Prepare the change in the dedicated implementation branch with a clear summary of resulting behavior.
- [ ] Provide proposed/implemented site maps, migration ledger, preservation report, verification report, and significant technical/content changes.
- [ ] Separate remaining factual/publication decisions from technical findings and excluded external/deployed checks.
- [ ] Inspect the outgoing diff for accidental private planning material, unrelated user changes, and unexplained content deletion.
- [ ] Record the intended deployable revision and recoverable previous version.

**Outputs:** A concrete review package or draft PR, plus the final owner review list. Creating a remote PR/publishing repository content should follow the authorization available at execution time.

**Done when:** The owner can assess the final content, behavior, evidence, limitations, and rollback plan without reconstructing the development history. Depends on V04.

## D02 — Production deployment approval

- [ ] Identify the existing production target and deployment mechanism from authorized local configuration or owner information; do not infer hosting from a commented workflow.
- [ ] Present the exact revision, deployment action, material unresolved issues, and rollback plan.
- [ ] Obtain and record explicit owner approval before production deployment.

**Output:** Approval tied to a concrete revision and deployment target/action.

**Done when:** Required production authorization has been received. Silence or a completed review package is not approval. Depends on D01.

## D03 — Deployment, verification, and rollback readiness

- [ ] Deploy the approved revision through the established mechanism without replacing hosting unnecessarily.
- [ ] Verify the approved production target's core pages, route compatibility, themes, downloads, and error behavior within the authorized release scope.
- [ ] Record deployed revision, time, verification results, and any environment-specific differences.
- [ ] Retain the previous version and apply the documented rollback if release checks expose a material failure.
- [ ] Update task statuses and close the final change summary with any remaining explicitly excluded checks.

**Outputs:** Deployment record, production verification evidence, and usable rollback information.

**Done when:** The approved revision operates as expected and content/route/download preservation holds in production. Document links remain ignored; inspecting the release target does not authorize following external document links. Depends on D02.
