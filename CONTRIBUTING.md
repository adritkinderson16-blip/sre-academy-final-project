# Contributing to ShikyBox

Thank you for your interest in contributing to ShikyBox.

Suggestions, improvements, bug fixes, monitoring enhancements, and documentation updates are welcome.

## How to Contribute

1. **Fork the repository**

   Use GitHub to create a personal fork of the ShikyBox repository.

2. **Create a feature branch**

   Choose a short name that describes the proposed change.

       git checkout -b feature/add-new-pet-box

3. **Make your changes**

   Please:

   - Follow the existing folder structure and naming conventions.
   - Keep the customer-facing application simple and pet-focused.
   - Write clear comments and documentation.
   - Add or update tests when application behavior changes.
   - Do not commit credentials, tokens, private keys, or customer data.

4. **Validate your changes**

   Run the application tests:

       source .venv/bin/activate
       python -m pytest -v

   If Kubernetes manifests changed, validate them before applying:

       kubectl kustomize kubernetes > /tmp/shikybox-rendered.yaml
       kubectl apply -k kubernetes --dry-run=server

   If monitoring resources changed, validate the relevant Prometheus, Grafana, or Alertmanager configuration.

5. **Commit and push**

       git add .
       git commit -m "Add new ShikyBox feature"
       git push origin feature/add-new-pet-box

6. **Open a pull request**

   Include:

   - A descriptive title
   - A short summary of the change
   - The validation steps performed
   - Screenshots when the user interface or dashboards changed
   - Related issue numbers, if applicable

## Guidelines

- Use clear and professional language.
- Keep changes focused and reproducible.
- Preserve the existing health, readiness, and metrics endpoints.
- Follow Prometheus naming conventions for new metrics.
- Avoid high-cardinality metric labels such as customer names or order IDs.
- Keep Kubernetes resources declarative and compatible with Kustomize.
- Update `README.md` when routes, metrics, alerts, dashboards, or deployment steps change.
- Store implementation screenshots in the `screenshots` directory.
- Never commit passwords, tokens, kubeconfig files, Secret exports, or Terraform state.

## Reviews

Pull requests may receive suggestions before merging to maintain consistency, reliability, and clear documentation across the project.

Thank you for helping improve ShikyBox.
