{{- define "shikybox.name" -}}
shikybox
{{- end }}

{{- define "shikybox.fullname" -}}
{{ .Release.Name }}
{{- end }}

{{- define "shikybox.labels" -}}
app.kubernetes.io/name: {{ include "shikybox.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: shikybox-platform
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
{{- end }}

{{- define "shikybox.selectorLabels" -}}
app.kubernetes.io/name: {{ include "shikybox.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
