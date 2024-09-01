import json
import tempfile
import subprocess
import shlex

import pyfzf
import argh


def main(editor=None, namespace=None):
    if not editor:
        editor = ["jless"]
    else:
        editor = [editor]

    fzf = pyfzf.FzfPrompt()

    resources = subprocess.check_output(
        ["kubectl", "api-resources", "-o", "wide"], text=True
    ).split("\n")
    resources = resources[1:-1]

    crds = subprocess.check_output(["kubectl", "get", "crd"], text=True).split("\n")
    crds = crds[1:-1]

    all_resources = resources + crds

    # resource_verbs = {r.split()[0]: r.split()[-1].split(",") for r in resources}

    res_opts = [line.split()[0] for line in all_resources]

    while sel_res := fzf.prompt(res_opts):
        sel_res = sel_res[0]
        cmd = ["kubectl", "get", sel_res, "-o", "json"]
        if namespace:
            cmd = cmd + ["-n", namespace]
        else:
            cmd = cmd + ["-A"]

        try:
            print(shlex.join(cmd))
            r = subprocess.check_output(cmd, text=True)
        except subprocess.CalledProcessError:
            continue

        r = json.loads(r)["items"]

        item_namespaces = {
            obj["metadata"].get("name"): obj["metadata"].get("namespace") for obj in r
        }

        names = [obj["metadata"].get("name") for obj in r]

        while sel_obj := fzf.prompt(names):
            sel_obj = sel_obj[0]
            item_namespace = item_namespaces[sel_obj]

            if item_namespace:
                cmd = [
                    "kubectl",
                    "get",
                    sel_res,
                    sel_obj,
                    "-o",
                    "yaml",
                    "-n",
                    item_namespace,
                ]
            else:
                cmd = ["kubectl", "get", sel_res, sel_obj, "-o", "yaml"]

            try:
                print(shlex.join(cmd))
                r = subprocess.check_output(cmd, text=True)
            except subprocess.CalledProcessError:
                continue

            with tempfile.NamedTemporaryFile(
                mode="wt", delete=False, prefix=f"{sel_res}_{sel_obj}-", suffix=".yaml"
            ) as f:
                f.write(r)
                f.close()
                subprocess.run(editor + [f.name])


if __name__ == "__main__":
    argh.dispatch_command(main)

