from kubernetes import client, config, watch
import os
import json

config.load_incluster_config()
v1 = client.CoreV1Api()
role_label_key = "node-group"

def label_node(node_name, key, value):
    body = {
        "metadata": {
            "labels": {
                key: value
            }
        }
    }
    try:
        v1.patch_node(node_name, body)
        response = {
            "status": "success",
            "message": f"Successfully labeled node {node_name} with {key}={value}",
            "node_name": node_name,
            "label": {key: value}
        }
        # print(f"Successfully labeled node {node_name} with {key}={value}")
    except client.exceptions.ApiException as e:
        response = {
            "status": "error",
            "message": f"Failed to label node {node_name}: {e}",
            "node_name": node_name
        }
    return json.dumps(response)
        # print(f"Failed to label the node {node_name}: {e}")

def watch_new_nodes():
    w = watch.Watch()
    for event in w.stream(v1.list_node):
        node = event["object"]
        node_name = node.metadata.name
        node_role_label = node.metadata.labels.get(role_label_key)
        node_role_label_key = f'node-role.kubernetes.io/{node_role_label}'
        event_type = event["type"]

        if event_type == "ADDED":
            labels = set(node.metadata.labels.keys())
            if node_role_label_key not in labels:
                response = {
                    "status": "info",
                    "message": f"New node detected: {node_name}, labeling it...",
                    "node_name": node_name
                }
                # print(f"New node detected: {node_name}, labeling it...")
                label_node(node_name, node_role_label_key, 'true')
            else:
                response = {
                    "status": "info",
                    "message": f"Node {node_name} already has the role label {node_role_label}",
                    "node_name": node_name
                }  
                print(json.dumps(response))          
                # print(f"Node {node_name} already has the role label.{node_role_label}")

if __name__ == "__main__":
    response = {
        "status": "info",
        "message": "Starting to watch for new nodes..."
    }
    print(json.dumps(response))
    # print("Starting to watch for new nodes...")
    watch_new_nodes()
