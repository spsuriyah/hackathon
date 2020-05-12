#!/bin/bash  
echo "Executing ansible playbook to installing ssm agent in host machine"

ansible-playbook ssm_agent.yml -i host

echo "SSM_agent installation completed"

echo "Executing ansible playbook to create ssm document"

ansible-playbook ssm_document.yml -v 

echo "Document creation completed"
