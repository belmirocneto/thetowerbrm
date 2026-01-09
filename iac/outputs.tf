output "resource_group_name" {
  description = "Resource group name"
  value       = azurerm_resource_group.main.name
}

output "frontend_url" {
  description = "Frontend URL"
  value       = "https://${azurerm_static_web_app.frontend.default_host_name}"
}

output "backend_url" {
  description = "Backend API URL"
  value       = "https://${azurerm_linux_function_app.backend.default_hostname}/api"
}

output "database_host" {
  description = "PostgreSQL host"
  value       = azurerm_postgresql_flexible_server.main.fqdn
  sensitive   = true
}

output "static_web_app_token" {
  description = "Static Web App deployment token"
  value       = azurerm_static_web_app.frontend.api_key
  sensitive   = true
}

output "function_app_name" {
  description = "Function App name"
  value       = azurerm_linux_function_app.backend.name
}

output "application_insights_key" {
  description = "Application Insights instrumentation key"
  value       = azurerm_application_insights.main.instrumentation_key
  sensitive   = true
}