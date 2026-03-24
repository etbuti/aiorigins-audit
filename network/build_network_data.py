import json, time

nodes = [
    # 从 node 状态收集
]

out = {
    "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "nodes": nodes
}

open("network/data.json","w").write(json.dumps(out, indent=2))
