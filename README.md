# wat.py

<p align="center">
<img width="32%" src="https://i.imgur.com/tABEGLg.png"/><img width="32%" src="https://i.imgur.com/OMqZRXZ.png"/><img width="32%" src="https://i.imgur.com/UqWTWY1.png"/>
</p>

wat.py is a viewer for kubernetes resources

It uses fzf-based to present a menu of kubernetes resources and crd 'kinds' (such as `pods`, `nodes`, `clusterrolebindings`, etc)

Once you select one, it gives you a fzf-based menu of kubernetes resources of the kind you selected.

Once you select a kubernetes resource, it launches a pager showing the output of `kubectl get <kind> <resource> [-n <namespace>] -o yaml`

This allows for quick and efficient browsing of all kubernetes resources (including custom resources).

## requirements

- `kubectl` (https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
- `bat` (`apt install bat`)
- `fzf` (`apt install fzf`)
- `pyfzf` (`pip3 install pyfzf`)

## Running

`python3 wat.py`

## Notes

In `fzf` menus, press `control-c` to go up a level.

In the pager, press `q` to go back to the resource list.
