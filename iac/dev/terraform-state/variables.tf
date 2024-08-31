variable tf_state_rg {
    type = string
    default = "tf_state_rg"
    description = "Resource Group name for the terraform backend"
}

variable tf_state_location {
    type = string
    default = "East US"
    description = "Location of the RG and the storage account for terraform backend"
}

variable tf_state_storage_acc {
    type = string
    default = "tf_state_storage_acc"
    description = "Storage account name for the terraform backend"
}

variable tf_state_storage_acc_container {
    type = string
    default = "tf_state_storage_acc_container"
    description = "Storage account container name for the terraform backend"
}

variable tf_state_storage_environment {
    type = string
    default = "dev"
    description = "Environment name for the terraform backend"
}