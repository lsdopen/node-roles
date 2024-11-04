"""
This app watches for new nodes in the Kubernetes cluster
and labels them with the appropriate role label.
"""
import json
from kubernetes import client, config, watch
config.load_incluster_config()
v1 = client.CoreV1Api()
ROLE_LABEL_KEY = "node-group"
def label_node(node_name, key, value):
    """
    Label a node with a key-value pair.
    """
    body = {
        "metadata": {
            "labels": {
                key: value
            }
        }
    }
    try:
        v1.patch_node(node_name, body)
        label_node_response = {
            "status": "success",
            "message": f"Successfully labeled node {node_name} with {key}={value}",
            "node_name": node_name,
            "label": {key: value}
        }
    except client.exceptions.ApiException as e:
        label_node_response = {
            "status": "error",
            "message": f"Failed to label node {node_name}: {e}",
            "node_name": node_name
        }
    return json.dumps(label_node_response)
def watch_new_nodes():
    """
    Watch for new nodes in the cluster 
    and label them with the appropriate role label.
    """
    w = watch.Watch()
    for event in w.stream(v1.list_node):
        node = event["object"]
        node_name = node.metadata.name
        node_role_label = node.metadata.labels.get(ROLE_LABEL_KEY)
        node_role_label_key = f'node-role.kubernetes.io/{node_role_label}'
        event_type = event["type"]

        if event_type == "ADDED":
            labels = set(node.metadata.labels.keys())
            if node_role_label_key not in labels:
                watch_node_response = {
                    "status": "info",
                    "message": f"New node detected: {node_name}, labeling it...",
                    "node_name": node_name
                }               
                label_node(node_name, node_role_label_key, 'true')
            else:
                watch_node_response = {
                    "status": "info",
                    "message": f"Node {node_name} already has the role label {node_role_label}",
                    "node_name": node_name
                }  
                print(json.dumps(watch_node_response))
if __name__ == "__main__":
    response = {
        "status": "info",
        "message": "Starting to watch for new nodes..."
    }
    print(json.dumps(response))
    watch_new_nodes()
