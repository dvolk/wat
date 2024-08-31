# wat.py

wat.py is a viewer for kubernetes resources

It uses fzf-based to present a menu of kubernetes resources and crd 'kinds' (such as `pods`, `nodes`, `clusterrolebindings`, etc)

Once you select one, it gives you a fzf-based menu of kubernetes resources of the kind you selected.

Once you select a kubernetes resource, it launches a pager showing the output of `kubectl get <kind> <resource> [-n <namespace>] -o yaml`

This allows for quick and efficient browsing of all kubernetes resources.
