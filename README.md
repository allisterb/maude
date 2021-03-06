<p align="center">
  <img src="https://dm2301files.storage.live.com/y4mcsbz3k1tSwFp5Yhk20iT2u0dWQdar8ylYMSSZ0cdd8zQgZ-6nn8-CGCbxEZm-6SeSxl7lBTw8OzQpTx1Hnj56jNZ2LvBKg8GRLUDMW_jPufXzSVq3_yZS6V1rTlOBn-YZUtXQyVn1Xiep3lGTRMMePOu5UhC1S7aPRpxu8eUgfZQuMh321ISJU7qiO8yYWKn?width=469&height=469&cropmode=none" />

<img src="https://github.com/allisterb/maude/blob/master/doc/screencap1.webp?raw=true" type="image/webp" width="640" height="480" />
</p>

# Requirements
* libclamav-dev (*nix/macOS)

# Building
1. Create a venv e.g `python3 -m venv maude` and activate it.
2. Clone the repo and submodules:  `git clone https://github.com/allisterb/maude --recurse-submodules`
3. Run `install.cmd` on Windows or `install.sh` on *nix/macOS.  On systems with a small amount of memory like a VPS you may get an error like `install.sh: line 5: 382383 Killed                  pip install ext/nsfw_model` in which case you should use `install_lowmem.sh`.
4. Download `models.zip` or `models.tar.gz` from the latest [release](https://github.com/allisterb/maude/releases) and unzip/untar in the root repo directory so you have a `models` directory alongside `doc` and `test` et.al. Note this step is only required when installing directly from the git repo; the release archives already include the `models` folder.
5. To use [Microsoft PhotoDNA](https://www.microsoft.com/en-us/photodna) hashing you must put the `PhotoDNAx64.dll` (Windows) or `PhotoDNAx64.so` (Mac) where the maude Python interpreter can find it: e.g. on Windows in the `Scripts` folder of your maude Python venv. See [here](https://github.com/jankais3r/pyPhotoDNA) for more info.
6. On Windows the `libclamav*` DLLs are bundled with maude however on other platforms you'll have to install it yourself using your package manager e.g. `sudo apt-get install libclamav-dev` or other method. See https://github.com/Cisco-Talos/clamav/blob/main/INSTALL.md for more info.
7. Run `maude` or `maude.sh` from the root repo folder.

# Getting started
1. Use the `start_ipfs` scripts to start an IPFS instance e.g `./start_ipfs.sh ipfs.log ../../go-ipfs/ipfs` or set the appropriate environment variables and flags yourself based on what the script says. IPFS needs to run with the `--enable-pubsub-experiment` flag and JSON log output. See the [script](https://github.com/allisterb/maude/blob/master/start_ipfs.sh) for full details.
2. If this is the first time you are running maude you will need to generate a keypair for your instance: `maude[.sh] crypto gen`. 
3. To start the maude server in monitor mode say `maude[.sh] server monitor`. This will start monitoring a local IPFS node using the node's logs and will detect when a CID is pinned locally. maude tries to detect the type of file being pinned like a binary executable or archive or a document like a pdf or a media file like an image or video. It then runs different classifiers and detectors on the file like computer vision models that can detect NSFW images and videos, and malware detectors like ClamAV and YARA rulesets on binary executables and archives. maude publishes the raw classification data to an IPFS pubsub topic. 
4. You can subscribe to the topic e.g `ipfs pubsub sub maude` to see the data maude publishes on pinned files.
5. There are other maude commands for running the ML models and scanners on local files e.g. `maude image classify --nudenet /path/to/a/image` See `maude --help` for the full list of commands.
