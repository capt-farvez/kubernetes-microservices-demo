# Essential statements for problem solving

## Analysis:

- `kubectl get pods -A` (list all pods across all namespaces — quick overview of the entire cluster)
- `kubectl -n <namespace> get pods` (list pods in a specific namespace — check their STATUS, RESTARTS, and AGE)
- `kubectl -n <namespace> logs <podname>` (print the stdout/stderr logs of a pod — first place to look for errors)
- `kubectl -n <namespace> describe pod <podname>` (detailed info about a pod — shows events, conditions, container states, resource limits, and mounts)
- `kubectl -n <namespace> get pod <podname> -o yaml` (full pod spec and status as YAML — useful to see exact config, environment variables, and image tags)
- `kubectl -n <namespace> get events --sort-by='.lastTimestamp'` (list cluster events sorted by time — shows scheduling, pulling, killing, and error events)
- `kubectl -n <namespace> logs <podname> --previous` (view logs from a crashed/restarted container)
- `kubectl -n <namespace> logs <podname> -c <container>` (specific container in a multi-container pod)
- `kubectl -n <namespace> exec -it <podname> -- /bin/sh` (shell into a running container)
- `kubectl top pods -n <namespace>` (check CPU/memory usage)
- `kubectl top nodes` (check node resource usage)
- `kubectl get nodes -o wide` (node status with IPs and versions)

## Networking:

- `kubectl -n <namespace> get svc` (list services)
- `kubectl -n <namespace> get endpoints` (check if services have backing pods)
- `kubectl -n <namespace> port-forward svc/<service> <local-port>:<remote-port>` (forward a service port locally)
- `kubectl -n <namespace> run tmp-debug --rm -it --image=busybox -- wget -qO- http://<service>:<port>` (test service connectivity)

## ConfigMaps & Secrets:

- `kubectl -n <namespace> get configmaps` (list all ConfigMaps — these hold non-sensitive config data like env vars and config files)
- `kubectl -n <namespace> get secrets` (list all Secrets — these hold sensitive data like passwords, tokens, and TLS certs)
- `kubectl -n <namespace> get secret <name> -o jsonpath='{.data}'` (view secret data, base64 encoded)

## Restarting:

- `kubectl -n <namespace> get deployments` (list all deployments — shows READY, UP-TO-DATE, and AVAILABLE replica counts)
- `kubectl rollout restart deployment <deployment name> --namespace <namespace>` (gracefully restart all pods in a deployment — triggers a rolling update with zero downtime)

OR just simply:

- `kubectl -n <namespace> delete pod <podname>` (delete a single pod — the deployment controller will automatically create a fresh replacement)

## Other tips:

If you ever see a pod hanging in "ContainerCreating" and in "describe pod" you see the following event:

  Warning  FailedAttachVolume      25s   attachdetach-controller  Multi-Attach error for volume "xxxxxxxxxxxxxxxxxxxx" Volume is already exclusively attached to one node and can't be attached to another
  
Then find the deployment name and do this:

- `kubectl scale deploy <deployment name> -n <namespace> --replicas=0` (scale down to zero — forces the pod to terminate and release the attached volume)

Then wait for the pod to be deleted and then do:
- `kubectl scale deploy <deployment name> -n <namespace> --replicas=1` (scale back up to one — a fresh pod is created and can now attach the volume cleanly)

## CrashLoopBackOff:

If a pod is in "CrashLoopBackOff":

1. Check logs: `kubectl -n <namespace> logs <podname> --previous`
2. Check events: `kubectl -n <namespace> describe pod <podname>` (look at the Events section)
3. Check if it's an OOM kill: `kubectl -n <namespace> get pod <podname> -o jsonpath='{.status.containerStatuses[0].lastState}'`

## ImagePullBackOff:

If a pod is stuck in "ImagePullBackOff" or "ErrImagePull":

- Verify image name/tag: `kubectl -n <namespace> describe pod <podname>` (check the image field)
- Check image pull secrets: `kubectl -n <namespace> get pod <podname> -o jsonpath='{.spec.imagePullSecrets}'`

## Resource issues:

If pods are stuck in "Pending" due to insufficient resources:

- `kubectl describe node <nodename>` (check Allocatable vs Allocated resources)
- `kubectl get pods -A --field-selector=status.phase=Pending` (find all pending pods)

## Cleanup:

- `kubectl -n <namespace> delete pods --field-selector=status.phase=Failed` (remove all failed pods)
- `kubectl -n <namespace> delete pods --field-selector=status.phase=Succeeded` (remove completed pods)

## Quick health check:

- `kubectl get componentstatuses` (cluster component health)
- `kubectl cluster-info` (cluster info and endpoints)
- `kubectl get all -n <namespace>` (all resources in a namespace)