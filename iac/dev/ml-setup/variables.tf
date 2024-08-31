# Start of declaration of TF State Variables
variable tf_state_rg {
    type = string
    default = "tf_state_rg"
    description = "Resource Group name for the terraform backend"
}

variable tf_state_location {
    type = string
    default = "tf_state_location"
    description = "Resource Group location for the terraform backend"
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

variable tf_state_file_name {
    type = string
    default = "dev"
    description = "File name for .tfstate file"
}

#Start of instance variables

variable mlops_rg {
    type = string
    default = "mlops-rg"
    description = "RG name for the MLOps instances"
}

variable mlops_loc {
    type = string
    default = "East US"
    description = "Location of the RG"
}

variable mlops_base_name {
    type = string
    default = "mlopsxsanjeev"
    description = "Prefix to be attached to all the instances"
}

variable aml_ws_name {
    type = string
    default = "mlopsxsanjeevxaml"
    description = "Azure Machine Learning workspace name"
}