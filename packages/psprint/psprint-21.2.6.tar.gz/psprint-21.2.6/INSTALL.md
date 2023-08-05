Prerequisites
---------------

Python


pip
----

Preferred method

### Install

```sh
pip install psprint
```


### Update

```sh
pip install -U psprint
```


### Uninstall

You may have to do this multiple times until a warning message informs:

<span style="background-color: black; color: yellow;">WARNING: Skipping psprint as it is not installed.</span>

```sh
pip uninstall -y psprint
```


[pspman](https://github.com/pradyparanjpe/pspman)
--------------------------------------------------

(Linux only)

For automated management: updates, etc

**Caution**: PSPMan is unstable and under testing.

### Install

```sh
pspman -s -i https://github.com/pradyparanjpe/psprint.git
```


### Update

```sh
pspman
```

That's it.


### Uninstall

Remove installation: TODO: Include this in future PSPMan releases

```sh
pip uninstall -y psprint
```

Remove repository clone

```sh
pspman -s -d psprint
```
