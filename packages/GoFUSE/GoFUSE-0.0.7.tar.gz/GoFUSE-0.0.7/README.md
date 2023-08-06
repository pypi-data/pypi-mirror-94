# GoFUSE

GoFUSE is a pyfuse / xmlrpc based distributed filesystem.

## Installation

```
pip3 install GoFUSE
```

## Usage

```
python3 -m GoFUSE.server ./data
python3 -m GoFUSE.client /mnt/test
```

### Example

```
LOGLEVEL=DEBUG python3 -m GoFUSE.server .
```
