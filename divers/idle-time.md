az containerapp show -n frontend -g RG-SIMPLON-CERTIF > app.yaml
az containerapp update -n frontend -g RG-SIMPLON-CERTIF --yaml app.yaml
az containerapp revision list -n frontend -g RG-SIMPLON-CERTIF --query "[0].template.scale.rules"
az containerapp show -n frontend -g RG-SIMPLON-CERTIF --query "properties.template.scale.rules"

az containerapp list --environment cae-simplon-certif -g RG-SIMPLON-CERTIF  --query "properties.template.containers[].name"
az containerapp list --environment cae-simplon-certif -g RG-SIMPLON-CERTIF  --query "[].name" -o table