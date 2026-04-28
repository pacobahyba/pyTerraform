variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "enable_public_backend" {
  description = "Permite invocacao publica no Cloud Run (allUsers)."
  type        = bool
  default     = false
}

variable "enable_public_frontend" {
  description = "Permite leitura publica do bucket do frontend (allUsers)."
  type        = bool
  default     = false
}

variable "frontend_cors_origins" {
  description = "Lista de origens permitidas no CORS do bucket frontend."
  type        = list(string)
  default     = ["http://localhost:3001"]
}
