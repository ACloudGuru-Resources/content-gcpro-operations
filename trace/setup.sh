#!/bin/bash
################## Set up service a ###########################

echo "Creating service a"
kubectl apply -f app/acg-service-a.yaml

################## Set up service b ###########################
echo "Fetching the external IP of service a"
endpoint=""
for run in {1..20}
do
  echo "Attempt #${run} to fetch the external IP of service a..."
  sleep 5
  endpoint=`kubectl get svc cloud-trace-acg-a -ojsonpath='{.status.loadBalancer.ingress[0].ip}'`
  if [[ "$endpoint" != "" ]]; then
    break
  fi
done

if [[ "$endpoint" == "" ]]; then
  echo "Unable to get external IP for service cloud-trace-acg-a"
  exit 1
fi

echo "Passing external IP for the first service ${endpoint} to the second service template"
sed "s/{{ endpoint }}/${endpoint}/g" app/acg-service-b.yaml.template > app/acg-service-b.yaml
kubectl apply -f app/acg-service-b.yaml
rm app/acg-service-b.yaml

################## Set up service c ###########################
echo "Fetching the external IP of service b"
endpoint=""
for run in {1..20}
do
  echo "Attempt #${run} to fetch the external IP of service b..."
  sleep 5
  endpoint=`kubectl get svc cloud-trace-acg-b -ojsonpath='{.status.loadBalancer.ingress[0].ip}'`
  if [[ "$endpoint" != "" ]]; then
    break
  fi
done

if [[ "$endpoint" == "" ]]; then
  echo "Unable to get external IP for service cloud-trace-acg-a"
  exit 1
fi

echo "Passing external IP for the service b ${endpoint} to the service c"
sed "s/{{ endpoint }}/${endpoint}/g" app/acg-service-c.yaml.template > app/acg-service-c.yaml
kubectl apply -f app/acg-service-c.yaml
rm app/acg-service-c.yaml

echo "Successfully deployed all services"
