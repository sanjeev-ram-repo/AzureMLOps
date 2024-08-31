data "azurerm_client_config" "config"{}

resource "azurerm_resource_group" "rg" {
  name     = var.mlops_rg
  location = var.mlops_loc
}

#Storage account
resource "azurerm_storage_account" "sa" {
    name = "${var.mlops_base_name}mlopsstorage"
    location = azurerm_resource_group.rg.location
    resource_group_name      = azurerm_resource_group.rg.name
    account_tier             = "Standard"
    account_replication_type = "LRS"
}

#Azure keyvault
resource "azurerm_key_vault" "kv" {
  name                = "${var.mlops_base_name}-mlops-kv"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  tenant_id           = data.azurerm_client_config.config.tenant_id
  sku_name            = "standard"
}

# Application Insights
resource "azurerm_application_insights" "app_ins" {
  name                = "${var.mlops_base_name}-mlops-appins"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  application_type    = "web"
}

# Container registry for AML Service
resource "azurerm_container_registry" "acr" {
  name                     = "${var.mlops_base_name}mlopsacr"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  sku                      = "Basic"
  admin_enabled            = true
}

resource "azurerm_machine_learning_workspace" "amlws" {
  name                    = var.aml_ws_name
  location                = azurerm_resource_group.rg.location
  resource_group_name     = azurerm_resource_group.rg.name
  application_insights_id = azurerm_application_insights.app_ins.id
  key_vault_id            = azurerm_key_vault.kv.id
  storage_account_id      = azurerm_storage_account.sa.id
  container_registry_id   = azurerm_container_registry.acr.id
  public_network_access_enabled = true

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_log_analytics_workspace" "alws"{
  name = "${var.mlops_base_name}-mlops-logws"
  location = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku = "PerGB2018"
  retention_in_days = 30
}