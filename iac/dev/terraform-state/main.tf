data "azurerm_client_config" "config"{}

resource "azurerm_resource_group" "tfstate" {
  name     = var.tf_state_rg
  location = var.tf_state_location
}

resource "azurerm_storage_account" "tfstate" {
  name                     = var.tf_state_storage_acc
  resource_group_name      = azurerm_resource_group.tfstate.name
  location                 = azurerm_resource_group.tfstate.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  allow_nested_items_to_be_public = false

  tags = {
    environment = var.tf_state_storage_environment
  }
}

resource "azurerm_storage_container" "tfstate" {
  name                  = "tfstate"
  storage_account_name  = azurerm_storage_account.tfstate.name
  container_access_type = "private"
} 
