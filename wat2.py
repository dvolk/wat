import subprocess
import json
import shlex

import argh
import flask
import waitress
import yaml

from pygments import highlight
from pygments.lexers import YamlLexer
from pygments.formatters import HtmlFormatter


app = flask.Flask(__name__)


def init():
    resources = subprocess.check_output(
        ["kubectl", "api-resources", "-o", "wide"], text=True
    ).split("\n")
    resources = resources[1:-1]

    crds = subprocess.check_output(["kubectl", "get", "crd"], text=True).split("\n")
    crds = crds[1:-1]

    all_resources = resources + crds

    resource_verbs = {r.split()[0]: r.split()[-1].split(",") for r in resources}
    resource_names = [line.split()[0] for line in all_resources]
    return sorted(resource_names), resource_verbs


@app.route("/container_log/<pod_namespace>/<pod_name>/<container_name>")
def container_log(pod_namespace, pod_name, container_name):
    log_cmd = [
        "kubectl",
        "logs",
        pod_name,
        "-c",
        container_name,
        "-n",
        pod_namespace,
        "--timestamps",
    ]
    container_log = subprocess.check_output(log_cmd, text=True)
    return flask.render_template(
        "container_log.jinja2",
        container_log=container_log,
        container_name=container_name,
    )


@app.route("/resource/<resource_name>")
def resource(resource_name):
    cmd = ["kubectl", "get", resource_name, "-o", "json"]
    cmd = cmd + ["-A"]

    print(shlex.join(cmd))
    r = subprocess.check_output(cmd, text=True)
    # print(r)

    items_data = json.loads(r)["items"]

    item_namespaces = {
        obj["metadata"].get("name"): obj["metadata"].get("namespace")
        for obj in items_data
    }
    item_names = [obj["metadata"].get("name") for obj in items_data]

    return flask.render_template(
        "resource.jinja2",
        resource_name=resource_name,
        item_namespaces=item_namespaces,
        item_names=item_names,
        items_data=items_data,
    )


def yaml_highlight(data):
    formatter = HtmlFormatter()
    formatter.noclasses = True
    formatter.cssclass = "code"
    return highlight(data, YamlLexer(), formatter)


@app.route("/item/<resource_name>/<item_name>")
def item(resource_name, item_name):
    item_namespace = flask.request.args.get("item_namespace")

    cmd = [
        "kubectl",
        "get",
        resource_name,
        item_name,
        "-o",
        "yaml",
    ]
    if item_namespace:
        cmd = cmd + ["-n", item_namespace]

    item_data = subprocess.check_output(cmd, text=True)
    item_dict = yaml.safe_load(item_data)

    return flask.render_template(
        "item.jinja2",
        resource_name=resource_name,
        item_name=item_name,
        item_namespace=item_namespace,
        item_data=item_data,
        item_dict=item_dict,
        yaml_highlight=yaml_highlight,
    )


@app.route("/")
def index():
    return flask.render_template(
        "index.jinja2",
        resource_names=resource_names,
        resource_verbs=resource_verbs,
    )


def main():
    global resource_names
    global resource_verbs
    resource_names, resource_verbs = init()

    app.run(port=1234, debug=True)
    # waitress.serve(app, port=1234)


if __name__ == "__main__":
    argh.dispatch_command(main)
