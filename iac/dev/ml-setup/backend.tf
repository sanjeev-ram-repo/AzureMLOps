terraform {
  backend "azurerm" {
    resource_group_name   = "$(var.tf_state_rg)"
    storage_account_name  = "$(var.tf_state_storage_account)"
    container_name       = "$(var.tf_state_container)"
    key                  = "$(var.tf_state_file_name)" #This will be the file name of .tfstate
  }
}
