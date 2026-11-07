# ShikyBox Helm Chart

This chart deploys the complete ShikyBox application and monitoring platform.

## Table of Contents

- [Components](#components)
- [Prerequisites](#prerequisites)
- [Validate](#validate)
- [Configure the Gmail Secret](#configure-the-gmail-secret)
- [Install](#install)
- [Upgrade](#upgrade)
- [Rollback](#rollback)
- [Uninstall](#uninstall)

## Components

- ShikyBox with three replicas
- Prometheus with Kubernetes discovery and five alert rules
- Grafana with the provisioned ShikyBox Operations Dashboard
- Alertmanager with warning and critical routing
- Persistent storage for Prometheus, Grafana, and Alertmanager
- Optional Gmail SMTP notification integration through an existing Kubernetes Secret

## Prerequisites

- Kubernetes
- Helm 3
- kubectl
- The `shikybox:1.0.0` image available to the cluster
- The `shikybox-email` Secret when external email is enabled

## Validate

    helm lint helm/shikybox

    helm template shikybox helm/shikybox \
      > /tmp/shikybox-rendered.yaml

    kubectl apply \
      --dry-run=client \
      -f /tmp/shikybox-rendered.yaml

## Configure the Gmail Secret

Create the monitoring namespace:

    kubectl create namespace monitoring-helm

Allow Helm to manage the namespace:

    kubectl label namespace monitoring-helm \
      app.kubernetes.io/managed-by=Helm \
      --overwrite

    kubectl annotate namespace monitoring-helm \
      meta.helm.sh/release-name=shikybox-helm \
      meta.helm.sh/release-namespace=default \
      --overwrite

Load the Gmail App Password:

    read -s -p "Paste the Gmail App Password: " GMAIL_APP_PASSWORD
    echo

    GMAIL_APP_PASSWORD="${GMAIL_APP_PASSWORD// /}"

Create the external Secret:

    kubectl create secret generic shikybox-email \
      -n monitoring-helm \
      --from-literal=smtp-password="$GMAIL_APP_PASSWORD"

    unset GMAIL_APP_PASSWORD

The Gmail App Password is not stored in the chart or repository.

## Install

    helm install shikybox-helm helm/shikybox \
      --set namespaces.application=shikybox-helm \
      --set namespaces.monitoring=monitoring-helm \
      --set shikybox.service.nodePort=30180 \
      --set prometheus.service.nodePort=30190 \
      --set grafana.service.nodePort=30130 \
      --set alertmanager.service.nodePort=30193 \
      --wait \
      --timeout=10m

## Upgrade

Scale ShikyBox from three to four replicas:

    helm upgrade shikybox-helm helm/shikybox \
      --reuse-values \
      --set shikybox.replicaCount=4 \
      --wait \
      --timeout=5m

## Rollback

Review the release history:

    helm history shikybox-helm

Rollback to the previous healthy revision:

    helm rollback shikybox-helm 2 \
      --wait \
      --timeout=5m

The revision number may differ in another environment. Use `helm history shikybox-helm` to identify the desired healthy revision before running the rollback.

## Uninstall

    helm uninstall shikybox-helm

Delete the external Gmail Secret separately if it is no longer required:

    kubectl delete secret shikybox-email \
      -n monitoring-helm

The Gmail App Password is not stored in this chart. The chart references the existing Secret configured through `alertmanager.email.existingSecret`.
