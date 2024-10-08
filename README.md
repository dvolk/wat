# wat.py

<p align="center">
<img width="32%" src="https://i.imgur.com/paeGhbf.png"/><img width="32%" src="https://i.imgur.com/2PFLncp.png"/><img width="32%" src="https://i.imgur.com/870o5Ln.png"/>
</p>

wat.py is a viewer for kubernetes resources

It presents a menu of kubernetes resources and crd 'kinds' (such as `pods`, `nodes`, `clusterrolebindings`, etc)

Once you select a `kind`, it presents a menu of kubernetes resources of the kind you selected.

After selecting a kubernetes resource, it launches a pager showing the output of `kubectl get <kind> <resource> [-n <namespace>] -o yaml`

This allows for quick and efficient listing and viewing of all kubernetes resources (including custom resources).

## Requirements

- `kubectl` (https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
- `jless` (https://github.com/PaulJuliusMartinez/jless/releases)
- `fzf` (`apt install fzf`)
- `pyfzf` (`pip3 install pyfzf`)

## Running

`python3 wat.py [--editor EDITOR] [--namespace NAMESPACE]`

## Notes

In `fzf` menus, press `control-c` to go up a level.

## Ideas for future work

- Custom narrower with table view
- Custom pager with actions such as edit and exec
