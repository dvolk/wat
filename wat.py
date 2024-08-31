import json
import tempfile
import subprocess
import os

import pyfzf


def main():
    editor = os.environ.get("EDITOR")
    if not editor:
        editor = ["bat", "--color", "always", "--paging", "always"]
    else:
        editor = [editor]

    fzf = pyfzf.FzfPrompt()

    resources = subprocess.check_output(["kubectl", "api-resources"], text=True).split(
        "\n"
    )
    resources = resources[1:-1]

    crds = subprocess.check_output(["kubectl", "get", "crd"], text=True).split("\n")
    crds = crds[1:-1]

    all_resources = resources + crds

    res_opts = [line.split(" ")[0] for line in all_resources]

    while sel_res := fzf.prompt(res_opts):
        sel_res = sel_res[0]

        try:
            r = subprocess.check_output(
                ["kubectl", "get", sel_res, "-A", "-o", "json"], text=True
            )
        except subprocess.CalledProcessError:
            print(f"Failed to retrieve resources for {sel_res}. Skipping.")
            continue

        r = json.loads(r)["items"]

        item_namespaces = {
            obj["metadata"].get("name"): obj["metadata"].get("namespace") for obj in r
        }

        names = [obj["metadata"].get("name") for obj in r]

        while sel_obj := fzf.prompt(names):
            sel_obj = sel_obj[0]
            namespace = item_namespaces[sel_obj]

            if namespace:
                command = [
                    "kubectl",
                    "get",
                    sel_res,
                    sel_obj,
                    "-o",
                    "yaml",
                    "-n",
                    namespace,
                ]
            else:
                command = ["kubectl", "get", sel_res, sel_obj, "-o", "yaml"]

            try:
                r = subprocess.check_output(command, text=True)
            except subprocess.CalledProcessError:
                print(f"Failed to retrieve details for {sel_obj}. Skipping.")
                continue

            with tempfile.NamedTemporaryFile(
                mode="wt", delete=False, prefix=f"{sel_res}.{sel_obj}", suffix=".yaml"
            ) as f:
                f.write(r)
                f.close()
                subprocess.run(editor + [f.name])


if __name__ == "__main__":
    main()
